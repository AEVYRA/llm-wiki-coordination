#!/usr/bin/env python3
"""
LLM Wiki Integrity Audit — Generic v2 (enhanced).
Drop-in audit tool for any llm-wiki-coordination compatible repo.

Covers L0 (hygiene), L1 (graph), L2 (protocol/consensus/source/crypto),
and optional L3 (cross-protocol consistency).

Usage:
  python3 llm-wiki-audit.py [root] [--strict-legacy] [--json] [--layer L3]
  python3 llm-wiki-audit.py . --legacy-cutoff 2026-05-12
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlparse

import yaml

HARD = "HARD"
WARN = "WARN"
INFO = "INFO"

VALID_TIERS = {"working", "episodic", "semantic", "procedural"}
VALID_ENTRY_TYPES = {"contribution", "closure", "reopen"}
VALID_DIALOGUE_STATUSES = {"open", "crystallized", "crystallizing", "closed-without-crystallization",
                           "awaiting-crystallization", "reopened"}
DIALOGUE_STATUS_PATTERN = re.compile(r"^pending-[A-Za-zЀ-ӿ][A-Za-z0-9Ѐ-ӿ_-]*$")


def is_valid_dialogue_status(status):
    if status in VALID_DIALOGUE_STATUSES:
        return True
    return bool(DIALOGUE_STATUS_PATTERN.match(status))

VALID_LIFECYCLES = {"draft", "working", "proposal", "accepted", "deprecated"}

DEFAULT_LEGACY_CUTOFF = "2026-05-12"

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")
WIKILINK_RE = re.compile(r"(?<!!)\[\[([^\]]+)\]\]")
PRIVATE_KEY_PATTERNS = [
    re.compile(r"private[_-]?key", re.IGNORECASE),
    re.compile(r"secret[_-]?key", re.IGNORECASE),
    re.compile(r"-----BEGIN.*PRIVATE KEY-----"),
    re.compile(r"ed25519[_-]?priv", re.IGNORECASE),
    re.compile(r"хранит.*приватный.*ключ", re.IGNORECASE),
    re.compile(r"модель.*держит.*ключ", re.IGNORECASE),
    re.compile(r"model\s+(stores|holds|keeps).*key", re.IGNORECASE),
]
PRIVATE_KEY_NEGATION_RE = re.compile(
    r"(не\s+(хранит|держит|умеет|содержит|генерирует|может\s+(над[её]жно\s+)?хранить).{0,30}(ключ|key))|"
    r"((does|should)\s+not|doesn't|cannot|can't|never|won't).{0,30}(store|hold|keep|generate).{0,20}key|"
    r"key.{0,30}(lives|жив[её]т|долж[её]н\s+(быть|жить|находиться)).{0,20}(tool|repo|локальн)|"
    r"tool/repo\s+layer|"
    r"bounded\s+substrate-portability",
    re.IGNORECASE
)


class GenericWikiAudit:
    def __init__(self, root_dir, legacy_cutoff=DEFAULT_LEGACY_CUTOFF, strict_legacy=False, max_layer=3):
        self.root_dir = Path(root_dir).resolve()
        self.legacy_cutoff = legacy_cutoff
        self.strict_legacy = strict_legacy
        self.max_layer = max_layer
        self.findings = []
        self.wikilink_index = None
        self.heading_index = {}
        self._file_cache = {}

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def report(self, severity, type_, layer, invariant, file, locus, reason, proposed_action):
        path = Path(file)
        display_path = str(path if not path.is_absolute() else path.relative_to(self.root_dir))
        self.findings.append({
            "severity": severity,
            "type": type_,
            "layer": layer,
            "violated_invariant": invariant,
            "file": display_path,
            "locus": locus,
            "reason": reason,
            "proposed_action": proposed_action,
            "detected_by": "script",
        })

    def markdown_files(self):
        wiki_dir = self.root_dir / "wiki"
        if not wiki_dir.exists():
            return []
        return sorted(wiki_dir.rglob("*.md"))

    def read_text(self, path):
        p = Path(path)
        if p not in self._file_cache:
            self._file_cache[p] = p.read_text(encoding="utf-8")
        return self._file_cache[p]

    def strip_markdown_code(self, text):
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        return re.sub(r"`[^`\n]*`", "", text)

    def parse_frontmatter(self, path):
        text = self.read_text(path)
        if not text.startswith("---\n"):
            return {}, text
        match = re.match(r"^---\n(.*?)\n---\n?", text, re.DOTALL)
        if not match:
            self.report(HARD, "Block", "L0", "B", path, "frontmatter",
                        "Unclosed YAML frontmatter", "Close frontmatter with a second --- line")
            return {}, text
        raw = match.group(1)
        try:
            return yaml.safe_load(raw) or {}, text[match.end():]
        except yaml.YAMLError as exc:
            self.report(HARD, "Block", "L0", "B", path, "frontmatter",
                        f"Invalid YAML frontmatter: {exc}", "Fix frontmatter YAML")
            return {}, text[match.end():]

    def extract_headings(self, text):
        headings = {}
        for match in HEADING_RE.finditer(text):
            title = match.group(2).strip()
            slug = title.lower().strip()
            slug = re.sub(r"\s+", "-", slug)
            slug = re.sub(r"[^\w\-]", "", slug, flags=re.UNICODE)
            slug = re.sub(r"-{2,}", "-", slug)
            headings[slug] = title
            headings[title.lower()] = title
        return headings

    def _build_heading_index(self):
        for path in self.markdown_files():
            text = self.read_text(path)
            self.heading_index[path] = self.extract_headings(text)

    def is_legacy_dialogue_file(self, path):
        if self.strict_legacy:
            return False
        frontmatter, _ = self.parse_frontmatter(path)
        created = frontmatter.get("created") or frontmatter.get("opened_at") or frontmatter.get("opened")
        if created is None:
            return False
        return str(created) < self.legacy_cutoff

    # ==================================================================
    # L0: HYGIENE
    # ==================================================================

    def run_l0_hygiene(self):
        wiki_dir = self.root_dir / "wiki"
        if not wiki_dir.exists():
            return
        for path in self.markdown_files():
            self._check_l0_file(path)

    def _check_l0_file(self, path):
        frontmatter, content = self.parse_frontmatter(path)

        if "tier" not in frontmatter:
            self.report(WARN, "Hygiene", "L0", "B", path, "frontmatter",
                        "Missing 'tier:' field",
                        "Add 'tier: working|episodic|semantic|procedural' to frontmatter")
        elif frontmatter["tier"] not in VALID_TIERS:
            self.report(WARN, "Hygiene", "L0", "B", path, "frontmatter.tier",
                        f"Invalid tier '{frontmatter['tier']}', expected one of {VALID_TIERS}",
                        "Set tier to a valid value")

        stripped = content.strip()
        if not stripped or (len(stripped) < 20 and path.suffix == ".md"):
            self.report(WARN, "Hygiene", "L0", "B", path, "content",
                        "File appears empty or near-empty",
                        "Add content or remove the file with a tombstone entry")

    # ==================================================================
    # L1: GRAPH
    # ==================================================================

    def run_l1_graph(self):
        log_path = self.root_dir / "wiki" / "log.md"
        if not log_path.exists():
            self.report(HARD, "Block", "L1", "C", log_path, "file",
                        "wiki/log.md is missing", "Create wiki/log.md")

        self._build_wikilink_index()
        self._build_heading_index()
        self._check_markdown_links()
        self._check_obsidian_wikilinks()
        self._check_heading_anchors()
        self._check_orphans()
        self._check_index_completeness()

    def _build_wikilink_index(self):
        idx = defaultdict(list)
        wiki_dir = self.root_dir / "wiki"
        for path in self.markdown_files():
            rel = path.relative_to(wiki_dir)
            idx[path.stem].append(path)
            idx[str(rel.with_suffix(""))].append(path)
            idx[str(rel)].append(path)
        self.wikilink_index = idx

    def _resolve_wikilink(self, current_path, target):
        if self.wikilink_index is None:
            self._build_wikilink_index()
        target = target.split("|", 1)[0].split("#", 1)[0].strip()
        if not target:
            return True
        target = target.replace("\\", "/")
        candidates = []
        if "/" in target:
            raw = Path(target)
            if raw.suffix != ".md":
                raw = raw.with_suffix(".md")
            candidates.extend([
                (current_path.parent / raw).resolve(),
                (self.root_dir / "wiki" / raw).resolve(),
            ])
        else:
            candidates.extend(self.wikilink_index.get(target, []))
            if not target.endswith(".md"):
                candidates.extend(self.wikilink_index.get(f"{target}.md", []))
        return any(Path(c).exists() for c in candidates)

    def _check_markdown_links(self):
        for path in self.markdown_files():
            text = self.strip_markdown_code(self.read_text(path))
            for match in LINK_RE.finditer(text):
                target = match.group(2).strip()
                if not target or target.startswith("#"):
                    continue
                if "://" in target or target.startswith("mailto:"):
                    continue
                target = unquote(target.split("#", 1)[0].strip("<>"))
                parsed = urlparse(target)
                if parsed.scheme:
                    continue
                resolved = (path.parent / target).resolve()
                try:
                    resolved.relative_to(self.root_dir)
                except ValueError:
                    continue
                if not resolved.exists():
                    self.report(HARD, "Block", "L1", "S2", path, f"link:{target}",
                                "Markdown link points to a missing local file",
                                "Update the link target or restore the referenced file")

    def _check_obsidian_wikilinks(self):
        for path in self.markdown_files():
            text = self.strip_markdown_code(self.read_text(path))
            for match in WIKILINK_RE.finditer(text):
                target = match.group(1).strip()
                if not self._resolve_wikilink(path, target):
                    self.report(HARD, "Block", "L1", "S2", path, f"wikilink:{target}",
                                "Obsidian wiki-link points to a missing local file",
                                "Update the wiki-link target or create the referenced page")

    def _check_heading_anchors(self):
        for path in self.markdown_files():
            text = self.strip_markdown_code(self.read_text(path))
            for match in LINK_RE.finditer(text):
                target = match.group(2).strip()
                if "#" not in target or target.startswith("#"):
                    continue
                if "://" in target:
                    continue
                file_part, anchor = target.split("#", 1)
                if not file_part:
                    target_path = path
                else:
                    file_part = unquote(file_part.strip("<>"))
                    target_path = (path.parent / file_part).resolve()
                    try:
                        target_path.relative_to(self.root_dir)
                    except ValueError:
                        continue
                    if not target_path.exists():
                        continue
                if target_path in self.heading_index:
                    anchor_lower = anchor.lower().strip()
                    headings = self.heading_index[target_path]
                    if anchor_lower not in headings:
                        self.report(WARN, "Block", "L1", "S2", path, f"link:{target}",
                                    f"Heading anchor '#{anchor}' not found in {target_path.relative_to(self.root_dir)}",
                                    "Update the heading anchor or add the referenced heading")

    def _check_orphans(self):
        wiki_dir = self.root_dir / "wiki"
        all_pages = set()
        linked_pages = set()
        for path in self.markdown_files():
            rel = str(path.relative_to(wiki_dir))
            all_pages.add(rel)
            text = self.strip_markdown_code(self.read_text(path))
            for match in LINK_RE.finditer(text):
                target = match.group(2).strip()
                if not target or "://" in target:
                    continue
                target = unquote(target.split("#", 1)[0].strip("<>"))
                resolved = path.parent / target
                try:
                    resolved = resolved.resolve()
                    resolved.relative_to(self.root_dir)
                    linked_pages.add(str(resolved.relative_to(wiki_dir)))
                except (ValueError, OSError):
                    pass
            for match in WIKILINK_RE.finditer(text):
                target = match.group(1).split("|")[0].split("#")[0].strip()
                if not target:
                    continue
                if "/" not in target:
                    target = target + ".md" if not target.endswith(".md") else target
                raw = Path(target)
                resolved = path.parent / raw
                try:
                    resolved = resolved.resolve()
                    resolved.relative_to(self.root_dir)
                    linked_pages.add(str(resolved.relative_to(wiki_dir)))
                except (ValueError, OSError):
                    pass

        entrypoints = {"index.md", "overview.md", "ai-readme.md", "CRITICAL_FACTS.md",
                       "MEMORY.md", "SOUL.md", "hints.md", "hot.md", "log.md",
                       "agents/handoff-log.md", "agents/_context.md"}
        for page in sorted(all_pages - linked_pages):
            if page in entrypoints:
                continue
            if "/dialogue/" in page or "/honest/" in page or "/notes/" in page:
                continue
            if page.endswith("/_context.md"):
                continue
            self.report(INFO, "Graph", "L1", "S3", wiki_dir / page, "orphan",
                        f"Page '{page}' has no incoming links from other wiki pages",
                        "Add page to wiki/index.md or link from relevant pages")

    def _check_index_completeness(self):
        index_path = self.root_dir / "wiki" / "index.md"
        if not index_path.exists():
            return
        index_text = self.read_text(index_path)
        wiki_dir = self.root_dir / "wiki"
        for check_dir, label in [("concepts", "Concept"), ("workflows", "Workflow"), ("entities", "Entity")]:
            d = wiki_dir / check_dir
            if not d.exists():
                continue
            for path in sorted(d.glob("*.md")):
                name = path.stem
                rel = str(path.relative_to(wiki_dir))
                if name not in index_text and rel not in index_text:
                    self.report(INFO, "Graph", "L1", "S3", path, "index",
                                f"{label} '{name}' not referenced in wiki/index.md",
                                f"Add a link to [{name}]({rel}) in wiki/index.md")

    # ==================================================================
    # L2: PROTOCOL
    # ==================================================================

    def run_l2_protocol(self):
        self._check_dialogue_format()
        self._check_consensus_blocks()
        self._check_crypto_claims()

    # --- Dialogue format ---

    def _check_dialogue_format(self):
        dialogue_dir = self.root_dir / "wiki" / "agents" / "dialogue"
        if not dialogue_dir.exists():
            return
        for path in sorted(dialogue_dir.iterdir()):
            item = path.name
            if item.startswith(".") or item == "_context.md":
                continue
            if path.is_file() and path.suffix == ".md":
                if self.is_legacy_dialogue_file(path):
                    self.report(INFO, "Legacy", "L0", "D1", path, "file",
                                "Legacy dialogue thread is allowed before the directory-format cutoff",
                                "No action required until migration or crystallization")
                else:
                    self.report(HARD, "Block", "L0", "D1", path, "file",
                                "New dialogue thread must be a directory",
                                "Convert to directory format (thread.md, meta.yaml, entries/)")
                continue
            if path.is_dir():
                if not (path / "thread.md").exists():
                    self.report(HARD, "Block", "L0", "D2", path, "directory",
                                "Missing thread.md", "Create thread.md")
                if not (path / "meta.yaml").exists():
                    self.report(HARD, "Block", "L0", "D2", path, "directory",
                                "Missing meta.yaml", "Create meta.yaml")
                meta = {}
                meta_path = path / "meta.yaml"
                if meta_path.exists():
                    try:
                        meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
                    except yaml.YAMLError:
                        meta = {}
                self._check_meta_yaml(path, meta)
                entries_dir = path / "entries"
                if entries_dir.exists():
                    self._check_dialogue_entries(path, entries_dir, meta)

    def _check_meta_yaml(self, thread_dir, meta):
        if meta.get("migration_mode") == "archival":
            return
        for field in ["slug", "status", "participants"]:
            if field not in meta:
                self.report(WARN, "Protocol", "L2", "D2", thread_dir / "meta.yaml",
                            f"meta.{field}", f"Missing '{field}' in meta.yaml",
                            f"Add {field} to meta.yaml")
        status = meta.get("status")
        if status and not is_valid_dialogue_status(status):
            self.report(HARD, "Block", "L2", "D2", thread_dir / "meta.yaml",
                        "meta.status", f"Invalid status '{status}', expected one of {VALID_DIALOGUE_STATUSES} or pending-<agent>",
                        "Set status to a valid value")

    def _check_dialogue_entries(self, thread_dir, entries_dir, meta):
        if meta.get("migration_mode") == "archival":
            self.report(INFO, "Legacy", "L2", "D3", thread_dir, "migration_mode",
                        "Archival migration keeps pre-format entry metadata as historical text",
                        "No action required unless the thread is reopened")
            return
        entries = sorted(entries_dir.glob("*.md"))
        if not entries:
            return
        previous = None
        current = {"N": 0.0, "C": 0.0, "R": 0.0}
        for expected_n, entry in enumerate(entries, start=1):
            frontmatter, _ = self.parse_frontmatter(entry)
            entry_type = frontmatter.get("type")
            author = frontmatter.get("author")
            n = frontmatter.get("n")
            if n is None:
                self.report(WARN, "Protocol", "L2", "D3", entry, "frontmatter.n",
                            "Entry is missing sequence number",
                            "Add n: <sequence> or mark the thread as archival migration")
            elif n != expected_n:
                self.report(WARN, "Protocol", "L2", "D3", entry, "frontmatter.n",
                            f"Entry sequence is {n}, expected {expected_n}",
                            "Renumber entries or document archival migration")
            if entry_type and entry_type not in VALID_ENTRY_TYPES:
                self.report(HARD, "Block", "L2", "D3", entry, "frontmatter.type",
                            f"Invalid entry type '{entry_type}', expected one of {VALID_ENTRY_TYPES}",
                            "Set type to a valid value")
            if entry_type in {"contribution", "reopen", "closure"} and expected_n > 1:
                last_eval = frontmatter.get("last_eval")
                if not last_eval:
                    self.report(HARD, "Cascade", "L2", "D4", entry, "last_eval",
                                "Entry after n=1 is missing last_eval",
                                "Evaluate the previous entry in last_eval")
                else:
                    self._check_rolespace_vector(entry, "last_eval.v", last_eval.get("v"))
                    vector = last_eval.get("v") or {}
                    for axis in current:
                        if isinstance(vector.get(axis), (int, float)):
                            current[axis] += float(vector[axis])
                    ref = last_eval.get("ref")
                    if not ref:
                        self.report(HARD, "Cascade", "L2", "D4", entry, "last_eval.ref",
                                    "last_eval is missing ref",
                                    "Point last_eval.ref at the previous entry file")
                    elif previous and ref != previous.name:
                        self.report(WARN, "Protocol", "L2", "D4", entry, "last_eval.ref",
                                    f"last_eval.ref points to {ref}, expected {previous.name}",
                                    "Point last_eval.ref at the immediately previous entry")
            if previous and entry_type in {"contribution", "reopen", "closure"}:
                last_eval = frontmatter.get("last_eval") or {}
                ref = last_eval.get("ref")
                if ref == entry.name:
                    self.report(HARD, "Cascade", "L2", "D5", entry, "last_eval.ref",
                                "Entry evaluates itself", "Move peer evaluation to the next entry")
                previous_frontmatter, _ = self.parse_frontmatter(previous)
                if ref == previous.name and previous_frontmatter.get("author") == author:
                    self.report(HARD, "Cascade", "L2", "D5", entry, "last_eval.ref",
                                "Author evaluates their own previous contribution",
                                "Have a different participant evaluate the previous contribution")
            if entry_type == "closure":
                current_at_close = frontmatter.get("current_at_close")
                if not current_at_close:
                    self.report(HARD, "Block", "L2", "D6", entry, "current_at_close",
                                "Closure entry is missing current_at_close",
                                "Add current_at_close with the calculated RoleSpace vector")
                else:
                    self._check_rolespace_vector(entry, "current_at_close", current_at_close, allow_over_one=True)
                    self._compare_vectors(entry, "current_at_close", current_at_close, current)
            previous = entry
        rolespace = meta.get("rolespace") or {}
        if "current" in rolespace:
            self._check_rolespace_vector(thread_dir / "meta.yaml", "rolespace.current", rolespace["current"], allow_over_one=True)
            self._compare_vectors(thread_dir / "meta.yaml", "rolespace.current", rolespace["current"], current)

    def _check_rolespace_vector(self, path, locus, vector, allow_over_one=False):
        if not isinstance(vector, dict):
            self.report(HARD, "Cascade", "L2", "D4", path, locus,
                        "RoleSpace vector is missing or not a mapping",
                        "Use {N: <0..1>, C: <0..1>, R: <0..1>}")
            return
        for axis in ("N", "C", "R"):
            value = vector.get(axis)
            if not isinstance(value, (int, float)):
                self.report(HARD, "Cascade", "L2", "D4", path, f"{locus}.{axis}",
                            f"Missing or non-numeric RoleSpace axis {axis}",
                            "Provide numeric N/C/R values")
                continue
            if value < 0 or (value > 1 and not allow_over_one):
                max_text = ">= 0" if allow_over_one else "between 0 and 1"
                self.report(HARD, "Cascade", "L2", "D4", path, f"{locus}.{axis}",
                            f"RoleSpace axis {axis} must be {max_text}",
                            "Correct the vector value")

    def _compare_vectors(self, path, locus, declared, calculated):
        if not isinstance(declared, dict):
            return
        for axis in ("N", "C", "R"):
            value = declared.get(axis)
            if not isinstance(value, (int, float)):
                continue
            if abs(float(value) - calculated[axis]) > 0.01:
                self.report(HARD, "Cascade", "L2", "D6", path, f"{locus}.{axis}",
                            f"Declared {axis}={value} does not match calculated {calculated[axis]:.2f}",
                            "Recalculate RoleSpace current from entry last_eval vectors")

    # --- Consensus blocks ---

    def _check_consensus_blocks(self):
        wiki_dir = self.root_dir / "wiki"
        for path in self.markdown_files():
            rel = str(path.relative_to(wiki_dir))
            frontmatter, _ = self.parse_frontmatter(path)
            lifecycle = frontmatter.get("lifecycle")

            # Structural pages: workflows, concepts, agents, entities with lifecycle
            is_structural = any(rel.startswith(p + "/") or rel == p + ".md"
                                for p in ["workflows", "concepts", "agents", "entities"])
            if not is_structural:
                continue
            # Skip dialogue/honest/notes/logs
            if any(rel.startswith(s) for s in ["agents/dialogue/", "agents/honest/",
                                                 "agents/notes/", "agents/handoff-log",
                                                 "agents/agent-council"]):
                continue

            if lifecycle == "accepted" and "consensus" not in frontmatter:
                self.report(HARD, "Trust", "L2", "C4", path, "frontmatter.consensus",
                            "lifecycle is 'accepted' but no consensus block present",
                            "Add a consensus: block documenting agent endorsements")

            if "consensus" not in frontmatter:
                self.report(WARN, "Cascade", "L2", "C1", path, "frontmatter",
                            "Structural page missing 'consensus:' block",
                            "Add 'consensus:' block even if pending")

            if "consensus" in frontmatter and lifecycle == "accepted":
                consensus = frontmatter["consensus"]
                if isinstance(consensus, dict):
                    for agent_name, status in consensus.items():
                        if isinstance(status, str) and status.startswith("pending"):
                            self.report(HARD, "Cascade", "L2", "C4", path, f"consensus.{agent_name}",
                                        f"lifecycle is 'accepted' but agent '{agent_name}' is still 'pending'",
                                        "Resolve pending status or downgrade lifecycle")

    # --- Crypto claims (K1) ---

    def _check_crypto_claims(self):
        for path in self.markdown_files():
            text = self.read_text(path)
            clean = self.strip_markdown_code(text)
            for pattern in PRIVATE_KEY_PATTERNS:
                match = pattern.search(clean)
                if match:
                    start = max(0, match.start() - 80)
                    end = min(len(clean), match.end() + 80)
                    context = clean[start:end]
                    if PRIVATE_KEY_NEGATION_RE.search(context):
                        continue
                    self.report(HARD, "Trust", "L2", "K1", path, "content",
                                "Text suggests a model stores/holds private keys — violates key-custody invariant",
                                "Rephrase: keys live in tool/repo layer, never inside the model")
                    break

    # ==================================================================
    # L3: CROSS-PROTOCOL CONSISTENCY
    # ==================================================================

    def run_l3_cross_protocol(self):
        if self.max_layer < 3:
            return
        self._check_canon_pages_exist()
        self._check_agents_md_refs()
        self._check_crystallized_threads_have_sig_or_explicit_none()

    def _check_canon_pages_exist(self):
        dialogue_dir = self.root_dir / "wiki" / "agents" / "dialogue"
        if not dialogue_dir.exists():
            return
        wiki_dir = self.root_dir / "wiki"
        search_dirs = [wiki_dir, wiki_dir / "workflows", wiki_dir / "concepts",
                       wiki_dir / "entities", wiki_dir / "agents"]
        for path in sorted(dialogue_dir.iterdir()):
            if not path.is_dir():
                continue
            meta_path = path / "meta.yaml"
            if not meta_path.exists():
                continue
            try:
                meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
            except yaml.YAMLError:
                continue
            if meta.get("status") != "crystallized":
                continue
            canon_pages = meta.get("crystallization", {}).get("canon_pages", [])
            for canon in canon_pages:
                found = any((d / canon).exists() for d in search_dirs) or (wiki_dir / canon).exists()
                if not found:
                    self.report(HARD, "Cascade", "L3", "X1", meta_path, f"canon_pages.{canon}",
                                f"Crystallized thread references non-existent canon page '{canon}'",
                                "Create the referenced page or update canon_pages in meta.yaml")

    def _check_agents_md_refs(self):
        agents_path = self.root_dir / "AGENTS.md"
        if not agents_path.exists():
            return
        text = self.read_text(agents_path)
        ref_re = re.compile(r'`(wiki/[\w\-/]+\.md)`')
        for match in ref_re.finditer(text):
            ref_path = match.group(1)
            full_path = self.root_dir / ref_path
            if not full_path.exists():
                self.report(HARD, "Block", "L3", "X2", agents_path, f"ref:{ref_path}",
                            f"AGENTS.md references non-existent file '{ref_path}'",
                            "Fix the reference or restore the missing file")

    def _check_crystallized_threads_have_sig_or_explicit_none(self):
        dialogue_dir = self.root_dir / "wiki" / "agents" / "dialogue"
        if not dialogue_dir.exists():
            return
        for path in sorted(dialogue_dir.iterdir()):
            if not path.is_dir():
                continue
            meta_path = path / "meta.yaml"
            if not meta_path.exists():
                continue
            try:
                meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
            except yaml.YAMLError:
                continue
            if meta.get("status") != "crystallized":
                continue
            crystallization = meta.get("crystallization", {})
            if "signature" not in crystallization:
                self.report(WARN, "Protocol", "L3", "X1", meta_path, "crystallization.signature",
                            "Crystallized thread has no 'signature' field in crystallization block",
                            "Add 'signature: null' (explicit none) or the actual signature pointer")

    # ==================================================================
    # Report output
    # ==================================================================

    def print_report(self, as_json=False):
        if as_json:
            print(json.dumps({"findings": self.findings, "summary": self._summary()},
                             indent=2, ensure_ascii=False))
            return
        if not self.findings:
            print("Audit: 100% integrity. No structural issues found.")
            return
        summary = self._summary()
        print(f"LLM Wiki Integrity Audit — "
              f"HARD: {summary['HARD']}, WARN: {summary['WARN']}, INFO: {summary['INFO']}")
        print("-" * 80)
        for f in self.findings:
            print(f"[{f['severity']}] {f['violated_invariant']} ({f['type']}) @ {f['layer']}")
            print(f"File: {f['file']} ({f['locus']})")
            print(f"Reason: {f['reason']}")
            print(f"Proposed: {f['proposed_action']}")
            print("-" * 80)

    def _summary(self):
        counts = {HARD: 0, WARN: 0, INFO: 0}
        for f in self.findings:
            counts[f["severity"]] = counts.get(f["severity"], 0) + 1
        return counts

    def run(self):
        self.run_l0_hygiene()
        self.run_l1_graph()
        self.run_l2_protocol()
        if self.max_layer >= 3:
            self.run_l3_cross_protocol()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit an LLM wiki coordination layer (v2 enhanced).")
    parser.add_argument("root", nargs="?", default=os.getcwd(), help="Wiki/repository root")
    parser.add_argument("--legacy-cutoff", default=DEFAULT_LEGACY_CUTOFF, help="Single-file threads before this date are legacy INFO, not HARD")
    parser.add_argument("--strict-legacy", action="store_true", help="Treat all single-file dialogue threads as D1 HARD errors")
    parser.add_argument("--json", action="store_true", help="Output findings as JSON")
    parser.add_argument("--layer", type=int, default=3, help="Maximum audit layer (0-3, default: 3)")
    args = parser.parse_args()

    audit = GenericWikiAudit(args.root, legacy_cutoff=args.legacy_cutoff,
                             strict_legacy=args.strict_legacy, max_layer=args.layer)
    audit.run()
    audit.print_report(as_json=args.json)
    sys.exit(0 if audit._summary()[HARD] == 0 else 1)

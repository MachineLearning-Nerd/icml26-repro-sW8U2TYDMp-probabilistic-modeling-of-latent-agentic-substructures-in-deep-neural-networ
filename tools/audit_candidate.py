"""Evaluator-blind audit for a fresh candidate Space directory.

The audit starts only from logbook.json/pages/index.md, follows the declared
navigation and local Markdown links, and reports paths rather than file
contents for secret-pattern findings.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SECRET_PATTERNS = (
    re.compile(rb"hf_[A-Za-z0-9]{20,}"),
    re.compile(rb"AKIA[A-Z0-9]{16}"),
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


def navigation(node: dict) -> list[tuple[str, Path]]:
    rows = [(node["slug"], Path(node["file"]))]
    for child in node.get("children", []):
        rows.extend(navigation(child))
    return rows


def local_links(path: Path, root: Path, slug_paths: dict[str, Path]) -> list[Path]:
    text = path.read_text(encoding="utf-8")
    targets: list[Path] = []
    for raw in LINK_RE.findall(text):
        target = raw.strip().split("#", 1)[0]
        if raw.startswith("#/"):
            slug = raw[2:].split("?", 1)[0]
            if slug not in slug_paths:
                raise AssertionError(f"unknown navigation slug {slug!r} in {path}")
            targets.append(root / slug_paths[slug])
        elif not target or "://" in target or target.startswith("mailto:"):
            continue
        else:
            targets.append((path.parent / target).resolve())
    return targets


def audit(root: Path, historical_manifest: Path | None) -> dict:
    root = root.resolve()
    logbook_path = root / "logbook.json"
    logbook = json.loads(logbook_path.read_text(encoding="utf-8"))
    nav = navigation(logbook["root"])
    slug_paths = dict(nav)
    assert slug_paths["index"] == Path("pages/index.md")

    opened: set[Path] = {logbook_path}
    queue = [root / path for _, path in nav]
    missing: list[str] = []
    while queue:
        path = queue.pop(0).resolve()
        if path in opened:
            continue
        if not path.is_file():
            missing.append(str(path.relative_to(root)))
            continue
        opened.add(path)
        if path.suffix.lower() == ".md":
            for linked in local_links(path, root, slug_paths):
                try:
                    linked.relative_to(root)
                except ValueError as exc:
                    raise AssertionError(f"link escapes candidate root: {linked}") from exc
                if linked not in opened:
                    queue.append(linked)
    assert not missing, f"missing reachable files: {missing}"

    fixed_command = (
        "uv sync --locked --no-dev && "
        ".venv/bin/python -m reproduction.run_all"
    )
    claim_statuses: dict[str, str] = {}
    for number in range(1, 7):
        path = root / f"pages/current-claim-{number}/page.md"
        text = path.read_text(encoding="utf-8")
        required = (
            "2509.06701v2",
            "013a579947622a09d4375d4d4d4cb18aa8c61728ed3070c83f084c40140f0282",
            fixed_command,
            "c2b9aefefc290d44097b4bdd18d5e8e7cf707ba4",
            "seed `42`",
            "one local CPU",
            "raw",
            "checker",
            "control",
            "limitations",
        )
        absent = [item for item in required if item not in text]
        assert not absent, f"claim {number} missing canonical fields: {absent}"
        status = "FALSIFIED" if "**Verdict contract: FALSIFIED**" in text else "VERIFIED"
        claim_statuses[str(number)] = status

    visibility = (root / "pages/visibility/page.md").read_text(encoding="utf-8")
    assert visibility.count("| VERIFIED |") == 5
    assert visibility.count("| FALSIFIED |") == 1
    assert "Historical rejected baseline" in visibility
    assert (root / "reproduction/verifier.py").is_file()
    assert (root / "reproduction/independent_checker.py").is_file()
    assert (root / "evidence/run_summary.json").is_file()

    json_files = sorted(root.rglob("*.json"))
    for path in json_files:
        if "/.cache/" not in path.as_posix():
            json.loads(path.read_text(encoding="utf-8"))

    secret_paths: set[str] = set()
    for path in root.rglob("*"):
        if not path.is_file() or "/.cache/" in path.as_posix():
            continue
        data = path.read_bytes()
        if any(pattern.search(data) for pattern in SECRET_PATTERNS):
            secret_paths.add(str(path.relative_to(root)))
    assert not secret_paths, f"secret-like patterns detected in {sorted(secret_paths)}"

    historical = {
        "manifest_entries": 0,
        "root_path_subset": False,
        "exact_historical_copy": False,
    }
    if historical_manifest:
        entries: list[tuple[str, str]] = []
        for line in historical_manifest.read_text(encoding="utf-8").splitlines():
            digest, relative = line.split("  ", 1)
            entries.append((digest, relative))
        historical["manifest_entries"] = len(entries)
        historical["root_path_subset"] = all((root / relative).is_file() for _, relative in entries)
        exact = True
        for digest, relative in entries:
            copied = root / "historical/judged-3d065680" / relative
            if not copied.is_file() or hashlib.sha256(copied.read_bytes()).hexdigest() != digest:
                exact = False
                break
        historical["exact_historical_copy"] = exact
        assert historical["root_path_subset"]
        assert historical["exact_historical_copy"]

    return {
        "audit_status": "PASS",
        "canonical_entrypoint": "pages/index.md",
        "opened_files": sorted(str(path.relative_to(root)) for path in opened),
        "opened_file_count": len(opened),
        "claim_statuses": claim_statuses,
        "missing_reachable_files": missing,
        "secret_pattern_paths": sorted(secret_paths),
        "json_files_validated": len(json_files),
        "historical_evidence": historical,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--historical-manifest", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(args.candidate, args.historical_manifest)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()

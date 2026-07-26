"""Publish only an audited UTF-8 allowlist to the existing Space."""

from __future__ import annotations

import argparse
from pathlib import Path

from huggingface_hub import CommitOperationAdd, HfApi


REPO_ID = "DineshAI/sW8U2TYDMp"


def load_operations(root: Path, allowlist: Path) -> list[CommitOperationAdd]:
    relative_paths = [
        Path(line.strip())
        for line in allowlist.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert len(relative_paths) == len(set(relative_paths)), "duplicate allowlist path"
    operations = []
    for relative in relative_paths:
        assert not relative.is_absolute() and ".." not in relative.parts
        source = root / relative
        assert source.is_file(), f"missing allowlisted file: {relative}"
        source.read_text(encoding="utf-8")
        operations.append(
            CommitOperationAdd(
                path_in_repo=relative.as_posix(),
                path_or_fileobj=str(source),
            )
        )
    return operations


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("space"))
    parser.add_argument(
        "--allowlist",
        type=Path,
        default=Path("space/release/upload-allowlist.txt"),
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    operations = load_operations(args.root, args.allowlist)
    if args.dry_run:
        print(f"dry_run=true repo={REPO_ID} text_operations={len(operations)}")
        return

    api = HfApi()
    api.repo_info(REPO_ID, repo_type="space")
    result = api.create_commit(
        repo_id=REPO_ID,
        repo_type="space",
        operations=operations,
        commit_message="Publish claim-level certificates and visible evidence",
    )
    print(f"repo={REPO_ID}")
    print(f"commit_oid={result.oid}")
    print(f"commit_url={result.commit_url}")


if __name__ == "__main__":
    main()

"""Build the exact UTF-8 Space upload allowlist and SHA-256 manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path("space")
ALLOWLIST = Path("release/upload-allowlist.txt")
MANIFEST = Path("release/upload-manifest.sha256")


def is_text(path: Path) -> bool:
    if ".cache" in path.parts:
        return False
    try:
        path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, IsADirectoryError):
        return False
    return True


def main() -> None:
    paths = {
        path.relative_to(ROOT)
        for path in ROOT.rglob("*")
        if path.is_file() and is_text(path)
    }
    paths.update({ALLOWLIST, MANIFEST})
    ordered = sorted(paths, key=lambda path: path.as_posix())
    (ROOT / ALLOWLIST).write_text(
        "".join(f"{path.as_posix()}\n" for path in ordered),
        encoding="utf-8",
    )

    manifest_lines = []
    for relative in ordered:
        if relative == MANIFEST:
            continue
        payload = (ROOT / relative).read_bytes()
        manifest_lines.append(
            f"{hashlib.sha256(payload).hexdigest()}  {relative.as_posix()}\n"
        )
    (ROOT / MANIFEST).write_text("".join(manifest_lines), encoding="utf-8")

    print(
        f"text_upload_files={len(ordered)} "
        f"manifest_entries={len(manifest_lines)} "
        "manifest_self_excluded=true"
    )


if __name__ == "__main__":
    main()

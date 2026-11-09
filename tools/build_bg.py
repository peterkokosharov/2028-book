#!/usr/bin/env python3
"""Build the Bulgarian reader edition of "2028": one HTML page + a Kindle-ready EPUB 3.

Python 3.12 standard library only.  Usage:  python3 -I tools/build_bg.py [out_dir]
Reads source-bg/[0-9]*-bg-*.md and writes index.bg.html and 2028.bg.epub at the repository
root (or out_dir). It reuses the converter and writers of tools/build_en.py, so both editions
look the same. The build is deterministic: the same sources give byte-identical files.
"""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

sys.dont_write_bytecode = True  # keep tools/ free of __pycache__
_spec = importlib.util.spec_from_file_location("build_en", HERE / "build_en.py")
en = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(en)

EDITION_DATE = (2026, 11, 2, 0, 0, 0)  # dcterms:modified and zip entry times; bump when the text changes
EDITION = {
    "lang": "bg",
    "contents": "Съдържание",
    "html": "index.bg.html",
    "epub": "2028.bg.epub",
    "uid": "2028-bg-peter-kokosharov",
    "date": EDITION_DATE,
    "switch": ("index.html", "en", "English"),  # link to the other language edition
}


def find_source() -> Path:
    p = ROOT / "source-bg"
    if p.is_dir() and any(p.glob("[0-9]*-bg-*.md")):
        return p
    sys.exit("Bulgarian chapters not found (source-bg/)")


def load_chapters(src: Path):
    """Only numbered *-bg-* chapters; work files (names, translator notes) never match."""
    chapters = []
    for f in sorted(src.glob("[0-9]*-bg-*.md")):
        md = en.strip_comments(f.read_text(encoding="utf-8"))
        body, head = en.convert(md)
        chapters.append({"id": f.stem, "title": head or f.stem, "body": body, "md": md,
                         "is_title": f.stem.startswith("00-bg-title")})
    return chapters


def main():
    out = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
    chapters = load_chapters(find_source())
    out.mkdir(parents=True, exist_ok=True)
    en.build_html(chapters, out, EDITION)
    en.build_epub(chapters, out, EDITION)
    print("chapters: %d, words: %d, out: %s" % (len(chapters), en.words(chapters), out))


if __name__ == "__main__":
    main()

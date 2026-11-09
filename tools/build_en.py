#!/usr/bin/env python3
"""Build the English reader edition of "2028": one HTML page + a Kindle-ready EPUB 3.

Python 3.12 standard library only.  Usage:  python3 -I tools/build_en.py [out_dir]
Reads source/*.md and writes index.html and 2028.epub at the repository root (or out_dir).
The build is deterministic: the same sources give byte-identical files.
"""
import datetime
import html
import re
import sys
import uuid
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
AUTHOR = "Peter Kokosharov"
RIGHTS = "CC BY-NC-SA 4.0"
EXCLUDE = {"92-thanks.md"}  # thanks stay in the repo, not in the published book
EDITION_DATE = (2026, 10, 30, 0, 0, 0)  # dcterms:modified and zip entry times; bump when the text changes

# One edition = one language; tools/build_bg.py reuses this module with its own EDITION.
EDITION = {
    "lang": "en",
    "contents": "Contents",
    "html": "index.html",
    "epub": "2028.epub",
    "uid": "2028-en-peter-kokosharov",
    "date": EDITION_DATE,
    "switch": ("index.bg.html", "bg", "Български"),  # link to the other language edition
}

CSS = """\
body { font-family: Georgia, "Times New Roman", serif; line-height: 1.6; margin: 0 5%; }
h1, h2, h3, h4 { font-family: Georgia, serif; line-height: 1.25; }
h1 { text-align: center; margin: 2em 0 1em; }
h2 { margin: 1.8em 0 0.8em; }
p { margin: 0 0 0.9em 0; text-align: justify; }
blockquote { margin: 1em 1.5em; font-style: italic; }
pre { white-space: pre-wrap; font-size: 0.85em; background: #f3f3f3; padding: 0.6em; }
code { font-family: monospace; font-size: 0.9em; }
.scene { text-align: center; margin: 1.5em 0; letter-spacing: 0.3em; }
.titlepage { text-align: center; margin-top: 25%; }
.titlepage p { text-align: center; }
"""

HTML_CSS = """\
:root { color-scheme: light dark; }
body { font-family: Georgia, "Iowan Old Style", "Times New Roman", serif; line-height: 1.7;
  max-width: 38em; margin: 0 auto; padding: 1.5em 1em 4em; background: #fdfcf9; color: #222; font-size: 1.1rem; }
@media (prefers-color-scheme: dark) { body { background: #17181a; color: #ddd; }
  pre { background: #24262a; } a { color: #8ab4f8; } }
h1 { text-align: center; margin: 1.5em 0 .5em; }
h2 { margin: 2.2em 0 .8em; line-height: 1.25; }
h3, h4 { line-height: 1.25; }
p { margin: 0 0 1em; }
blockquote { margin: 1em 1.5em; font-style: italic; }
pre { white-space: pre-wrap; background: #f1efe9; padding: .7em; font-size: .85em; }
code { font-family: ui-monospace, Consolas, monospace; font-size: .9em; }
.scene { text-align: center; margin: 1.6em 0; letter-spacing: .3em; }
.titlepage { text-align: center; margin: 3em 0; }
nav ol { list-style: none; padding-left: 0; } nav li { margin: .3em 0; }
section { margin-bottom: 3em; }
"""


def find_source() -> Path:
    p = ROOT / "source"
    if p.is_dir() and any(p.glob("[0-9]*.md")):
        return p
    sys.exit("source chapters not found (source/)")


def inline(text: str) -> str:
    codes = []

    def stash(m):
        codes.append("<code>" + html.escape(m.group(1), quote=False) + "</code>")
        return "\x00%d\x00" % (len(codes) - 1)

    text = re.sub(r"`([^`]+)`", stash, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
                  lambda m: '<a href="%s">%s</a>' % (m.group(2).replace('"', "%22"), m.group(1)), text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    return re.sub("\x00(\\d+)\x00", lambda m: codes[int(m.group(1))], text)


def convert(md: str, shift: int = 0):
    """Markdown -> XHTML-safe body fragment. Returns (html, first_heading)."""
    out, para, first = [], [], None
    lines = md.replace("\r\n", "\n").split("\n")
    i = 0

    def flush():
        if para:
            out.append("<p>" + " ".join(inline(x.strip()) for x in para) + "</p>")
            para.clear()

    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if s.startswith("```"):
            flush()
            buf = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            out.append("<pre>" + html.escape("\n".join(buf), quote=False) + "</pre>")
        elif not s:
            flush()
        elif re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", s):
            flush()
            out.append('<p class="scene">* * *</p>')
        elif re.match(r"#{1,4}\s", s):
            flush()
            m = re.match(r"(#+)\s+(.*?)\s*#*$", s)
            lvl = min(len(m.group(1)) + shift, 4)
            if first is None:
                first = m.group(2)
            out.append("<h%d>%s</h%d>" % (lvl, inline(m.group(2)), lvl))
        elif s.startswith(">"):
            flush()
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            i -= 1
            paras = [p for p in "\n".join(buf).split("\n\n")]
            out.append("<blockquote>" + "".join(
                "<p>" + inline(" ".join(p.split("\n"))) + "</p>" for p in paras if p.strip()) + "</blockquote>")
        elif re.match(r"([-*+])\s+", s) or re.match(r"\d+[.)]\s+", s):
            flush()
            ordered = bool(re.match(r"\d+[.)]\s", s))
            items = []
            while i < len(lines):
                t = lines[i].strip()
                m = re.match(r"(?:[-*+]|\d+[.)])\s+(.*)", t)
                if m and bool(re.match(r"\d", t)) == ordered:
                    items.append(m.group(1))
                elif t and items and lines[i].startswith((" ", "\t")):
                    items[-1] += " " + t
                else:
                    break
                i += 1
            i -= 1
            tag = "ol" if ordered else "ul"
            out.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % inline(x) for x in items), tag))
        else:
            para.append(ln)
        i += 1
    flush()
    return "\n".join(out), first


def strip_comments(md: str) -> str:
    """Drop author HTML comments and collapse the blank-line runs they leave."""
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    return re.sub(r"\n(?:[ \t]*\n){2,}", "\n\n", md)


def is_not_english(name: str) -> bool:
    """The English edition never takes Bulgarian files or a glossary."""
    n = name.lower()
    return "-bg-" in n or ".bg." in n or "glossary" in n


def load_chapters(src: Path):
    chapters = []
    for f in sorted(src.glob("[0-9]*.md")):
        if f.name in EXCLUDE or is_not_english(f.name):
            continue
        md = strip_comments(f.read_text(encoding="utf-8"))
        body, head = convert(md)
        chapters.append({"id": f.stem, "title": head or f.stem, "body": body, "md": md,
                         "is_title": f.stem.startswith("00-title")})
    return chapters


def words(chapters) -> int:
    return sum(len(re.findall(r"\w+", c["md"])) for c in chapters)


def chapter_id(n: int) -> str:
    return "ch%02d" % n


def build_html(chapters, out: Path, ed=None):
    ed = ed or EDITION
    title = chapters[0]["title"]
    toc, secs = [], []
    for n, c in enumerate(chapters):
        if c["is_title"]:
            secs.append('<section class="titlepage" id="%s">\n%s\n</section>' % (chapter_id(n), c["body"]))
            continue
        toc.append('<li><a href="#%s">%s</a></li>' % (chapter_id(n), html.escape(c["title"], quote=False)))
        secs.append('<section id="%s">\n%s\n</section>' % (chapter_id(n), c["body"]))
    # title page is first; insert TOC after it
    href, hlang, label = ed["switch"]
    switch = ('<p style="text-align: right; margin: 0; font-size: .9em;">'
              '<a href="%s" hreflang="%s" lang="%s">%s</a></p>' % (href, hlang, hlang, label))
    page = ('<!DOCTYPE html>\n<html lang="%s">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>%s</title>\n<style>\n%s</style>\n</head>\n<body>\n%s\n%s\n'
            '<nav id="toc"><h2>%s</h2>\n<ol>\n%s\n</ol></nav>\n%s\n</body>\n</html>\n'
            % (ed["lang"], html.escape(title, quote=False), HTML_CSS, switch, secs[0], ed["contents"],
               "\n".join(toc), "\n".join(secs[1:])))
    (out / ed["html"]).write_text(page, encoding="utf-8", newline="\n")


XHTML = ('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
         '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" '
         'xml:lang="{lang}" lang="{lang}">\n<head><meta charset="utf-8"/><title>%s</title>'
         '<link rel="stylesheet" type="text/css" href="style.css"/></head>\n<body>\n%s\n</body>\n</html>\n')


def build_epub(chapters, out: Path, ed=None):
    ed = ed or EDITION
    title = chapters[0]["title"]
    lang, date = ed["lang"], ed["date"]
    xhtml = XHTML.replace("{lang}", lang)
    uid = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, ed["uid"]))
    now = datetime.datetime(*date).strftime("%Y-%m-%dT%H:%M:%SZ")
    esc = lambda s: html.escape(s, quote=True)
    files, manifest, spine, navli = {}, [], [], []
    for n, c in enumerate(chapters):
        fid = chapter_id(n)
        fn = fid + ".xhtml"
        body = c["body"]
        if c["is_title"]:
            body = '<div class="titlepage">\n%s\n</div>' % body
        else:
            body = '<section epub:type="chapter">\n%s\n</section>' % body
        files["OEBPS/" + fn] = xhtml % (esc(c["title"]), body)
        manifest.append('<item id="%s" href="%s" media-type="application/xhtml+xml"/>' % (fid, fn))
        spine.append('<itemref idref="%s"/>' % fid)
        if not c["is_title"]:
            navli.append('<li><a href="%s">%s</a></li>' % (fn, esc(c["title"])))
    nav = xhtml % (ed["contents"], '<nav epub:type="toc" id="toc"><h1>%s</h1>\n<ol>\n%s\n</ol></nav>'
                   % (ed["contents"], "\n".join(navli)))
    files["OEBPS/nav.xhtml"] = nav
    files["OEBPS/style.css"] = CSS
    opf = ('<?xml version="1.0" encoding="utf-8"?>\n'
           '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="%s">\n'
           '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
           '<dc:identifier id="bookid">%s</dc:identifier>\n<dc:title>%s</dc:title>\n'
           '<dc:language>%s</dc:language>\n<dc:creator>%s</dc:creator>\n<dc:rights>%s</dc:rights>\n'
           '<meta property="dcterms:modified">%s</meta>\n</metadata>\n<manifest>\n'
           '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>\n'
           '<item id="css" href="style.css" media-type="text/css"/>\n%s\n</manifest>\n'
           '<spine>\n%s\n</spine>\n</package>\n'
           % (lang, uid, esc(title), lang, AUTHOR, RIGHTS, now, "\n".join(manifest), "\n".join(spine)))
    files["OEBPS/content.opf"] = opf
    container = ('<?xml version="1.0" encoding="utf-8"?>\n'
                 '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n'
                 '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>'
                 '</rootfiles>\n</container>\n')
    with zipfile.ZipFile(out / ed["epub"], "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype", date), "application/epub+zip",
                   compress_type=zipfile.ZIP_STORED)
        for name, data in [("META-INF/container.xml", container)] + list(files.items()):
            info = zipfile.ZipInfo(name, date)
            info.external_attr = 0o644 << 16
            z.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED)


def main():
    out = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
    chapters = load_chapters(find_source())
    out.mkdir(parents=True, exist_ok=True)
    build_html(chapters, out)
    build_epub(chapters, out)
    print("chapters: %d, words: %d, out: %s" % (len(chapters), words(chapters), out))


if __name__ == "__main__":
    main()

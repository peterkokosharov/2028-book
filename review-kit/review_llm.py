#!/usr/bin/env python3
"""Send the novel "2028" to a language model with the fixed prompt from PROMPT.md and save the review.

Python 3.12+, standard library only. API keys are read only from environment variables, never from the command line.

  python review_llm.py --dry-run                                    size check, sends nothing
  python review_llm.py --provider ollama --model <name>              local model
  python review_llm.py --provider openrouter --model <id> [BOOK]     needs OPENROUTER_API_KEY
  python review_llm.py --write-parts 6                               text files to paste into a chat, in 6 parts

BOOK is 2028.html or index.html (default: ../2028.html, then ../index.html, then ./index.html),
a .md or .txt file, or a folder of .md chapter files.
Providers: grok, nvidia, openrouter, gemini, anthropic, ollama, lmstudio, litellm,
or any OpenAI-compatible host with --base-url (and --key-env if it needs a key).

Part of the "2028" review kit. License: CC BY-NC-SA 4.0, the same as the book (see ../LICENSE).
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROMPT_FILE = HERE / "PROMPT.md"
DEFAULT_BOOK = HERE.parent / "2028.html"
DEFAULT_OUT = HERE / "results"
DEFAULT_MAX_CHARS = 600_000

# name -> (kind, base url, env var holding the key or None)
PRESETS = {
    "grok": ("openai", "https://api.x.ai/v1", "XAI_API_KEY"),
    "nvidia": ("openai", "https://integrate.api.nvidia.com/v1", "NVIDIA_API_KEY"),
    "openrouter": ("openai", "https://openrouter.ai/api/v1", "OPENROUTER_API_KEY"),
    "gemini": ("openai", "https://generativelanguage.googleapis.com/v1beta/openai", "GEMINI_API_KEY"),
    "anthropic": ("anthropic", "https://api.anthropic.com/v1", "ANTHROPIC_API_KEY"),
    "ollama": ("ollama", "http://localhost:11434/api", None),
    "lmstudio": ("openai", "http://localhost:1234/v1", None),
    "litellm": ("openai", "http://localhost:4000/v1", "LITELLM_API_KEY"),
}
KEY_OPTIONAL = {"litellm"}  # a local proxy may run without a key
LOCAL = {"ollama", "lmstudio", "litellm"}
USER_AGENT = "2028-review-kit/1.0"

OPENING = """I am going to send you a short novel in {n} parts, one part per message, in reading order.

After each part, reply with only "Received part K of {n}" (with K the part number) and nothing else. Do not
summarise, comment or judge yet.

After part {n} I will send the questions. Only then judge the novel as a whole.

Reply now with only "Ready".
"""
FINAL = "That was the last part.\n\n"


class ApiError(Exception):
    pass


def load_prompt(path: Path = PROMPT_FILE) -> str:
    """The fixed prompt: the first fenced block after the '## The prompt' heading of PROMPT.md."""
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^## The prompt\b.*?^```[^\n]*\n(.*?)^```", text, flags=re.S | re.M)
    if not m:
        raise SystemExit(f"{path.name}: prompt block not found")
    return m.group(1).rstrip("\n") + "\n"


class _Text(HTMLParser):
    """Visible text of the book; drops head, nav, style/script (sections are collected separately)."""

    BLOCK = {"p", "h1", "h2", "h3", "h4", "li", "blockquote", "pre", "div", "br", "tr"}
    SKIP = ("head", "style", "script", "nav")

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.sections: list[list[str]] = []
        self.skip = 0
        self.cur: list[str] | None = None

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        elif tag == "section":
            self.cur = []
        if tag in self.BLOCK and self.cur is not None and not self.skip:
            self.cur.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip = max(0, self.skip - 1)
        elif tag == "section" and self.cur is not None:
            self.sections.append(self.cur)
            self.cur = None
        if tag in self.BLOCK and self.cur is not None and not self.skip:
            self.cur.append("\n")

    def handle_data(self, data):
        if self.cur is not None and not self.skip:
            self.cur.append(data)


def html_to_text(html: str) -> str:
    """Plain text of the book, without the section whose title is 'Reviews' (the reader reads blind)."""
    p = _Text()
    p.feed(html)
    parts = []
    for sec in p.sections:
        text = re.sub(r"[ \t]+\n", "\n", "".join(sec))
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        if text.split("\n", 1)[0].strip().lower() == "reviews":
            continue
        parts.append(text)
    return "\n\n".join(parts) + "\n"


def md_book(folder: Path) -> str:
    """All .md chapter files in name order, without reviews and old bg-* drafts."""
    files = sorted(f for f in folder.glob("*.md")
                   if not f.name.startswith("bg-") and "review" not in f.name.lower()
                   and f.name.lower() != "readme.md")
    if not files:
        raise SystemExit(f"no .md chapter files in {folder}")
    return "\n\n".join(f.read_text(encoding="utf-8").strip() for f in files) + "\n"


def default_books() -> list[Path]:
    """Tried in order when no book is given: the release folder, then the web repo, then the current folder."""
    return [DEFAULT_BOOK, HERE.parent / "index.html", Path.cwd() / "index.html"]


def load_book(path: Path) -> tuple[str, str]:
    """Return (text, short description of what was read)."""
    if path.is_dir():
        return md_book(path), f"{path.name}/*.md (reviews left out)"
    if not path.is_file():
        raise SystemExit(f"book not found: {path}. Give the path to 2028.html as an argument.")
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".html", ".htm"):
        return html_to_text(raw), f"{path.name} (text, Reviews section left out)"
    return raw.rstrip("\n") + "\n", path.name


def fingerprint(book: str) -> str:
    return hashlib.sha256(book.encode("utf-8")).hexdigest()[:12]


def build_message(book: str, prompt: str) -> str:
    return book.rstrip("\n") + "\n\n" + prompt


def split_book(book: str, n: int) -> list[str]:
    """Cut the book into n parts of about equal size, only between paragraphs."""
    paras = [p for p in re.split(r"\n{2,}", book.strip()) if p.strip()]
    n = max(1, min(n, len(paras)))
    target = len(book) / n
    parts, cur, size = [], [], 0
    for i, p in enumerate(paras):
        left_paras, left_parts = len(paras) - i, n - len(parts)
        if cur and (size >= target or left_paras < left_parts) and len(parts) < n - 1:
            parts.append("\n\n".join(cur))
            cur, size = [], 0
        cur.append(p)
        size += len(p) + 2
    parts.append("\n\n".join(cur))
    return [p + "\n" for p in parts]


def write_parts(book: str, prompt: str, n: int, out: Path) -> list[Path]:
    """Files to paste into a chat in name order. n == 1: one file with the book and the prompt."""
    out.mkdir(parents=True, exist_ok=True)
    if n <= 1:
        files = {"01-book-and-prompt.txt": build_message(book, prompt)}
    else:
        parts = split_book(book, n)
        n = len(parts)
        files = {"00-start.txt": OPENING.format(n=n)}
        for k, text in enumerate(parts, 1):
            files[f"{k:02d}-part.txt"] = f"Part {k} of {n}:\n\n{text}"
        files[f"{n + 1:02d}-questions.txt"] = FINAL + prompt
    paths = []
    for name, text in files.items():
        path = out / name
        path.write_text(text, encoding="utf-8", newline="\n")
        paths.append(path)
    return paths


def resolve(provider: str, base_url: str | None, key_env: str | None):
    kind, url, env = PRESETS.get(provider, ("openai", None, None))
    if provider not in PRESETS and not base_url:
        raise SystemExit(f"unknown provider {provider!r}; use one of {', '.join(PRESETS)} or give --base-url")
    return kind, (base_url or url).rstrip("/"), (key_env or env)


def http_post(url: str, headers: dict, body: bytes, timeout: float) -> tuple[int, bytes]:
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except TimeoutError as e:
        raise ApiError(f"timeout after {timeout:.0f}s") from e
    except ValueError:  # e.g. invalid header value; never show the exception text (it may hold the key)
        raise ApiError("request could not be built (invalid header or URL)") from None
    except urllib.error.URLError as e:
        if isinstance(e.reason, TimeoutError):
            raise ApiError(f"timeout after {timeout:.0f}s") from e
        raise ApiError(f"connection failed: {e.reason}") from e
    except OSError as e:
        raise ApiError(f"connection failed: {type(e).__name__}") from None


def build_request(kind: str, base: str, key: str | None, model: str, message: str, max_tokens: int,
                  num_ctx: int = 0):
    headers = {"content-type": "application/json", "user-agent": USER_AGENT}
    messages = [{"role": "user", "content": message}]
    if kind == "anthropic":
        url = base + "/messages"
        headers["anthropic-version"] = "2023-06-01"
        if key:
            headers["x-api-key"] = key
        payload = {"model": model, "max_tokens": max_tokens, "messages": messages}
    elif kind == "ollama":  # native API: the only way to set the context size per request
        url = base + "/chat"
        payload = {"model": model, "messages": messages, "stream": False,
                   "options": {"num_ctx": num_ctx, "num_predict": max_tokens}}
    else:
        url = base + "/chat/completions"
        if key:
            headers["authorization"] = "Bearer " + key
        payload = {"model": model, "max_tokens": max_tokens, "messages": messages}
    return url, headers, json.dumps(payload).encode("utf-8")


def parse_answer(kind: str, data: dict) -> tuple[str, str]:
    """Return (answer text, stop reason). Empty answers raise ApiError."""
    try:
        if kind == "anthropic":
            text = "".join(b.get("text") or "" for b in data["content"] if b.get("type") == "text")
            stop = data.get("stop_reason") or "unknown"
        elif kind == "ollama":
            text = data["message"].get("content") or ""
            stop = data.get("done_reason") or "unknown"
        else:
            choice = data["choices"][0]
            text = choice["message"].get("content") or ""
            stop = choice.get("finish_reason") or "unknown"
    except (KeyError, IndexError, TypeError, AttributeError) as e:
        raise ApiError("unexpected response shape") from e
    if not isinstance(text, str) or not text.strip():
        raise ApiError(f"the model returned no text (stop reason: {stop}); "
                       "a reasoning model may need a higher --max-tokens")
    return text, stop


def is_truncated(stop: str) -> bool:
    return stop in ("length", "max_tokens")


def ask(kind, base, key, model, message, max_tokens, timeout, num_ctx=0) -> tuple[str, str]:
    url, headers, body = build_request(kind, base, key, model, message, max_tokens, num_ctx)
    status, raw = http_post(url, headers, body, timeout)
    if status != 200:
        detail = raw.decode("utf-8", "replace")[:500]
        if key:
            detail = detail.replace(key, "***")
        raise ApiError(f"HTTP {status}: {detail}")
    try:
        return parse_answer(kind, json.loads(raw))
    except json.JSONDecodeError as e:
        raise ApiError("HTTP 200 but the body is not JSON") from e


def auto_num_ctx(message: str, max_tokens: int) -> int:
    """Context size for a local model: the input (generous estimate, chars/3) plus the answer, in 1024 steps."""
    need = len(message) // 3 + max_tokens
    return -(-need // 1024) * 1024


def safe(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "-", s).strip("-") or "x"


def render(model, provider, date, source, fp, chars, answer, stop="unknown") -> str:
    """Result file: the header from PROMPT.md, filled in, then the answer exactly as it came."""
    return (
        "```\n"
        f"Model:          {model}\n"
        f"Provider:       {provider}\n"
        "Interface:      API (review_llm.py)\n"
        "Thinking mode:  unknown (provider default)\n"
        f"Date:           {date}\n"
        f"Edition:        {source}; text sha256 {fp}\n"
        f"Split:          no (whole book in one message, {chars} chars)\n"
        "Read blind:     yes\n"
        "Context:        clean (fresh API call)\n"
        f"Stop reason:    {stop}{' - TRUNCATED, the answer is incomplete' if is_truncated(stop) else ''}\n"
        "```\n\n" + answer.strip("\n") + "\n"
    )


def unique_path(out: Path, stem: str) -> Path:
    """out/stem.md, or out/stem-2.md, -3 ... never an existing file."""
    n = 1
    while True:
        path = out / (f"{stem}.md" if n == 1 else f"{stem}-{n}.md")
        if not path.exists():
            return path
        n += 1


def main(argv=None, env=None, today=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    env = os.environ if env is None else env
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("book", nargs="?", type=Path, default=None,
                    help="2028.html, a .md/.txt file, or a folder of .md chapters"
                         " (default: ../2028.html, then ../index.html, then ./index.html)")
    ap.add_argument("--provider", help="see the list above; not needed with --dry-run or --write-parts")
    ap.add_argument("--model", help="model name or id at that provider")
    ap.add_argument("--out", type=Path, help="folder for the result or the parts (default: results/ or parts/)")
    ap.add_argument("--base-url", help="any OpenAI-compatible host, e.g. http://localhost:8080/v1")
    ap.add_argument("--key-env", help="name of the environment variable that holds the key")
    ap.add_argument("--max-chars", type=int, default=DEFAULT_MAX_CHARS)
    ap.add_argument("--max-tokens", type=int, default=8000, help="answer limit (default 8000)")
    ap.add_argument("--num-ctx", type=int, default=0, help="Ollama context size (default: enough for the book)")
    ap.add_argument("--timeout", type=float, default=1800)
    ap.add_argument("--dry-run", action="store_true", help="show the size, send nothing")
    ap.add_argument("--write-parts", type=int, metavar="N",
                    help="write the book and the prompt as N text files to paste into a chat; send nothing")
    a = ap.parse_args(argv)

    if a.book is None:
        tried = default_books()
        found = next((p for p in tried if p.is_file()), None)
        if found is None:
            raise SystemExit("book not found; tried: " + ", ".join(str(p) for p in tried)
                             + ". Give the path to 2028.html or index.html as an argument.")
        a.book = found
    book, source = load_book(a.book)
    prompt = load_prompt()
    message = build_message(book, prompt)
    fp = fingerprint(book)

    if a.write_parts is not None:
        out = a.out or (HERE / "parts")
        paths = write_parts(book, prompt, a.write_parts, out)
        print(f"book: {source}; {len(book)} chars; sha256 {fp}")
        print(f"book file: {a.book.resolve()}")
        print(f"wrote {len(paths)} files to {out}; paste them into one fresh chat in name order:")
        for p in paths:
            print(f"  {p.name}  ({len(p.read_text(encoding='utf-8'))} chars)")
        return 0

    if len(book) > a.max_chars:
        print(f"STOP: the book is {len(book)} chars, more than --max-chars {a.max_chars}. "
              "Nothing sent, nothing truncated.", file=sys.stderr)
        return 2

    print(f"book: {source}; {len(book)} chars; sha256 {fp}")
    print(f"book file: {a.book.resolve()}")
    print(f"request: {len(message.encode('utf-8'))} bytes; about {len(message) // 4} tokens (chars/4 estimate) "
          f"plus up to {a.max_tokens} for the answer")
    if a.dry_run:
        print("dry run: nothing sent")
        return 0
    if not a.provider or not a.model:
        ap.error("--provider and --model are needed to send (or use --dry-run / --write-parts)")

    kind, base, key_env = resolve(a.provider, a.base_url, a.key_env)
    num_ctx = a.num_ctx or auto_num_ctx(message, a.max_tokens)
    print(f"provider {a.provider} ({kind}) {base}  model {a.model}"
          + (f"  context {num_ctx}" if kind == "ollama" else ""))
    if a.provider in LOCAL and kind != "ollama":
        print("note: make sure the local model is loaded with a context of at least "
              f"{auto_num_ctx(message, a.max_tokens)} tokens; a runtime that cuts long input silently "
              "would review only part of the book.")

    key = (env.get(key_env) or "").strip() if key_env else ""
    if key and any(ord(c) < 32 or ord(c) == 127 for c in key):
        print(f"error: the key in {key_env} contains control characters; fix the variable", file=sys.stderr)
        return 2
    if key_env and not key and a.provider not in KEY_OPTIONAL:
        print(f"error: environment variable {key_env} is not set", file=sys.stderr)
        return 2
    key = key or None
    print("sending; a long book can take several minutes ...")
    try:
        answer, stop = ask(kind, base, key, a.model, message, a.max_tokens, a.timeout, num_ctx)
    except ApiError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    date = (today or datetime.date.today()).isoformat()
    out = a.out or DEFAULT_OUT
    out.mkdir(parents=True, exist_ok=True)
    path = unique_path(out, f"{date}-{safe(a.provider)}-{safe(a.model)}")
    path.write_text(render(a.model, a.provider, date, source, fp, len(book), answer, stop), encoding="utf-8")
    print(f"saved {path}")
    if is_truncated(stop):
        print(f"WARNING: TRUNCATED - the answer hit the token limit ({stop}); "
              "the file is marked. Run again with a higher --max-tokens.", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())

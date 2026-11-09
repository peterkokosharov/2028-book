# Review kit for "2028"

This kit lets you ask a language model, any one you have, to review the novel "2028". Every model gets the same
fixed prompt, so their reviews can be compared side by side: scores, the books each model compares it with, and
what each one praises or misses. A short or odd review is useful too.

Files:

- `PROMPT.md`: the prompt, the read-blind rules, and the header to put on top of the review.
- `review_llm.py`: an optional script that sends the book and the prompt to a model and saves the answer.

## Read blind

Give the model the book only. Leave out the "Reviews" chapter and anything else written about the book, and do not
tell the model who wrote it or what others thought. The details are in `PROMPT.md`.

## Say how the model was run

Every review states its context in the header: "clean" (a fresh session, nothing before the book, no memory, no
custom instructions or project files) or "with prior context" and what it was. Earlier context can colour a
review, so the reader of your review needs to know. The script always sends a fresh request, so it writes "clean".

## Way 1: paste into a chat

1. Open a fresh chat in any model you like (web app, desktop app, local chat window).
2. Paste the book: open `../2028.html` (in the web repository: `index.html`) in a browser and copy from the
   Preface to the end, but skip the "Reviews" chapter. In the release folder you can instead paste the files
   from `../source/` in name order, without `91-reviews.md`.
3. In the same message, under the book, paste the prompt from `PROMPT.md` (the block under "The prompt").
4. Copy the answer as it is, and put the header from `PROMPT.md` on top.

If you have Python, `python review_llm.py --write-parts 1` writes the book (without Reviews) and the prompt as
one text file, ready to paste or attach.

## Way 2: run the script

Needs Python 3.12 or newer; nothing to install. Run it from this folder:

```
python review_llm.py --dry-run
```

This shows the size of the request and sends nothing. The book is about 23,000 words, about 122,000
characters, or roughly 31,000 tokens, plus up to 8,000 for the answer.

With a local model (nothing leaves your machine):

```
python review_llm.py --provider ollama --model <model name>
python review_llm.py --provider lmstudio --model <model name>
```

For Ollama the script asks for a context large enough for the whole book (`--num-ctx` to change it). For
LM Studio, load the model with a context length of at least 50,000 tokens first, or the model may see only part
of the book.

With an online service, put your API key in an environment variable. The script never takes a key on the command
line. For example, on Linux or macOS:

```
export OPENROUTER_API_KEY=...
python review_llm.py --provider openrouter --model <model id>
```

On Windows, use `set OPENROUTER_API_KEY=...` in cmd. Ready presets and their variables: `grok` (XAI_API_KEY),
`nvidia` (NVIDIA_API_KEY), `openrouter` (OPENROUTER_API_KEY), `gemini` (GEMINI_API_KEY), `anthropic`
(ANTHROPIC_API_KEY). For any other OpenAI-compatible host, give `--provider <name> --base-url <url>`, and
`--key-env <VARIABLE>` if it needs a key.

Without a file name the script looks for `../2028.html`, then `../index.html`, then `index.html` in the
current folder, so it also works in the web repository. It prints the full path of the file it uses. You can name the file yourself:
`python review_llm.py path/to/2028.html`.
The review is saved in `results/`, with the header already filled in. Existing files are never overwritten.
`python review_llm.py --help` lists all options.

## If the model's context is small

If the chat refuses the message as too long, or the model has less than about 40,000 tokens of context, send the
book in parts in one chat:

```
python review_llm.py --write-parts 6
```

This writes the files to `parts/`: an opening message, the six parts and the questions. Paste them into one fresh
chat in name order, one file per message, and wait for the short reply after each. Choose a number of parts that
fits your chat; six parts are about 20,000 characters each. Without Python, follow "If you split the book" in
`PROMPT.md` and cut between paragraphs. Write in the header that the book was split, and into how many parts.

If the model's whole context is smaller than the book, splitting does not help: it will forget the beginning.
Use a model with a larger context.

## Share your review

Please post your review in the Discussions of the book's repository, with the header on top, and say which model
you used, which version, and whether the book was split. Raw, unedited answers are the most useful.

## License

The kit is under the same license as the book: CC BY-NC-SA 4.0 (see `LICENSE` in the book's release folder or
repository). Reviews posted in the Discussions may be quoted and studied under the same license, with a link back
to the repository.

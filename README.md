# 2028: How to Survive as a Software Developer in the 21st Century

A short novel about working with AI agents, dignity, and doing the work carefully.

A work of fiction. The narrator is not the author. Claude, Claude Code, Opus and Sonnet are trademarks of Anthropic; other model names belong to their owners. No affiliation or endorsement is implied.

Free to read. Not free to sell.

## Read it

Online: **https://peterkokosharov.github.io/2028-book/**

Or open `index.html` in a browser. It is the whole book on one page: a preface, six chapters with the Emil interludes, an afterword, and reviews. For an e-reader, use `2028.epub`; on a Kindle, send it with Send to Kindle.

In Bulgarian (Български): **https://peterkokosharov.github.io/2028-book/index.bg.html**, or `index.bg.html` here; for an e-reader, `2028.bg.epub`.

## Talk about it

Comments, corrections and reviews are welcome in this repository's [Discussions](https://github.com/peterkokosharov/2028-book/discussions); typos can go to Issues.

## Review it with your own model

The [`review-kit/`](review-kit/) folder holds a fixed prompt and a small script, so any language model can review the book the same way; see [`review-kit/README.md`](review-kit/README.md). From this folder, `python review-kit/review_llm.py --dry-run` finds `index.html` by itself and checks the size first; you can also name the file: `python review-kit/review_llm.py index.html`. Post the review in this repository's Discussions, name the model, and say whether the run was clean (a fresh session, nothing before the book) or had prior context.

## Rebuild

`python3 tools/build_en.py` writes `index.html` and `2028.epub` from `source/` (Python standard library only). `python3 tools/build_bg.py` writes `index.bg.html` and `2028.bg.epub` from `source-bg/`.

## License

Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International ([CC BY-NC-SA 4.0](LICENSE)). You may read and share this work freely. You may translate and adapt it, with attribution and under the same licence. You may not sell it or use it commercially without the author's written permission.

(c) Peter Kokosharov

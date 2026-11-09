# The review prompt

One fixed prompt for every model, so that reviews from different models can be compared.

## Read blind

- Give the model the book only: `2028.html` (`index.html` in the web repository) or, in the release folder,
  the files in `source/`. Leave out the "Reviews" chapter (`source/91-reviews.md`), the book's README,
  the Discussions and anything else written about the book.
  `review_llm.py` leaves the Reviews chapter out by itself.
- Use a fresh chat with nothing earlier in it. Do not say who wrote the book, what other models scored, or what
  you think of it.
- If the model asks you something, answer only: "Judge from the text only."
- Copy the prompt below exactly as it is. Do not add hints, summaries or your own opinion.

## The prompt

Paste the book first, then this block, unchanged.

```
You have just read a short novel, "2028: How to Survive as a Software Developer in the 21st Century".
Review it as an honest, experienced reader and critic. Judge the book only, from the text only. Do not flatter.
If parts of the book were not visible to you, say which ones before you answer.
Answer in English, as a numbered list, in this order, in about 600 to 900 words in all:

1. Overall score out of 10, with one decimal (for example 6.5/10).
2. Sub-scores out of 10, one decimal each: plot, characters, style, structure, emotional effect, readability.
3. Comparable books: three to five real, published books (title, author, year) at about the same level
   and closest in kind. One line each on why.
4. One published book clearly below this one and one clearly above it (title, author, year),
   one line each on why.
5. The three strongest points, each with a concrete place in the text (chapter and scene).
6. The three weakest points, each with a concrete place in the text.
7. The single change that would raise the score the most: where, what to change, and about how much
   it would raise the score.
8. Plot: was anything confusing, hard to believe or left hanging? Say where.
9. Characters: which character is the most alive, and which the least? Why?
10. Readability: where did the pace drag, or where did you have to read a passage twice? Say where.
11. Would a general reader finish this book and recommend it to a friend? Yes or no, and why, in one line.
12. A short review as a reader would post it online: two or three lines, no score.

No introduction and no closing remarks.
```

## If you split the book

When the model or the chat cannot take the whole book in one message, send it in parts in one chat:

1. First this message (put the number of parts in place of N):

   ```
   I am going to send you a short novel in N parts, one part per message, in reading order.

   After each part, reply with only "Received part K of N" (with K the part number) and nothing else. Do not
   summarise, comment or judge yet.

   After part N I will send the questions. Only then judge the novel as a whole.

   Reply now with only "Ready".
   ```

2. Then each part, starting with the line `Part K of N:`. Cut only between paragraphs.
3. After the last part: the line `That was the last part.` and the prompt above, unchanged.

`python review_llm.py --write-parts N` writes all of these messages as ready text files.

## The result header

Put this at the top of every review, filled in. Write "unknown" rather than guess.

```
Model:          <name and exact version, as the app or the API shows it>
Provider:       <company or host; "local" for your own machine>
Interface:      <chat app / API / local runtime, e.g. Ollama or LM Studio>
Thinking mode:  <on / off / unknown>
Date:           <YYYY-MM-DD>
Edition:        <which file you gave the model, e.g. 2028.html from release v1.0, and where you got it>
Split:          <no / yes, into N parts>
Read blind:     <yes / no - what else the model saw>
Context:        <clean / with prior context: what>
```

`Context` is required. "clean" means a fresh session: nothing before the book, no memory, no custom instructions,
no project files. Otherwise write "with prior context" and say what, for example: other texts read or discussed
first, memory or custom instructions on, or an ongoing chat.

Below the header, paste the model's answer exactly as it came, without edits. One model, one run, one review.
A short or odd review is still useful.

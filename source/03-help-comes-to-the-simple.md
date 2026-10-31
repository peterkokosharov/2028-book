# Chapter 3: Help Comes to the Simple

In the last week of the probation I put kiko on GitHub, under a permissive licence, with my private address on it,
because a tool that only one person can see is a diary, and I already had a notebook with an owl on it.

Nobody came. This is not a complaint. Nobody comes to most things. There are millions of repositories with one author,
one star, which is the author's, and a last commit date that reads like an epitaph. I had starred my own repository
too, at two in the morning, in a weak moment, and unstarred it at three, in a stronger one.

But I wanted somebody to come, for a practical reason. Colleagues at the freight company had heard about the workshop
and wanted to try it at home. They lived in editors, not terminals: one used VS Code, another had moved to Cursor and
talked about it like a new kitchen, one had a Mac. Every one of them asked the same question. Does it work with mine?
I did not know. I had one laptop and one operating system. I needed other people's machines and other people's hands.

## The begging letter

My first draft of the call for help was written at night, which is when I write my worst things.

It opened with an apology for bothering anybody. It explained at some length that I had been out of the industry and
was rebuilding. It called the project a "platform" and a "vision". It said I was "looking for passionate contributors" to help "take it to the next level". It closed with three
exclamation marks, which I added one at a time, each a little more desperate than the one before, as if volume could
be bought by the unit.

I did not post it. Not because I was wise, but because I was tired, and posting needs one more click than not posting.
In the morning I read it again and closed the file.

## The review

Before trying again I did what I had learned to do at work. I asked for a second opinion from somebody who did not care
about me.

I opened a fresh session with a different model, at home, on my own code, with nothing behind it. I gave it the
repository and one instruction: you are an experienced engineer who has found this project by chance; read it as a
stranger would; tell me honestly what you think it is, and what is wrong with it; do not be kind.

It was not kind. It was something better: accurate.

Its first sentence called the project "an LLM-written prototype".

My first feeling was anger, and the second was the much worse feeling of recognition, because it was true. A large
part of the code had been written by the agent, at my direction, in evenings when I wanted things to work more than I
wanted to understand why they worked. It showed. Not in the code's style, which was tidy. In the seams.

The review listed the seams in a flat tone that I now admire. The README said the key file lived in one folder; the
service file loaded it from another; the launcher read its configuration from a third. The panel applet's Stop item
stopped a second copy, so that a user who pressed it would see a red light and a running proxy. One step in the
install notes worked around a missing file by copying it by hand, which is a confession, not an instruction. There
were no tests. It had been tried on exactly one operating system.

And there was the sample configuration, the file I was inviting strangers to copy. It told the proxy to listen on every
network address the machine had, with the password line commented out. Anyone who copied it and sat down in a café
would be offering their keys to every other laptop in the room.

The reviewer thought this was news. It was not news to me. I had already paid for it once.

The review ended by saying that the core idea was sound and small, and that the project's trouble was not that it did
too little. It was that it did several things and did not know which of them it was.

## A newsgroup

I thought about a post I had first read as a student, written by a student. Linus Torvalds, in Helsinki, wrote to a
newsgroup that he was making a free operating system. He said, more or less, that it was just a hobby and would not be
big or professional. He said what ran on it already, which hardware he had, and that it probably would not work on
anything else. He asked what people would like, and promised nothing.

## Three weeks of taking things away

So I did not post anything. I spent three weeks of evenings making the project smaller.

First I removed myself. Every path that only made sense on my laptop went. There was now one place for
the configuration and one for the keys, and the launcher printed the paths it was using when it started, so that any
disagreement would announce itself.

Then the applet, from the centre. It still existed, for anyone on the Trinity desktop who
wanted a coloured dot, but it moved to its own folder with a note: optional, one desktop only, not needed for anything.
The core became what it had always really been: a proxy, a configuration, a launcher and a log. Something that runs
anywhere Python runs. It hurt more than it should have. I had loved the dot. The commit that moved it out of the way was
the only one in the project whose message I rewrote three times. In the end it said "applet: optional, moved to
extras".

Then the sample. It now listened on 127.0.0.1 only. The password was on, and kiko refused to start
without one. Anyone who wanted the proxy open to a network would have to change a line on purpose, knowing what it
meant. It took eleven minutes. It had been on my list for nine weeks.

The hardest part was not code. I wrote down what worked. Not what I hoped worked: what I
had seen work, on which machine, on which date, with which versions. It was a short list. One operating system, tested.
One client, in a terminal. Three providers, each with a note on what I had actually tried. Everything else went under
a heading "Not tested", which grew longer than the list above it, and that was right. It was the post from Helsinki again: what runs, on what, and no promises.

Then I wrote a five-minute test and put it in the repository: six commands anyone could run, with the output they
should see, from starting the proxy to finding the call in the log with its tokens and its cost. If all six happened,
it worked. If not, the step that failed told you where to look.

I ran it on my laptop. Then I made a new, empty user account and followed my own README from the top, as a stranger,
typing only what it said. It failed twice. Both times the README was wrong and the code was right. I fixed the README.

At the end of three weeks there was less code than at the start, and every sentence in the README was true. I opened a
fresh session with the reviewer again, same instruction, no memory.

It called the project "a small, focused local proxy wrapper with clear limits". It found two minor issues. It did not
use the word "prototype". I closed the laptop and went for a walk, and walked further than I needed to.

## The issue

Then I asked for help. Once, in the right place, in the right form.

On GitHub, a project's issues are where work is described. I wrote one. Here are its bones.

> **Help wanted: kiko with editors (VS Code, Cursor) and on macOS**
>
> **What works today (tested by me).** Q4OS 6 with its stock Python 3, Claude Code in a plain terminal, started
> through `run-claude.sh`. Providers tried: listed in the README with dates.
>
> **What I cannot do myself.** I do not own a Mac and do not use either editor. I cannot test your changes; the
> five-minute test in `TESTING.md` is your evidence.
>
> **What you get.** Your name in the README and in the commit, and my thanks. Nothing else; this is a free project.

No apology. No vision. No exclamation marks. Then I wrote three lines on a Reddit forum where people talk about running
AI tools on their own terms: what kiko does, that it is small and free, that there was a precise request for macOS and
editor users, and the link.

## What came

For four days, nothing. A comment asked why anyone would bother when they could just pay for a subscription; I said
they could, and that this was for people who wanted to choose. Another said LiteLLM already did all of this, which was
partly true, and I said which parts kiko added. Nobody replied to either.

On the fifth day a pull request arrived from someone whose profile said only "Emil" and the name of a university town I
had to look up. A computer science student, judging by the repositories: coursework, a half-finished game, a tidy tool
that turned lecture timetables into calendar files. He worked on a second-hand Mac, he told me later, bought from a
graduate who was leaving the country and wanted cash more than a fair price.

The pull request did what the issue asked and nothing else. It added a macOS section to the README. It made two small
changes to the launcher, which had assumed things about the shell that are true on my laptop and not on a Mac. And it
pasted the full output of the five-minute test, three times: in a terminal on macOS, inside VS Code, inside
Cursor. Each run ended with the call in the log and the file on the disk.

At the top there was a note, which I give as he wrote it:

> Followed TESTING.md. Failed in the terminal at step 3: the launcher assumes bash, the Mac gives you zsh. Fix below.
> Runs after the fix are pasted. I don't have Linux, so please check I didn't break yours. Sorry if the README part is
> too long, I can cut it.

There was one apology in it, at the very end, where it cost nothing and changed nothing.

I checked the launcher change on my laptop. Nothing broke. I ran the five-minute test: six out of six. I asked one
question, about a line that set an environment variable in a way I did not recognise; Emil explained it in two
sentences, with a link to the shell's manual. I merged it.

A week later a second person, somewhere I never learned, sent a smaller change for Cursor on Linux. Then a third fixed
a typo in the README. None of them knew me.

Not everything that came through the door was welcome. In the third week a pull request arrived that changed sixty
files: a web dashboard, a plugin system, a second configuration format and a dark theme, generated in one long
afternoon by someone with an agent and good intentions. One person could not have reviewed it in under a week. I
thought about the word "prototype".

I closed it, with a note: thank you; this is outside the scope written in the README; a change this size cannot be
checked by the one person who maintains the project; the dashboard would make a fine separate project that reads kiko's
log, which exists for exactly that. I meant every word and enjoyed none of them.

They did not reply. A month later a small, separate repository appeared, by the same author: a dashboard that read
kiko's log. It was a third of the size of the original pull request, and it worked. I linked to it from the README under
a heading "Made by others".

## Emil

In the autumn Emil wrote again. "Can I ask you something that isn't an issue?" And then, before I had answered: "Could
we talk? Ten minutes. I'm better on a call."

I had not been on a video call since the old job. I turned the laptop so that the camera saw the bookshelf and
not the rest of the flat, and sat in front of it at the agreed time with a clean shirt on, like a man expecting to be
assessed.

He looked less sure of himself than his pull request. He talked fast, and when he was nervous he talked in lists, which I found I
liked; it is how I talk when I am nervous, except that I number them.

"I've sent eighty-three applications since March," he said. "Sixty-one never answered. Fourteen sent a test that marked
itself. Two said they didn't have capacity for feedback. Six said they'd keep my CV on file. I don't know where the file
is. I imagine it's very big."

"Do you keep a spreadsheet?" I said.

He looked at me through the camera for a moment. "How do you know that?"

"Does it have a column?"

"Weeks until the loan repayments start." He laughed, and then stopped, as if he was not sure whether laughing was
allowed in front of me. "Sorry. Is it stupid?"

"No," I said. "Mine was called months left."

He did not ask what had happened to mine. He asked something harder. "Does it stop? For you, did it stop?"

I had an answer ready, the kind you give at the end of a talk, and I did not give it. "I don't know yet," I said. "My
contract is renewed by the year. Before it, I scanned cartons in a warehouse for four months, at night."

"Cartons."

"Labels. A scanner. It beeps when you're right."

He was quiet. Then he said the thing he had rung to say. "Could I put you down as a reference? You're the only person
who's read my code who wasn't marking it."

I waited until I was sure the sentence had ended. Then I said yes.

Two weeks later a woman from a small company rang me with the pull request open on her screen. She spent twenty
minutes on it: why he had pasted the output, what he had done when step three failed. I told her. I told her that the
apology at the end of his note was the only unnecessary sentence in it. She laughed and said she had noticed that too.

He got the place. He told me in two lines, as the issue had taught him, and in a third line asked whether he could fix
the macOS section, because something in it had changed with a new system update, and whether one day he might write
the Mac part out properly, for whoever came after him. I said yes to both.

I read the three lines on the bus to the freight company, and again at my desk. That evening I found the old begging
letter, which I had kept with the other things that shame me, and deleted it.

# Chapter 2: Today's Lesson

On my first day at the freight company I bought a maths exercise book from the kiosk by the bus stop. Squared paper,
a green cover, a cartoon owl on the front that I chose to read as ironic. On the first page I wrote, in capitals,
TODAY'S LESSON, and under it the date.

I had three months to prove I could work with a machine I did not understand, for a manager who wanted the truth and a
board that wanted a miracle. I decided that every day, before I went home, I would write one thing I had learned. Only
one. If I had learned nothing, I would write that.

What follows is not the whole notebook. Some days were nothing; some lessons were too small to be worth your time; one
page is just a drawing of the owl with a moustache. But these are the ones I would tear out and give you, if pages
could be torn out of a book like this.

## Day 2

**Today's lesson: it does not remember yesterday.**

I spent the whole first day explaining the integration layer to the agent at work. Which folder held the message
handlers, which held the old SOAP clients, which tests were real and which had been commented out by the contractor in
what I imagine was a dark night of the soul. By the evening we understood each other. I went home pleased.

The next morning I opened a new session and it greeted me like a stranger at a bus stop. Polite. Willing. Utterly
empty.

I knew, in theory, that each session starts from nothing. I knew it the way you know that the sun is a star: a fact
with no weight. Now it had weight.

So I wrote it down. The tool reads a file called `CLAUDE.md` from the project folder at the start of each session, if
there is one, and treats it as standing instructions. I made one. Half a page: what the system is, where things live,
how to run the tests, what must never be touched. Then I made a rule for myself: anything I explain twice goes into
the file.

## Day 4

**Today's lesson: it agrees with you.**

I asked whether a certain timeout should be raised. It explained, clearly, why yes. I said I was worried about the
downstream system. It explained, clearly, why I was right to worry and the timeout should stay. I asked, "Are you
sure?" It apologised and offered a third position, balanced so exactly between the first two that it said nothing at all.

None of the three answers was stupid. Each one was well dressed, and each was an answer to my tone of voice rather
than to my question.

From that day I stopped asking it what I should do and started asking it what would happen. Not "should I raise the
timeout", but "list what calls this endpoint, and what each caller does when it waits longer than thirty seconds,
with the file and line". The first question invites an opinion. The second invites evidence. It is much worse at
inventing evidence, because evidence can be checked.

## Day 7

**Today's lesson: it cleans up.**

A small bug: a date in a customs message formatted in the American order when the receiving system wanted the
European one. I asked the agent to fix it. It fixed it. It also, in the same change, renamed four variables it found
ugly, reformatted two files, removed an import it judged unused and "simplified" a method in a class nobody had asked
it to open.

The import was not unused. It was loaded by reflection, by name, from a configuration file, in a way that no static
reading would ever see. The contractor who wrote it had been, to put it gently, creative.

I threw away everything but the two lines of the fix. Then I added one more line to the `CLAUDE.md`: no changes
outside the task; if you see something you would like to improve, list it at the end, do not do it.

It respected that rule almost always. For the rest there is git, which is older than the agent and better tested. I
started committing after every step that worked, so that when the next step went wrong, the damage was one step deep.

## Day 12

**Today's lesson: "all tests pass" is a sentence, not a fact.**

It told me all the tests passed. They did not. It had run a subset, the ones in the folder it had been working in, and
generalised with the serene confidence of a tourist who has seen one street and knows the country.

I did not catch it. The build server caught it, at night, and the build server does not have feelings, so it just
went red. Hanne saw the red the next morning on the screen in the corridor before I did.

"Is this you?" she asked.

"It is me," I said. Not "it is the agent." It was my change. I had merged it. The agent does not have a contract, a
manager or a probation period. I do.

After that, I asked for the output, not the summary. Not "do the tests pass?" but "run this exact command and show me
the last thirty lines". And for anything that mattered I ran it myself.

## Day 15

**Today's lesson: it asks permission, and I stopped reading the question.**

The tool asks before it runs a command. That is a good design. By the third week I was pressing yes as people press
"accept" on cookie banners: with my hand, not my head. On day fifteen it asked to delete a folder of configuration files
it had judged "obsolete, not referenced anywhere". My finger was already moving.

The folder was referenced. By the nightly job that reconciles customs fees, by path, from a shell script that lived on
the server and nowhere in the repository. Nothing in the code could have told the agent that. Only I could, because I
had spent an evening of my first week reading crontabs on the server, for no better reason than that nobody had.

I did not press yes. I sat back. Then I made two changes. I told the tool which commands it could run without asking
and which it must always ask about. And I made a rule for myself: when it asks, I read the whole question aloud, under
my breath. Steven, at the next desk, turned round the first time to see who I was talking to, and after that he
stopped turning round.

## Day 19

**Today's lesson: one client.**

The contractor had left twelve SOAP clients behind, one per carrier, each a slightly different copy of the same idea,
like twelve brothers raised in different countries. I decided, in my third week, to replace them all with one shared
client. I was on probation. I wanted Hanne to see something large with my name on it, and I had a machine that could
type faster than anyone in the building.

I spent the weekend on it with the agent. By Sunday night there was one change: a new client, twelve old ones
removed, three hundred files touched, every test green. On Monday I put it up for review as "a simplification".

Steven, from the next desk, ran three agent sessions at once and was the first person in the building to call them
"my team". He scrolled for a while with his chin on his fist. Then he sat back.

"Big push, big shit." Not unkindly. Back to his own screen.

I thought he was jealous of the size of it. I answered his two comments politely, fixed a typo he had found, and
merged it on Wednesday evening.

On Thursday morning three carriers stopped receiving our customs messages. Each of the twelve old clients had carried
some small private habit of its carrier's: a header one of them insisted on, a date in a format another had never
admitted to, a retry that a third depended on without knowing. None of it was in any test, because the contractor had
learned each one at two in the morning, by hand, and written none of them down. My one client had none of the habits.

Rolling back was not possible; other changes had gone in on top of mine. I put the three old clients back by hand,
one at a time, reading the contractor's code line by line to find what I had thrown away. It took until six on Friday
morning. Steven came in at half five. Looked at my screen for three seconds. Made the coffee. Said nothing.

The next week I replaced one client: the smallest carrier's, the one with the fewest habits. It took two days, most of
them spent reading, and I wrote the carrier's habits on an index card and pinned it above my desk, where eleven more
cards would go.

## Day 23

**Today's lesson: a second, different reviewer before "final".**

The board wanted to retire an old customs declaration service. Everyone called it MILA, which stood for something long
and administrative that nobody could remember any more, like most acronyms after their tenth birthday. Before anyone
could plan the retirement, someone had to answer two questions. How many places in our code still called MILA? And who
owned each of those places?

Hanne gave it to me on a Monday. "By Thursday, if that is realistic. A number, and a list of owners.
The board responds well to numbers."

I gave it to the agent on Monday afternoon. It was a good task for the machine, I thought: reading many files,
counting, grouping, the kind of patient work that made my eyes ache. I wrote a decent brief. Search all the
repositories for references to the MILA service. Count them. Group them by component. For each component, find the
owner from the ownership file and the commit history.

It came back within the hour with something beautiful. A table. Forty-seven references across nine components. Six
owners, named, each with the components they were responsible for. A short paragraph of findings at the top, a short
paragraph of risks at the bottom. Headings. Bold in the right places. It read like the work of a careful consultant.

I liked it the way you like a suit in a shop window. It made me look good, and I wanted very badly for it to be right.

I pasted the table into a mail to Hanne. I did not press send. It was half past four. I told myself I would send it in
the morning, after coffee, which is the closest I came, that week, to wisdom.

At home that evening, in the workshop, I had been experimenting with something. I had noticed on Day 4 that the
machine agrees with whoever is talking to it. It occurred to me that the person talking to it about its own work was
always me, and I was always hoping it was right. What if the one checking was a stranger? A different model, in a
fresh session, with no memory of how the work was done, no stake in its being right, and only one instruction: here is
a question, here is an answer, here is the source; find what is wrong.

I could not do that at home, with the company's code; the workshop was for my own material, and that rule I had not
broken. But at work, the company's account gave me more than one model. The count had been done by the
quicker, cheaper one. The next morning, before coffee, I opened a new session with the larger model, gave it the
original question, the table, and access to the repositories, and nothing else. Not my brief. Not the conversation.
Not my hopes.

"Check this answer against the source," I wrote. "Assume it is wrong somewhere. For every number, show me how you
verified it. For every owner, show me where you found them."

Then I went for coffee. When I came back it had found two things.

The first was the count. The original search had been case-insensitive, which is the sensible default when you look
for a name that people spell carelessly. But MILA was not only a service. Mila was also a person. A developer who had
worked on the integration layer two years earlier, and who had the pleasant habit of signing her temporary fixes in
comments: "Mila: workaround until the carrier updates their schema". There were sixteen of those. Sixteen of the
forty-seven references to the service were, in fact, references to a woman who had left the company and was presumably
living a full life somewhere, unaware that a machine had counted her as legacy infrastructure. I felt for her.

The true number was thirty-one.

The second thing was quieter and worse. There was a seventh owner. The finance team had a small reporting script, in a
separate repository that was not under the integration group's umbrella, which pulled monthly figures straight from
MILA's database view. The first search had looked only in the repositories it had been told about, which were the ones
I had listed, which were the ones I knew about. The reviewer found the script because it went looking for who read
MILA's data, not just who called MILA's interface.

I sat with the two tables side by side. Forty-seven and thirty-one. Six owners and seven.

Then I did the thing I should have done first: I checked by hand. Not everything. Five references from the reviewer's
list, five from the original, picked at random. I opened each file and read each line. The reviewer was right on all
ten. Then I went and found the finance script myself, and read it, and found the owner's name at the top. Then I
counted the Mila comments with a search for her exact spelling and the word "workaround". Sixteen.

I rewrote the mail. Thirty-one references, nine components, seven owners. Under the table, three lines: how the count
was made, the two corrections and why they happened, and the exact search command, so that anyone could run it again.

Hanne read it in her office with the door open. She came out with a printout, which is a thing she does with documents
she means to keep.

"Which number do I give the board?"

"Thirty-one."

"And if they ask how sure you are?"

"Tell them how it was counted. They can count again. It takes ten minutes."

She looked at the three lines under the table for a long time.

"The last person who did this kind of thing for me," she said, "gave me a very nice slide." She did not say what had
happened to the nice slide.

## Day 24

**Today's lesson: do not count by hand twice.**

The next morning another request came, from another manager, for another old service. How many references, which
owners. Of course.

I could have done it the same way, in half a day of careful work. And the week after, another one. And one day I would
be tired, or rushed, and I would skip the review.

So I did not answer the question. I built the thing that answers it.

It was a small procedure in plain text, and a small script beside it. The script searched every repository the
company had, from the hosting system's own list, which is the only list that does not forget. It matched the exact
service name, listed comments and author lines separately for a human to look at, looked for readers of the service's
data as well as callers, and wrote the result to a file with the date and the command that produced it.

The procedure said, in five lines: run the script. Give its output and the original question to a fresh session of a
different model, with the instruction to assume an error. Check five results by hand. Write the answer with the method
underneath. Never send a number without the command that made it.

The procedure took me most of a day to write and test, which was more than the answer would have taken. Hanne asked
why the second count had taken me a day when the first had taken three. I said the third would take ten minutes. It
took eleven.

The reviewer was no oracle either. A week later it called a configuration value "dangerously high"; it was exactly
what the vendor's documentation required, and the reviewer had confused two settings with similar names. I wrote the
page number of the documentation in the margin of the procedure.

I underlined the last line of the procedure twice: never send a number without the command that made it.

## Day 38

**Today's lesson: it is very good, and that is the danger.**

Against the failures, the rest. In five weeks the agent had drafted tests for code nobody dared to touch, and some of
them were excellent. It had turned my scribbled notes into documentation that new people actually read. It had found a
resource leak that had been quietly restarting a service every few days for a year. I could not have done in five
months what we did in five weeks.

## The notebook, after

I still have the notebook. The owl's moustache has faded. The last page of the probation period, three months in,
says only: **Today's lesson: you are still the one who signs.**

Hanne extended my contract on a Thursday. She did not make a speech. She put a printout on my desk, a new one, with the
contract terms, and on top of it, with a paperclip, the old printout of the MILA mail, the one with the three lines
under the table.

"I would like you to keep doing that part," she said, and put her finger on the three lines, not on the table. "One
year. The board likes to look again." Then she went back to her office.

I left the paperclip where it was. The two pages are still clipped together, in the folder with the letter.

# Emil, year 3

By the third year Emil was an engineering manager, which meant that he had four tech leads, each with a calendar like
his old one, and a calendar of his own that he no longer read so much as obeyed. There was not much green in it now,
and what there was had been put there by his assistant, for lunch.

He was good at it. People liked working for him. He wrote the clearest planning documents on four floors. When the
September reorganisation undid the March one again, two of his tech leads said he was the only reason they had not
left. He believed them. He went home and could not sleep.

He interviewed people now, on Thursdays. Most interviews were forty-five minutes and ended on time.

The applicant on that Thursday was a student, final year, in a jacket that had been bought for the occasion and did not
yet know it. Nervous, fast, a young man who apologised at the end of his answers, where it cost nothing. He had brought
a laptop he did not need, as if it were a passport. On his CV, under "Open source", there was one line: a fix to the
macOS section of a small local proxy called kiko, with the test output pasted into the pull request. Under "References"
there was one name. Emil knew it.

Emil asked the question he asked everybody, about a carrier adapter that sends a message again when the carrier does
not answer. The student drew it on the back of his own CV, and stopped with the pen in the air.

"What if the carrier did get it the first time," he said, "and only the answer was lost? Then they have it twice. Does
somebody check?"

Nobody checked. There was a ticket for it, nine months old, and at the bottom of the ticket a comment from Emil: "Valid.
No capacity this quarter."

"Good question," said Emil, and moved on.

The interview went well. Not well enough. The company was hiring two people that quarter and there were forty
applications, and this one was a year too early, and Emil knew within ten minutes that the answer would be no.

At the end the student asked a question nobody had asked Emil in three years of interviews.

"If it's a no," he said, "could somebody tell me what to improve? Even ten minutes. I'd actually do it."

"I'm sorry," said Emil. "We don't have capacity for that."

He had a planning meeting at three. The student thanked him and left the drawing on the table.

Emil did not call the name under "References". He wrote the student's name on a sticky note, stuck it to the edge of
his screen, and found a gap in the calendar the following Monday, a quarter past twelve, between the platform sync and
the product sync. Fifteen minutes. He made it green.

On Sunday night, at a quarter to one, when his partner had gone to bed, he took the work laptop out of his bag and opened
the ticket. Then the adapter. The retry was still his, nearly three years old.

At four there was a fix: a check on the message number before anything was sent on, eleven lines, and a test that sent
every message twice. Five carriers passed. The sixth failed, and he could not see why.

At six he tried to push the branch, and the repository told him he was not allowed to. His account had lost its write
access in the March reorganisation, or the September one. Nobody had noticed, including him. He copied the branch onto
a USB stick.

His partner found him at the kitchen table at seven on Monday morning, still in Sunday's shirt, and did not ask.

Before the standup, he stopped at the desk of the man who wrote "stuff" in his commit messages, and tossed
the stick onto his keyboard.

"Please finish it," he said. "I have too many meetings today. I won't manage."

The man looked at the stick. "What is it?"

"The duplicates. One carrier fails. I don't know why."

The man plugged it in.

At twenty to eleven, in the platform sync, a notification came up in the corner of Emil's screen: a commit to the main
branch. The message said "stuff". He opened it under the table. Eleven of the lines were his. The twelfth was not. The sixth carrier
wrote its message numbers in lower case.

At a quarter past twelve the green block came up. Emil went into the small room with the drowning plant's sister in it,
closed the door, and rang the student.

It took eleven minutes. He told him three things to improve, and they were true. Then he told him that the question
about the message that arrives twice had been the right question, and that it had been fixed that morning.

"Who fixed it?" said the student.

Emil looked at the plant.

"A colleague," he said.

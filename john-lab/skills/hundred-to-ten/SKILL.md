---
name: hundred-to-ten
description: "Use when a user wants the best few of something short (tweets, hooks, headlines, taglines, subject lines, product names, ad lines) instead of a first draft. Triggers include 'make 100 and give me the best 10', 'grade these and cut them down', 'refine until you have the final 10', 'give me killer tweets', 'which of these hooks is best', or 'too generic, try again'. Generates a large pool, scores it on a fixed rubric, then cuts about 20% per round, each round judged through a different lens, refining survivors along the way."
---

# Hundred to ten

Asking for ten good lines gets ten average ones. Asking for a hundred and cutting them down in rounds, each round with a different reason to cut, gets ten that survived eleven kinds of scrutiny. Every cut is written down, so the user can see why a line died and pull it back.

## Inputs

- **What** is being written, **for whom**, and **where** it will appear (platform, character limit).
- **Source material:** transcripts, posts, product facts, past winners. Lines grounded in real material beat invented ones.
- **No-go list:** topics, words and framings the user rejects. Ask for this before generating, because users usually have one and only say so after seeing the first batch (for example: do not disparage yourself, do not mention a sensitive project, do not talk about revenue).
- **Final count** (default 10) and **pool size** (default 100).

## Rubric

Five criteria, 1-5 each, out of 25. Agree on them with the user. A default for social posts:

| Criterion | Asks |
|---|---|
| Hook | Does the first line stop the scroll? |
| Spice | Would someone reply or argue? |
| Receipts | Is there a specific, true detail? |
| Voice | Does it sound like the person, not a carousel? |
| Safe | Could this hurt their reputation or business? |

## Rounds

Write the pool and every round to one file, for example `ideas/<date>_<topic>-100-to-10.md`.

1. **Generate** the pool. Tag each line with its source (which video, post or fact). Vary form: questions, one-liners, lists, confessions, contrarian takes.
2. **Score** every line on the rubric.
3. **Cut about 20% per round**, each round through one lens, and say which lines were cut and why. A typical run from 100:

| Round | Count | Lens |
|---|---|---|
| 1 | 100 → 80 | Lowest total score |
| 2 | → 64 | Remove near-duplicates; keep the stronger twin |
| 3 | → 51 | Reply bait: would anyone respond? |
| 4 | → 41 | Receipts: cut anything generic |
| 5 | → 33 | Voice: cut anything that sounds templated |
| 6 | → 26 | Safety for this person's reputation |
| 7 | → 21 | Head-to-head within each topic |
| 8 | → 17 | Would a stranger share it? |
| 9 | → 14 | Works without context |
| 10 | → 11 | Merge and tighten |
| 11 | → 10 | Final cut |

4. **Refine** survivors as you go: tighten wording, merge two halves into one stronger line, move a closer from a cut line onto a survivor. Note every merge.
5. **Deliver** the final ten in order, each with its score, source and one line on why it survived, followed by three notable cuts and why they died.

## Rules

- Every line obeys the no-go list from the first generation onward. A no-go line in the pool is a bug, not a cut.
- No invented facts or numbers. If a line needs a statistic, it uses the user's real one or is cut.
- Match the platform's style conventions the user cares about (for example lowercase, no em dashes).
- Do not post or schedule anything.

---
name: writers-room
description: "Use when a creator or founder wants short talking-head video episodes written by a room of critics instead of one draft. Triggers include 'pitch me video ideas for this week', 'write my LinkedIn videos', 'react to what's trending', 'give me a teleprompter script', 'make episodes from these sources', 'weekly AI launches roundup', or 'run the writers room'. Runs scout pitches, a scored pitch meeting, a showrunner pick, draft, critique, accept-or-rebut revision, a red-line check against a show bible, a blind audience panel, and a final spoken script."
---

# Writers' room

One model writing one script produces the average take. A room of roles that disagree, scored by a panel that has never seen the script, produces the take worth filming. Every stage writes a file so the room can be resumed, audited and reused.

## Before the first run: the bible

Write `bible.md` with the user and keep it in the show folder. It is every role's system prompt.

- **Host:** who they are, what they have actually done, how they talk (sentence length, words they never use).
- **Audience:** 3-5 named personas with role, age, platform, moment of viewing, and what makes them stop or scroll. Example: "Dana, 46, owns a 14-person HVAC company, scrolls Reels at 9pm, distrusts anyone selling AI."
- **Pillars:** for example build-in-public, hot take, story, how-to, news reaction.
- **Red lines:** no facts beyond the sources (a post on X is "someone claimed", not a fact); nothing that identifies a customer or prospect; no legal conclusions; no punching down; any product names or numbers that must never appear.
- **Banned phrases** and a **spice dial** from 1 (useful) to 5 (picks a fight).

## Roles

| Role | Job |
|---|---|
| Scout | Pitches twice as many angles as needed, each tied to one real source (a trending post, a launch, a commit) with its link. |
| Provocateur | Scores for tension and shareability. |
| Strategist | Scores for fit with the audience and the host's business. |
| Skeptic | Scores for truth and red lines. The only role allowed to say "must". |
| Showrunner | Picks the episodes and writes each brief. |
| Copywriter | Drafts and revises. |
| Panel | The bible's personas, scoring hooks blind. |

## Stages

Write each stage to `shows/.work/<date>/NN_<stage>.json`.

1. **Scout.** 2N angles: `{id, pillar, raw_take, source_url, source_text, facts[], audience, so_what}`. Drop any angle without a source link.
2. **Pitch meeting.** Provocateur, Strategist and Skeptic score every angle 1-10 with a blunt `note` and a `direction` or `kill`.
3. **Pick.** Showrunner picks N. Disagreement is signal: a high Provocateur score with a low Skeptic score can still be the best episode if the brief fixes the truth problem. Brief: `{thesis, direction, spice_target, avoid}`. Every kill gets a one-line reason.
4. **Draft.** Six hooks of 14 words or fewer, one of each type (confession, contrarian, number, stakes, you-are-doing-X, live test); 3-5 beats `{cue, nudge}`; three closes; a 110-200 word script; the facts used.
5. **Critique.** Each critic quotes the exact words they would change, with severity `should` or `could`. The Skeptic may use `must`, only for red lines.
6. **Revise.** The copywriter answers every note `accepted` (and changes it) or `rebutted` with a reason. Skeptic `must` notes cannot be rebutted.
7. **Red-line check.** Skeptic passes or lists must-fix items. On fail, one fix round that changes only those items.
8. **Blind panel.** Shuffle the hooks without labels. Each persona scores `stop` and `comment` 1-10 with a 12-word reaction.
9. **Final cut.** Lead hook, two A/B alternates, script, risk notes, production notes.
10. **Own the take.** The exact words the host reads aloud, 150-220 words, in their voice: no hedges, no placeholders, no handles. This is what goes on the teleprompter.

## Variants

- **Trend reaction:** every angle reacts to one specific trending post and carries its link.
- **Weekly launches:** the scout finds 10-12 launches from the last 7 days with working links; the room picks 4-5 for a roundup (250-360 words, each with a use / watch / skip verdict) and up to two for their own episode.

## Rules

- Keep a `history.txt` of produced topics and reject repeats.
- Facts come only from the sources. If a claim matters and cannot be checked, the script says who claimed it.
- The host's real feedback overrides the room. Record it in the bible so the next run inherits it.
- Audio, when the room hands off to editing: voice around -16 LUFS, music about 20 LU under the voice. Hosts consistently notice music and effects that are too loud.
- Produce scripts. Do not post anything.

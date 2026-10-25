---
name: podcast-room
description: "Use when a user wants to produce a two-host podcast episode with AI voices from real material. Triggers include 'make a podcast episode', 'turn this into a podcast', 'write a two-person segment', 'use my cloned voice', 'make a 20 minute episode', or 'set up a podcast feed'. Runs pitchers and a showrunner to build a rundown with a facts ledger, writes and edits each segment with a red-line veto, records with consistent voices, checks the recording against the script, and assembles a leveled episode."
---

# Podcast room

A sequel to `writers-room`, for long form. The trick is the same: separate roles, written stages, and a veto for truth. The new parts are continuity across segments and checking that the recording says what the script says.

## Show bible

`BIBLE.md`: hosts (name, voice, what each may claim about themselves; a synthetic co-host claims no personal history), audience, segment formats, red lines (no facts beyond the sources, nothing that identifies a customer, words that must never be spoken), product mention limit per episode, pronunciation map, and loudness target.

## Stages

1. **Pitch.** Three pitchers with different lenses (listener, operator, provocateur) each pitch angles from the sources: trending topics, launches, real work from the week.
2. **Rundown.** A showrunner picks the episode: cold open, intro, 3-5 segments of 3-5 minutes each, outro, and a **facts ledger** listing every fact the episode may use with its source.
3. **Segments, one at a time.** Head writer drafts `{"id","title","lines":[{"speaker","text"}]}` → editor critiques with a red-line veto → revise. Finish one segment (write, record, check) before starting the next, so voice and running jokes stay consistent.
4. **Record.** Same voice IDs and a fixed seed for the whole episode; apply the pronunciation map; abort if a banned word appears in the text.
5. **Check.** Transcribe the recording locally and diff it against the script. Re-record any line that drifted, dropped words or mispronounced a name.
6. **Assemble.** Cold open → jingle → intro → segments → outro, leveled to the loudness target (around -16 LUFS for speech), music well under the voices.
7. **Lint and publish prep.** Episode length, chapter markers, show notes with links (sponsor mentions go here, not in the dialogue), cover art, and a feed entry. The owner publishes.

## Rules

- Write numbers as words in scripts so voices read them naturally.
- Use only voices the owner has rights to. A cloned voice is the owner's own, used with their consent.
- Disclose synthetic voices wherever the platform or the law requires it.
- Never publish or submit the feed without the owner's approval.

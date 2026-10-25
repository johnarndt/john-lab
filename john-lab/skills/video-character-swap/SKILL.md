---
name: video-character-swap
description: Replace one specific person in real footage (a player in a sports clip, someone in a crowd) with a character from reference images, so it looks filmed live, while every other person, the background, broadcast graphics and audio stay untouched. Use when the user wants "turn X in this clip into <character/mascot/icon>", a Higgsfield/Genjutsu-style character swap, or to fix a swap where the wrong person changed, uniforms got recoloured, or the character looks pasted on. Pipeline: SAM2 tracking → tracked crop → Happy Horse edit on Sunra → SAM2 matte of the character → tight composite with graphics protection. Also covers relabelling a lower-third name and trimming.
---

# Video character swap

Swap exactly one person in a real clip for a character, Higgsfield-style, and keep everything else original.
Proven on a 9 s NFL broadcast clip with 20+ players, score bug, a TOUCHDOWN stinger and a name lower-third.

**Why this shape.** Full-frame prompt editors (Kling O3 edit, Happy Horse on the whole frame) guess the target from
text: they picked the wrong player, recoloured a team's uniforms and garbled the score bug. The fix is to
(1) point a click-based tracker at the one person, (2) give the editor a crop where that person is the obvious
subject, and (3) paste back *only the character*, cut out with its own matte. Every pixel outside that matte stays
the source footage.

Scripts are in `scripts/` next to this file. Run `scripts/setup.sh` once (venv + SAM2.1-large weights in
`$SWAP_HOME`, default `~/.cache/video-character-swap`); it prints `PY=...` — use that interpreter for every
script, with `HF_HUB_OFFLINE=1 PYTORCH_ENABLE_MPS_FALLBACK=1` for the SAM2 ones. Put work files in the scratchpad.

## Costs and approvals

- Happy Horse edit on Sunra (`happy-horse-edit`): ~21 credits per second of input (9 s ≈ 192, 3.1 s ≈ 72).
  Follow the sunra skill: run `sunra tools` first, quote the cost, wait for the user's OK before `--yes`.
- Image keyframes / anything on fal need the user's own `FAL_KEY`; never write a key into a file.
- Everything else (SAM2, crop, composite, relabel, encode) is local and free.
- Needs: ffmpeg, [uv](https://docs.astral.sh/uv/), the `sunra` CLI with a Sunra account (or the user's own fal key for
  the optional keyframe steps), and a Mac with Apple silicon or a CUDA GPU for SAM2 at a usable speed.

## Use it responsibly

- Only edit footage the user owns or has the rights to edit, and only use character references they have the rights
  to use (their own mascot, licensed art, an original character).
- Swap a person for a clearly fictional character. Never use this to make a real person appear to do or say
  something they did not, or to put a real person's face or likeness into footage.
- A relabelled lower-third is for obvious parody or content. Never present an edited clip as an unaltered broadcast,
  and label it as edited where it is shared.
- Broadcast clips belong to their rights holders; check before posting one, edited or not.

## Workflow

1. **Frames and shots.** `ffmpeg -i in.mp4 -q:v 2 frames/%05d.jpg`, then `find_cuts.py frames` — a real cut
   scores ~0.6+. Each shot is tracked and composited separately (SAM2 does not survive cuts).
2. **Find the target per shot.** Make contact sheets (`ffmpeg ... tile`), then look at a full-res frame where the
   target is large and unoccluded. Note its number/name/position and the frame where it is clearest.
3. **Track the target.** `track.py frames masks START END PROMPT_FRAME "x,y,1;x,y,1;...;x,y,0"` — 3–4 positive
   clicks on the target (helmet, jersey, shorts, legs), negatives on the people touching it. Prompt from the clear
   frame; it propagates both ways. Check with `overlay.py frames masks sheet.jpg i,i,...` before going on.
   Also track any person who stands **in front of** the target (an "occluder", e.g. the defender beside him) into
   its own mask dir; they are kept real and on top.
4. **Graphics.** Static overlays: `static_gfx.py frames 0:END static_gfx.png "y0:y1:x0:x1;..."` over a stretch
   where the camera moves (search boxes around the score bug / stat line / network bug). Note when the bug fades
   out and when any full-screen stinger starts. Write `gfx.json` (schema in `composite.py`). SAM2 cannot track
   graphics — don't try.
5. **Character references.** Clean full-body front + 3/4 shots on white, borders trimmed (a screenshot's black
   rounded border will be copied). Search press images if the user's is small; skip off-colour photos (a pink-lit
   standee shifted the colour). Upload with `sunra_upload.sh FILE image/png`.
6. **Tracked crop.** `crop_track.py frames masks c SHOT_STARTS` → `c_crop.mp4` (9:16, target centred ~2× its
   height) + `c_rects.json`. For a close-up where the target already fills the frame, use the full 16:9 frame for
   that shot instead (rects `[[0,0,W,H]]*n`); Happy Horse needs ≥3 s, so ping-pong the frames to pad.
7. **Happy Horse edit** (`sunra call create_video`, model `happy-horse-edit`, `source_video` = uploaded crop,
   `reference_images` = up to 5 refs, matching `aspect_ratio`, `resolution` 1080p). Prompt rules learned the hard way:
   - Identify the target by **position and action** ("the player kept at the centre", "the one on the left of the
     hug"). Never mention another person's jersey number — "keep #53 human" printed **53 on the character**.
   - Say "plain fur/skin only: no jersey, no numbers, no letters, no text on the character".
   - Give the action timeline with seconds, especially props: "empty paws on the route, catches the ball at ~3 s,
     spikes it at ~5 s, empty paws after". Without it the character held the ball before the catch.
   - "Keep every other player, uniforms, field, crowd, camera motion and graphics unchanged."
   Output is 24 fps; `composite.py` maps frames by timestamp.
8. **Matte the character.** Extract the model output to frames and `track.py` the character in it (per shot, the
   model output keeps the source's cuts — find them with `find_cuts.py`). Check with `overlay.py`.
9. **Composite.** Per shot: `composite.py --frames frames --target-masks masks --rects c_rects.json --model hh.mp4
   --mattes hhmask --out-frames final [--offset FIRST_FRAME_OF_SHOT] --occluders occ_masks --gfx gfx.json`.
   Shots write into the same `final/` dir by source frame number, so splicing is automatic.
10. **Optional lower-third relabel.** Measure the name box (gridded crops), then
    `relabel.py --frames final --box X0,Y0,Y1 --text-xy X,Y --text "NEW NAME" --reveal "i:x,i:x" --hold 45`.
    If the source ends mid-wipe, the hold frames finish it so it's readable.
11. **Encode.** `ffmpeg -framerate 30000/1001 -i final/%05d.jpg -i in.mp4 -map 0:v -map 1:a -c:v libx264 -crf 14
    -pix_fmt yuv420p -af apad -c:a aac -shortest out.mp4` (use `-frames:v N -t SEC` and an `afade` to trim).
12. **Review before showing.** Zoomed crops around the character at the catch/peak moments, at shot edges, under
    the score bug and during any stinger. Check: right person replaced in every frame, no halo, no straight-edge
    slice (character ran off the crop → redo that shot wider), no character text, graphics on top, no ghost limbs.

## Dead ends (don't repeat)

| Tried | Result |
|---|---|
| Kling O3 / Happy Horse edit on the full frame | Swapped the wrong player; recoloured a team; garbled graphics |
| Wan VACE 14B masked inpainting (fal), even with pose skeletons and image keyframes every ~20 frames | Correct place, but identity melts between keyframes; black-filled masks become black stick legs |
| Wan 2.2 Animate Replace (fal) on the tracked crop | Ignores a non-human plush reference; draws a smeared human |
| Pasting back a padded hull around the original person | Blurry halo of model-redrawn background; character "collapses" when teammates occlude the target |
| Rectangle protection for graphics | Original person's legs show through gaps; use stillness mask + colour key |
| SAM2 on broadcast graphics | Catches fragments, then drifts onto players |
| `hf` hub download of SAM2 | Hung; `setup.sh` curls the resolve URLs |

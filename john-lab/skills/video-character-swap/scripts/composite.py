"""Paste only the swapped character back into the full-res original, using its own SAM2 matte from the model output.

usage: composite.py --frames DIR --target-masks DIR --rects JSON --model MP4 --mattes DIR --out-frames DIR
                    [--offset N] [--occluders DIR ...] [--gfx JSON]

Per source frame i (rects[k] is source frame offset+k; model frames are matched by timestamp, so a 24 fps model
output against a 29.97 fps source is fine):
  region = character matte from the model output (holes filled, so arms wrapped around it stay coherent)
           union the original target's mask (so no trace of the replaced person survives)
           minus occluders (people who must stay in front) and broadcast graphics (--gfx).
Edges are feathered ~1px: no soft halo of model-redrawn background survives around the character.
Writes NNNNN.jpg (1-based source numbering) into --out-frames, so shots can be composited separately and spliced.

--gfx JSON (all keys optional; frame indices 0-based, "until" exclusive):
{
  "static_mask": "static_gfx.png", "static_until": 243,       # stillness mask from static_gfx.py, while visible
  "rects": [[y0, y1, x0, x1, from, until], ...],              # always keep these boxes original in that range
  "stinger": {"from": 247, "band": [[y0, y1, x0, x1], ...]}   # animated full-screen graphic, keyed by colour
}
The stinger key keeps big solid saturated-red shapes, silver bevels touching them, the dark panel and pure-white
flying letters (not on the replaced person); over the character itself only solid red letters count, so the
target's original red pants stripes and white pants never leak through as speckles.
"""
import os, json, argparse
import numpy as np, cv2

ap = argparse.ArgumentParser()
ap.add_argument("--frames", required=True)
ap.add_argument("--target-masks", required=True)
ap.add_argument("--rects", required=True)
ap.add_argument("--model", required=True)
ap.add_argument("--mattes", required=True)
ap.add_argument("--out-frames", required=True)
ap.add_argument("--offset", type=int, default=0)
ap.add_argument("--occluders", nargs="*", default=[])
ap.add_argument("--gfx")
ap.add_argument("--src-fps", type=float, default=30000 / 1001)
a = ap.parse_args()

rects = json.load(open(a.rects))
gfx = json.load(open(a.gfx)) if a.gfx else {}
static = cv2.imread(gfx["static_mask"], cv2.IMREAD_GRAYSCALE) if gfx.get("static_mask") else None
os.makedirs(a.out_frames, exist_ok=True)

cap = cv2.VideoCapture(a.model)
mfps = cap.get(cv2.CAP_PROP_FPS)
gen = []
while True:
    ok, f = cap.read()
    if not ok:
        break
    gen.append(f)
print("model frames", len(gen), "fps", mfps)

def ellipse(k):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))

def stinger_mask(img, target, char, bands):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue, sat, val = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    red = (((hue < 8) | (hue > 170)) & (sat > 110) & (val > 60)).astype(np.uint8) * 255
    n, lab, st, _ = cv2.connectedComponentsWithStats(red)
    big, solid = np.zeros_like(red), np.zeros_like(red)
    for c in range(1, n):
        x, y, w, h, area = st[c]
        if area > 1500 and min(w, h) > 25:
            big[lab == c] = 255
        if area > 4000 and area / float(w * h) > 0.35:
            solid[lab == c] = 255
    silver = ((sat < 40) & (val > 110)).astype(np.uint8) * 255 & cv2.dilate(big, ellipse(15))
    panel = ((sat < 45) & (val < 85)).astype(np.uint8) * 255
    off_target = 255 - cv2.dilate(target, ellipse(21)) if target is not None else 255
    white = ((sat < 18) & (val > 175)).astype(np.uint8) * 255 & off_target
    g = big | silver | panel | white
    inner = cv2.erode(char, ellipse(21)) > 0
    g[inner] = solid[inner]
    band = np.zeros_like(g)
    for y0, y1, x0, x1 in bands:
        band[y0:y1, x0:x1] = 255
    return cv2.morphologyEx(g & band, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

def protect(m, i, img, target, char):
    if static is not None and i < gfx.get("static_until", 10 ** 9):
        m[cv2.dilate(static, np.ones((3, 3), np.uint8)) > 0] = 0
    for y0, y1, x0, x1, fr, to in gfx.get("rects", []):
        if fr <= i < to:
            m[y0:y1, x0:x1] = 0
    sting = gfx.get("stinger")
    if sting and i >= sting["from"]:
        m[stinger_mask(img, target, char, sting["band"]) > 0] = 0
    for d in a.occluders:
        occ = cv2.imread(os.path.join(d, f"{i + 1:05d}.png"), cv2.IMREAD_GRAYSCALE)
        if occ is not None:
            m[cv2.dilate(occ, np.ones((5, 5), np.uint8)) > 0] = 0
    return m

def fill_holes(m):
    cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    out = np.zeros_like(m)
    cv2.drawContours(out, cnts, -1, 255, -1)
    return out

for k, (x0, y0, w, h) in enumerate(rects):
    i = k + a.offset
    name = f"{i + 1:05d}"
    orig = cv2.imread(os.path.join(a.frames, name + ".jpg"))
    j = min(len(gen) - 1, int(round(k / a.src_fps * mfps)))
    matte = cv2.imread(os.path.join(a.mattes, f"{j + 1:05d}.png"), cv2.IMREAD_GRAYSCALE)
    tm = cv2.imread(os.path.join(a.target_masks, name + ".png"), cv2.IMREAD_GRAYSCALE)
    reg = np.zeros(orig.shape[:2], np.uint8)
    if matte is not None and matte.any():
        reg[y0:y0 + h, x0:x0 + w] = cv2.resize(fill_holes(matte), (w, h), interpolation=cv2.INTER_LINEAR)
        reg = cv2.dilate((reg > 127).astype(np.uint8) * 255, np.ones((3, 3), np.uint8))
    char = reg.copy()
    if tm is not None and tm.any():
        inside = np.zeros_like(reg); inside[y0:y0 + h, x0:x0 + w] = 255
        reg |= cv2.dilate(tm, ellipse(13)) & inside
    reg = protect(reg, i, orig, tm, char)
    if reg.any():
        full = orig.copy()
        g = gen[j]
        full[y0:y0 + h, x0:x0 + w] = cv2.resize(g, (w, h), interpolation=cv2.INTER_AREA if w < g.shape[1] else cv2.INTER_LANCZOS4)
        al = cv2.GaussianBlur(reg, (0, 0), 1.2).astype(np.float32)[..., None] / 255.0
        orig = (full * al + orig * (1 - al)).astype(np.uint8)
    cv2.imwrite(os.path.join(a.out_frames, name + ".jpg"), orig, [cv2.IMWRITE_JPEG_QUALITY, 97])
print("wrote", len(rects), "frames to", a.out_frames)

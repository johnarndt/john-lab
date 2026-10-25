"""Replace a broadcast name label (e.g. the player name over TOUCHDOWN) with new text, keep its wipe-in, hold the end.

usage: relabel.py --frames DIR --box X0,Y0,Y1 --text-xy X,Y --text "NEW NAME" --reveal "265:590,266:632,267:722"
                  [--hold 45] [--font PATH] [--size 62]
--box: the label box's left edge and vertical span. --reveal: how far right the original box has wiped in on each
frame (measure by eye from crops: the logo behind the box is dark too, so auto-detecting the edge fails).
The box is redrawn in its own sampled colour with the new text clipped to the wipe. Then HOLD copies of the last
frame are appended (NNNNN.jpg continuing the numbering) while the wipe finishes, so the new name is readable when
the original clip ends mid-animation. Encode with `-af apad -shortest` so audio pads with silence.
"""
import os, glob, argparse
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("--frames", required=True)
ap.add_argument("--box", required=True)
ap.add_argument("--text-xy", required=True)
ap.add_argument("--text", required=True)
ap.add_argument("--reveal", required=True)
ap.add_argument("--hold", type=int, default=45)
ap.add_argument("--font", default="/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf")
ap.add_argument("--size", type=int, default=62)
a = ap.parse_args()

X0, Y0, Y1 = (int(v) for v in a.box.split(","))
TX, TY = (int(v) for v in a.text_xy.split(","))
reveal = {int(k): int(v) for k, v in (p.split(":") for p in a.reveal.split(","))}
font = ImageFont.truetype(a.font, a.size)
FULL_R = TX + int(font.getlength(a.text)) + 14
files = sorted(glob.glob(os.path.join(a.frames, "*.jpg")))
last = len(files) - 1

def draw(img, right, color):
    img[Y0:Y1, X0:right] = color
    pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    layer = Image.new("L", pil.size, 0)
    ImageDraw.Draw(layer).text((TX, TY), a.text, font=font, fill=255)
    m = np.array(layer, np.float32)[..., None] / 255.0
    m[:, right - 6:] = 0
    out = np.array(pil, np.float32) * (1 - m) + 255 * m
    return cv2.cvtColor(out.astype(np.uint8), cv2.COLOR_RGB2BGR)

color = right = None
for i in sorted(reveal):
    img = cv2.imread(files[i])
    if color is None:
        color = np.median(img[Y0 + 10:Y1 - 10, X0 + 2:X0 + 12].reshape(-1, 3), 0).astype(np.uint8)
    right = reveal[i]
    cv2.imwrite(files[i], draw(img, right, color), [cv2.IMWRITE_JPEG_QUALITY, 97])

last_img = cv2.imread(files[last])
step = max(8, (FULL_R - right) // 6)
for k in range(a.hold):
    right = min(FULL_R, right + step)
    cv2.imwrite(os.path.join(a.frames, f"{last + 2 + k:05d}.jpg"), draw(last_img.copy(), right, color), [cv2.IMWRITE_JPEG_QUALITY, 97])
print("relabeled", sorted(reveal), "held", a.hold, "frames; box full width to x", FULL_R)

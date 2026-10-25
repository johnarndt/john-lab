"""Exact mask of static broadcast overlays (score bug, network logo, stat lines) from pixel stillness.

usage: static_gfx.py FRAMES_DIR START:END OUT_PNG "y0:y1:x0:x1;..." [THRESH]
Over a stretch where the camera moves (START:END, 0-based, inclusive), overlay pixels barely change while the
field does. Pixels with per-pixel std below THRESH (default 9) inside the given search boxes become the mask.
Text that changes during the stretch (a running clock) may only partly register; add a small box for it in the
graphics config instead. SAM2 cannot track broadcast graphics, so don't try.
"""
import sys
import numpy as np, cv2

fd, rng, out, boxes = sys.argv[1:5]
thresh = float(sys.argv[5]) if len(sys.argv) > 5 else 9
a, b = (int(x) for x in rng.split(":"))
stack = np.stack([cv2.imread(f"{fd}/{i + 1:05d}.jpg").astype(np.float32) for i in range(a, b + 1, 3)])
m = (stack.std(0).mean(2) < thresh).astype(np.uint8) * 255
m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
keep = np.zeros_like(m)
for box in boxes.split(";"):
    y0, y1, x0, x1 = (int(v) for v in box.split(":"))
    keep[y0:y1, x0:x1] = 255
cv2.imwrite(out, m & keep)
print("wrote", out, int((m & keep).astype(bool).sum()), "px")

"""Find hard camera cuts by colour-histogram jumps between consecutive frames.

usage: find_cuts.py FRAMES_DIR [TOP_N]
Prints the biggest jumps as (frame_index_of_new_shot, score). A real cut scores far above the rest (~0.6+);
broadcast graphics wiping in score ~0.1-0.3. ffmpeg's scene filter misses soft broadcast cuts, so use this.
"""
import sys, glob
import numpy as np, cv2

fs = sorted(glob.glob(sys.argv[1] + "/*.jpg"))
top = int(sys.argv[2]) if len(sys.argv) > 2 else 8
prev, d = None, []
for i, f in enumerate(fs):
    h = cv2.calcHist([cv2.resize(cv2.imread(f), (160, 90))], [0, 1, 2], None, [8, 8, 8], [0, 256] * 3).flatten()
    h /= h.sum()
    if prev is not None:
        d.append((i, round(float(np.abs(h - prev).sum()), 3)))
    prev = h
print(sorted(d, key=lambda x: -x[1])[:top])

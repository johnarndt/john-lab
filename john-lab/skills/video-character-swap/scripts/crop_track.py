"""Cut a smoothed 9:16 virtual-camera crop that follows the tracked target, for whole-subject swap models.

usage: crop_track.py FRAMES_DIR MASKS_DIR OUT_PREFIX SHOT_STARTS [MIN_H]
SHOT_STARTS: comma-separated first frame index of each shot (e.g. 0,226); smoothing never crosses a cut.
The window is ~2x the target's height (min MIN_H px, default 420) so a wider character still fits; if the swapped
character is drawn bigger than the target and runs off the crop edge, re-run that shot with a full-frame 16:9 crop.
Writes OUT_PREFIX_crop.mp4 (720x1280, 29.97 fps) and OUT_PREFIX_rects.json ([x0, y0, w, h] per source frame).
"""
import sys, os, json, subprocess, tempfile
import numpy as np, cv2

frames_dir, masks_dir, out, shots = sys.argv[1:5]
min_h = int(sys.argv[5]) if len(sys.argv) > 5 else 420
files = sorted(f for f in os.listdir(frames_dir) if f.endswith(".jpg"))
n = len(files)
FH, FW = cv2.imread(os.path.join(frames_dir, files[0])).shape[:2]
cuts = [int(s) for s in shots.split(",")] + [n]
OW, OH = 720, 1280

boxes = np.full((n, 4), np.nan)
for i in range(n):
    m = cv2.imread(os.path.join(masks_dir, f"{i + 1:05d}.png"), cv2.IMREAD_GRAYSCALE)
    if m is not None and m.any():
        x, y, w, h = cv2.boundingRect(m)
        boxes[i] = [x + w / 2, y + h / 2, w, h]

def smooth(a, k=9):
    idx = np.arange(len(a))
    good = ~np.isnan(a)
    a = np.interp(idx, idx[good], a[good])
    pad = np.pad(a, k // 2, mode="edge")
    return np.convolve(pad, np.ones(k) / k, mode="valid")

rects = []
for s, e in zip(cuts[:-1], cuts[1:]):
    cx, cy, bw, bh = (smooth(boxes[s:e, c]) for c in range(4))
    H = smooth(np.clip(np.maximum(2.0 * bh, 1.4 * bw * 16 / 9), min_h, FH), 15)
    for j in range(e - s):
        h = int(round(H[j])); w = int(round(h * 9 / 16))
        x0 = int(np.clip(cx[j] - w / 2, 0, FW - w)); y0 = int(np.clip(cy[j] - h / 2, 0, FH - h))
        rects.append([x0, y0, w, h])

tmp = tempfile.mkdtemp()
for i, (x0, y0, w, h) in enumerate(rects):
    f = cv2.imread(os.path.join(frames_dir, f"{i + 1:05d}.jpg"))
    cv2.imwrite(os.path.join(tmp, f"{i:05d}.png"), cv2.resize(f[y0:y0 + h, x0:x0 + w], (OW, OH), interpolation=cv2.INTER_LANCZOS4))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30000/1001", "-i", os.path.join(tmp, "%05d.png"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "12", out + "_crop.mp4"], check=True)
json.dump(rects, open(out + "_rects.json", "w"))
print("wrote", out + "_crop.mp4", len(rects), "frames")

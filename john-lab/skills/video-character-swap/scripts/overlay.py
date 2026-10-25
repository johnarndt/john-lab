"""Contact sheet of masks drawn over frames, to check a SAM2 track before spending anything on it.

usage: overlay.py FRAMES_DIR MASKS_DIR OUT_JPG IDX,IDX,...   (0-based frame indices; 4 tiles per row)
"""
import sys, os
import numpy as np, cv2

fd, md, out = sys.argv[1:4]
idx = [int(x) for x in sys.argv[4].split(",")]
tiles = []
for i in idx:
    n = f"{i + 1:05d}"
    f = cv2.imread(os.path.join(fd, n + ".jpg"))
    m = cv2.imread(os.path.join(md, n + ".png"), cv2.IMREAD_GRAYSCALE)
    if m is not None:
        c = f.copy()
        c[m > 0] = (0.4 * c[m > 0] + 0.6 * np.array([255, 0, 255])).astype(np.uint8)
        cnt, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(c, cnt, -1, (0, 255, 255), 3)
        f = c
    cv2.putText(f, str(i), (40, 80), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 255, 255), 5)
    tiles.append(cv2.resize(f, (640, int(640 * f.shape[0] / f.shape[1]))))
while len(tiles) % 4:
    tiles.append(np.zeros_like(tiles[0]))
cv2.imwrite(out, np.vstack([np.hstack(tiles[r:r + 4]) for r in range(0, len(tiles), 4)]))
print("wrote", out)

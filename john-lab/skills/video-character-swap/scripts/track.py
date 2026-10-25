"""Track one object through a frame range with SAM2.1 video and write per-frame PNG masks (255 = object).

usage: track.py FRAMES_DIR OUT_DIR START END PROMPT_FRAME "x,y,label;x,y,label;..."
Frame indices are 0-based; FRAMES_DIR holds 00001.jpg... (1-based names). label 1 = on the object, 0 = not.
Propagates forward and backward from PROMPT_FRAME. Run once per shot: SAM2 does not survive hard cuts.
Weights: $SWAP_HOME/sam21 (see setup.sh). Run with HF_HUB_OFFLINE=1 PYTORCH_ENABLE_MPS_FALLBACK=1.
"""
import sys, os, glob
import numpy as np, cv2, torch
from PIL import Image
from transformers import Sam2VideoModel, Sam2VideoProcessor

frames_dir, out_dir, start, end, pf, pts = sys.argv[1:7]
start, end, pf = int(start), int(end), int(pf)
os.makedirs(out_dir, exist_ok=True)
weights = os.path.join(os.environ.get("SWAP_HOME", os.path.expanduser("~/.cache/video-character-swap")), "sam21")
files = sorted(glob.glob(os.path.join(frames_dir, "*.jpg")))[start:end + 1]
frames = [Image.open(f).convert("RGB") for f in files]
points = [[float(a), float(b)] for a, b, _ in (p.split(",") for p in pts.split(";"))]
labels = [int(l) for *_, l in (p.split(",") for p in pts.split(";"))]

device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
model = Sam2VideoModel.from_pretrained(weights).to(device, dtype=torch.float32)
proc = Sam2VideoProcessor.from_pretrained(weights)
sess = proc.init_video_session(video=frames, inference_device=device, dtype=torch.float32)
rel = pf - start
proc.add_inputs_to_inference_session(inference_session=sess, frame_idx=rel, obj_ids=1,
                                     input_points=[[points]], input_labels=[[labels]])
model(inference_session=sess, frame_idx=rel)

H, W = sess.video_height, sess.video_width
masks = {}
for reverse in (False, True):
    for out in model.propagate_in_video_iterator(sess, start_frame_idx=rel, reverse=reverse):
        m = proc.post_process_masks([out.pred_masks], original_sizes=[[H, W]], binarize=True)[0]
        masks[out.frame_idx] = m[0, 0].cpu().numpy().astype(np.uint8) * 255

for i in range(len(frames)):
    m = masks.get(i, np.zeros((H, W), np.uint8))
    cv2.imwrite(os.path.join(out_dir, f"{start + i + 1:05d}.png"), m)
print("frames", len(frames), "masked", sum(1 for v in masks.values() if v.any()))

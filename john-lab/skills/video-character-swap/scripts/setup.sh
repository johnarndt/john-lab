#!/usr/bin/env bash
# One-time setup: Python venv with torch/transformers/opencv and SAM2.1-large weights.
# Everything lives in $SWAP_HOME (default ~/.cache/video-character-swap). Safe to re-run.
set -euo pipefail
SWAP_HOME="${SWAP_HOME:-$HOME/.cache/video-character-swap}"
mkdir -p "$SWAP_HOME/sam21"
if [ ! -x "$SWAP_HOME/venv/bin/python" ]; then
  uv venv -q --python 3.12 "$SWAP_HOME/venv"
fi
uv pip install -q --python "$SWAP_HOME/venv/bin/python" torch torchvision "transformers>=4.57" accelerate \
  opencv-python-headless pillow numpy scipy
# hf hub downloads can hang; plain curl of the resolve URLs is reliable
for f in config.json preprocessor_config.json video_preprocessor_config.json processor_config.json model.safetensors; do
  [ -s "$SWAP_HOME/sam21/$f" ] || curl -sfL --max-time 600 -o "$SWAP_HOME/sam21/$f" \
    "https://huggingface.co/facebook/sam2.1-hiera-large/resolve/main/$f"
done
"$SWAP_HOME/venv/bin/python" -c "from transformers import Sam2VideoModel; print('ok: SAM2 video available')"
echo "PY=$SWAP_HOME/venv/bin/python"

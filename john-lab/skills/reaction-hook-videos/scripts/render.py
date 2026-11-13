#!/usr/bin/env python3
"""Join a batch of local reaction clips to a reusable demo with FFmpeg."""

import argparse
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


WIDTH = 1080
HEIGHT = 1920
FPS = 30
POSITIONS = {"top": (500, 360), "center": (500, 950), "lower": (500, 1470)}


def probe(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)],
        check=True, capture_output=True, text=True,
    )
    data = json.loads(result.stdout)
    video = next(
        (stream for stream in data["streams"]
         if stream["codec_type"] == "video" and not stream.get("disposition", {}).get("attached_pic")),
        None,
    )
    if video is None:
        raise ValueError(f"{path} needs a video stream")
    if video != next(stream for stream in data["streams"] if stream["codec_type"] == "video"):
        raise ValueError(f"{path} has an attached image before its video stream")
    duration = float(video.get("duration", data["format"].get("duration", "nan")))
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError(f"Could not determine the video duration of {path}")
    rotated = any(
        abs(round(float(item.get("rotation", 0)))) % 180 == 90
        for item in video.get("side_data_list", [])
    )
    width, height = video["width"], video["height"]
    if rotated:
        width, height = height, width
    has_audio = any(stream["codec_type"] == "audio" for stream in data["streams"])
    return duration, (width, height), has_audio


def frame_count(seconds, name):
    if (
        isinstance(seconds, bool) or not isinstance(seconds, (int, float))
        or not math.isfinite(seconds) or seconds < 0
    ):
        raise ValueError(f"{name} must be a finite, nonnegative number of seconds")
    return round(seconds * FPS)


def segment(start, duration, available, name):
    start_frame = frame_count(start, name + " start")
    count = frame_count(duration, name + " duration")
    if count < 1 or start_frame + count > math.floor(available * FPS + 0.001):
        raise ValueError(f"{name} range is empty or extends past its source ({available:.2f}s)")
    return start_frame / FPS, count / FPS


def ass_time(frame):
    centiseconds = round(frame * 100 / FPS)
    seconds, fraction = divmod(centiseconds, 100)
    minutes, second = divmod(seconds, 60)
    hour, minute = divmod(minutes, 60)
    return f"{hour}:{minute:02}:{second:02}.{fraction:02}"


def subtitle_file(font, hook, hook_duration, captions, duration):
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {WIDTH}
PlayResY: {HEIGHT}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,{font},76,&H00FFFFFF,&H00FFFFFF,&H18131313,&H55000000,-1,0,0,0,100,100,0,0,1,6,3,5,96,176,0,1
Style: Caption,{font},59,&H00FFFFFF,&H00FFFFFF,&H18131313,&H55000000,-1,0,0,0,100,100,0,0,1,5,2,5,96,176,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    hook_position = hook.get("position", "lower") if isinstance(hook, dict) else "lower"
    hook_text = hook.get("text") if isinstance(hook, dict) else hook
    events = [(0, hook_duration, hook_text, hook_position, "Hook")]
    events.extend(
        (item["start"], item["end"], item["text"], item.get("position", "lower"), "Caption")
        for item in captions
    )
    lines = []
    occupied = {}
    for start, end, message, position, style in events:
        first = frame_count(start, "Caption start")
        last = frame_count(end, "Caption end")
        if not first < last <= frame_count(duration, "Video duration"):
            raise ValueError("Caption timing must fall within the finished video")
        if position not in POSITIONS:
            raise ValueError(f"Unknown caption position: {position}")
        if any(first < other_end and other_start < last for other_start, other_end in occupied.get(position, [])):
            raise ValueError(f"Captions overlap at the {position} position")
        occupied.setdefault(position, []).append((first, last))
        if not isinstance(message, str) or not message.strip() or re.search(r"[{}\\\x00-\x09\x0b-\x1f]", message):
            raise ValueError("Caption text must be plain text without braces or backslashes")
        x, y = POSITIONS[position]
        # Keep deliberate line breaks and allow libass to wrap within safe margins.
        message = message.strip().replace("\n", r"\N")
        placement = rf"{{\an5\pos({x},{y})}}"
        lines.append(f"Dialogue: 0,{ass_time(first)},{ass_time(last)},{style},,0,0,0,,{placement}{message}")
    return header + "\n".join(lines) + "\n"


def crop_filter(crop, size):
    if crop is None:
        return "", size[0] / size[1]
    if not isinstance(crop, list) or len(crop) != 4 or any(type(value) is not int for value in crop):
        raise ValueError("Demo crop must be [x, y, width, height] in pixels")
    x, y, width, height = crop
    if min(x, y) < 0 or min(width, height) < 2 or x + width > size[0] or y + height > size[1]:
        raise ValueError("Demo crop extends outside the source frame")
    return f"crop={width}:{height}:{x}:{y}:exact=1,", width / height


def video_filters(index, duration, contain, label, crop=""):
    source = f"[{index}:v:0]{crop}fps={FPS},setpts=PTS-STARTPTS,format=yuv420p"
    cover = (
        f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase:force_divisible_by=2,"
        f"crop={WIDTH}:{HEIGHT},setsar=1"
    )
    finish = f"tpad=stop_mode=clone:stop_duration=0.1,trim=duration={duration:.6f}[{label}]"
    if not contain:
        return f"{source},{cover},{finish}"
    return (
        f"{source},split[{label}bg][{label}fg];"
        f"[{label}bg]{cover},boxblur=24:2,eq=brightness=-0.22[{label}canvas];"
        f"[{label}fg]scale=1000:1520:force_original_aspect_ratio=decrease:"
        f"force_divisible_by=2,setsar=1[{label}detail];"
        f"[{label}canvas][{label}detail]overlay=(W-w)/2:(H-h)/2:shortest=1,{finish}"
    )


def audio_filters(index, duration, enabled, label):
    if not enabled:
        return f"anullsrc=r=48000:cl=stereo,atrim=duration={duration:.6f}[{label}]"
    return (
        f"[{index}:a:0]asetpts=PTS-STARTPTS,"
        "aformat=sample_rates=48000:channel_layouts=stereo,"
        f"apad=whole_dur={duration:.6f},atrim=duration={duration:.6f},"
        f"afade=t=in:d=0.02,afade=t=out:st={max(0, duration - 0.04):.6f}:d=0.04[{label}]"
    )


def render(reaction, demo, reaction_edit, demo_edit, demo_framing, audio, subtitles, target):
    if target.exists():
        raise ValueError(f"Output already exists: {target}")
    with tempfile.TemporaryDirectory(prefix="reaction-render-", dir=target.parent) as stage:
        folder = Path(stage)
        (folder / "captions.ass").write_text(subtitles, encoding="utf-8")
        local_output = folder / "render.mp4"
        crop, ratio = demo_framing
        graph = ";".join([
            video_filters(0, reaction_edit[1], False, "reaction"),
            video_filters(1, demo_edit[1], abs(ratio - WIDTH / HEIGHT) > 0.04, "demo", crop),
            audio_filters(0, reaction_edit[1], audio[0], "intro_audio"),
            audio_filters(1, demo_edit[1], audio[1], "demo_audio"),
            "[reaction][intro_audio][demo][demo_audio]concat=n=2:v=1:a=1[edit][mix]",
            "[edit]ass=captions.ass[video]",
            "[mix]loudnorm=I=-16:TP=-1.5:LRA=9,aresample=48000[audio]",
        ])
        command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin"]
        for file, (start, duration) in [(reaction, reaction_edit), (demo, demo_edit)]:
            command.extend(["-ss", f"{start:.6f}", "-t", f"{duration:.6f}", "-i", str(file)])
        command.extend([
            "-filter_complex_threads", "2", "-filter_complex", graph, "-map", "[video]", "-map", "[audio]",
            "-c:v", "libx264", "-threads", "4", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", str(local_output),
        ])
        subprocess.run(command, cwd=folder, check=True)
        # Publish the completed file atomically and refuse to clobber a concurrent export.
        target.hardlink_to(local_output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--out", type=Path, default=Path("exports"))
    parser.add_argument("--only", help="Render one variant ID")
    args = parser.parse_args()
    try:
        for executable in ("ffmpeg", "ffprobe"):
            if not shutil.which(executable):
                raise ValueError(f"{executable} is required")
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        directory = args.manifest.resolve().parent
        output = args.out.resolve()
        output.mkdir(parents=True, exist_ok=True)
        demo = directory / manifest["demo"]
        demo_length, demo_size, demo_audio = probe(demo)
        font = manifest.get("font", "Arial")
        if not isinstance(font, str) or not font.strip() or re.search(r"[,\x00-\x1f]", font):
            raise ValueError("Use a plain font family name")
        variants = manifest["variants"]
        ids = [item["id"] for item in variants]
        if not ids or len(set(ids)) != len(ids):
            raise ValueError("The manifest needs at least one variant and unique variant IDs")
        if args.only and args.only not in ids:
            raise ValueError(f"Unknown variant: {args.only}")
        for variant in variants:
            name = variant["id"]
            if args.only and name != args.only:
                continue
            if not isinstance(name, str) or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}", name):
                raise ValueError("Use a variant ID of up to 64 letters, digits, dashes, or underscores")
            reaction = directory / variant["reaction"]
            reaction_length, _, reaction_audio = probe(reaction)
            reaction_edit = segment(
                variant.get("reaction_start", 0), variant.get("reaction_duration", 2),
                reaction_length, "Reaction",
            )
            demo_edit = segment(
                variant.get("demo_start", manifest.get("demo_start", 0)),
                variant.get("demo_duration", manifest.get("demo_duration", 8)),
                demo_length, "Demo",
            )
            subtitles = subtitle_file(
                font, variant["hook"], reaction_edit[1], variant.get("captions", []),
                reaction_edit[1] + demo_edit[1],
            )
            demo_framing = crop_filter(variant.get("demo_crop", manifest.get("demo_crop")), demo_size)
            target = output / (name + ".mp4")
            render(
                reaction, demo, reaction_edit, demo_edit, demo_framing,
                (reaction_audio and variant.get("reaction_audio", True), demo_audio),
                subtitles, target,
            )
            print(target)
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Render failed: {error}\n")


if __name__ == "__main__":
    main()

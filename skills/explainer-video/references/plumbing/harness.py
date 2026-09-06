"""Render harness: preview/full renders, beat timing report, contact sheet.

Usage:
  python harness.py --preview [--upto s2b] [--skip-holds] [--sheet]
  python harness.py --full

Adapt SCENE and MANIMGL to the project. The timing report is the edit:
if the title beat outruns the mechanism beat, you can see it without
watching anything.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
SCENE = os.environ.get("SCENE", "Explainer")
MANIMGL = Path(os.environ.get("MANIMGL", HERE.parent / "manim" / ".venv" / "bin" / "manimgl"))


def run(args):
    env = os.environ.copy()
    if args.upto:
        env["UPTO"] = args.upto
    if args.skip_holds:
        env["SKIP_HOLDS"] = "1"
    env["BEAT_OFFSETS_OUT"] = str(HERE / "beat_offsets.json")
    res = "640x360" if args.preview else "1920x1080"
    fps = "12" if args.preview else "30"
    cmd = [str(MANIMGL), "scenes.py", SCENE, "-w", "--resolution", res, "--fps", fps]
    print(" ".join(cmd))
    r = subprocess.run(cmd, cwd=HERE, env=env)
    if r.returncode != 0:
        sys.exit(r.returncode)

    off = json.loads((HERE / "beat_offsets.json").read_text())
    durs = json.loads((HERE / "audio" / "durations.json").read_text())
    print("\nbeat   start    audio")
    for k, v in off["offsets"].items():
        print(f"{k:5s}  {v:7.2f}  {durs.get(k, 0):6.2f}")
    print(f"total: {off['total']:.2f}s")

    if args.sheet:
        sheet()


def sheet():
    video = HERE / "videos" / f"{SCENE}.mp4"
    out = HERE / "sheets"
    out.mkdir(exist_ok=True)
    for f in out.glob("f_*.png"):
        f.unlink()
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(video),
                    "-vf", "fps=1/2,scale=480:-1", str(out / "f_%03d.png")],
                   check=True)
    n = len(sorted(out.glob("f_*.png")))
    cols = 5
    rows = (n + cols - 1) // cols
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(out / "f_%03d.png"),
                    "-frames:v", "1", "-filter_complex", f"tile={cols}x{rows}",
                    str(out / "sheet.png")], check=True)
    print(f"sheet: {out/'sheet.png'} ({n} frames)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--upto")
    ap.add_argument("--skip-holds", action="store_true")
    ap.add_argument("--sheet", action="store_true")
    run(ap.parse_args())

"""Lay beat wavs at recorded offsets, loudnorm, mux, emit .srt and a transcript skeleton.

Usage: python assemble.py <video.mp4> <outdir>
Reads beat_offsets.json (recorded during render) + audio/*.wav + beats.py.
Fill the transcript's number-provenance table before shipping (SKILL.md, Correctness).
"""
import json
import re
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

from beats import BEATS

HERE = Path(__file__).parent
video = Path(sys.argv[1])
outdir = Path(sys.argv[2])
outdir.mkdir(parents=True, exist_ok=True)

off = json.loads((HERE / "beat_offsets.json").read_text())
offsets, total = off["offsets"], off["total"]

RATE = 22050  # piper's output rate; check the wavs if you change voices
buf = np.zeros(int((total + 0.5) * RATE), dtype=np.float64)
for key, subtitle, say in BEATS:
    if say is None or key not in offsets:
        continue
    with wave.open(str(HERE / "audio" / f"{key}.wav")) as w:
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    i = int(offsets[key] * RATE)
    buf[i:i + len(data)] += data.astype(np.float64)

raw = outdir / "narration_raw.wav"
with wave.open(str(raw), "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(RATE)
    w.writeframes(np.clip(buf, -32768, 32767).astype(np.int16).tobytes())

norm = outdir / "narration.wav"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(raw),
                "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000",
                str(norm)], check=True)

final = outdir / "final.mp4"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-i", str(norm),
                "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest",
                str(final)], check=True)


def ts(t):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int((s % 1) * 1000):03d}"


def split_cues(text, dur):
    """Split beat text into <=90-char cues, preferring sentence boundaries."""
    sents = re.split(r"(?<=[.?!]) ", text)
    parts = []
    for s in sents:                       # break over-long sentences evenly
        n = -(-len(s) // 90)
        while n > 1:
            cut = s.rfind(" ", 0, len(s) // n + 12)
            if cut <= 0:
                break
            parts.append(s[:cut])
            s = s[cut + 1:]
            n -= 1
        parts.append(s)
    cues, cur = [], ""
    for p in parts:                       # greedily merge short neighbours
        cand = (cur + " " + p).strip()
        if len(cand) > 90 and cur:
            cues.append(cur)
            cur = p
        else:
            cur = cand
    if cur:
        cues.append(cur)
    n = sum(len(c) for c in cues)
    spans, t = [], 0.0
    for c in cues:
        d = dur * len(c) / n
        spans.append((t, t + d, c))
        t += d
    return spans


durs = json.loads((HERE / "audio" / "durations.json").read_text())
srt_lines, idx = [], 1
transcript = ["# TITLE — transcript\n"]
for key, subtitle, say in BEATS:
    if subtitle is None or key not in offsets:
        continue
    start = offsets[key]
    transcript.append(f"**[{int(start//60)}:{start%60:05.2f}] {key}** — {subtitle}\n")
    for a, b, cue in split_cues(subtitle, durs[key]):
        srt_lines += [str(idx), f"{ts(start+a)} --> {ts(start+b)}", cue, ""]
        idx += 1

(outdir / "final.srt").write_text("\n".join(srt_lines))

transcript.append("""
## Number provenance

| on-screen number | source |
|---|---|
| FILL ME | every number on screen traces to a named source (SKILL.md, Correctness) |

## Declared simplifications (stated in narration)

- FILL ME
""")
(outdir / "transcript.md").write_text("\n".join(transcript))
print(f"final: {final}\nsrt: {outdir/'final.srt'}\ntranscript: {outdir/'transcript.md'}")

"""Synthesize each narration beat to wav and record durations.json.

Run BEFORE animating: seconds of work, and the durations set every beat's
floor length. Adapt VOICE to the downloaded model.
"""
import json
import subprocess
import sys
import wave
from pathlib import Path

from beats import BEATS

HERE = Path(__file__).parent
AUDIO = HERE / "audio"
AUDIO.mkdir(exist_ok=True)
VOICE = HERE / "voices" / "en_GB-alan-medium.onnx"

durations = {}
for key, subtitle, say in BEATS:
    if say is None:
        durations[key] = 0.0
        continue
    out = AUDIO / f"{key}.wav"
    subprocess.run(
        [sys.executable, "-m", "piper", "--model", str(VOICE),
         "--length-scale", "0.95", "--output-file", str(out)],
        input=say.encode(), check=True, cwd=HERE)
    with wave.open(str(out)) as w:
        durations[key] = w.getnframes() / w.getframerate()

(AUDIO / "durations.json").write_text(json.dumps(durations, indent=1))
for k, v in durations.items():
    print(f"{k}: {v:.2f}s")
print(f"total narration: {sum(durations.values()):.1f}s")

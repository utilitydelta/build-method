"""BeatMixin: narration owns the clock (pipeline.md).

Use alongside manimgl's Scene:

    class MyVideo(BeatMixin, Scene):
        def construct(self):
            self.init_beats(json.loads(Path("audio/durations.json").read_text()))
            with self.beat("s1a"):
                ...animations...
            if self.stopped: return   # after each beat, honours UPTO
            self.write_offsets()

Env: UPTO=<key> stops after that beat; SKIP_HOLDS=1 drops the audio holds
(fast layout iteration); BEAT_OFFSETS_OUT overrides the output path.
"""
import json
import os
from contextlib import contextmanager
from pathlib import Path


class BeatMixin:
    def init_beats(self, durations):
        self.beat_offsets = {}
        self._durations = durations
        self.stopped = False

    @contextmanager
    def beat(self, key):
        self.beat_offsets[key] = float(self.time)
        yield
        if not os.environ.get("SKIP_HOLDS"):
            # hold for the audio plus a breath; never less than the audio
            hold = (self._durations.get(key, 0.0)
                    - (self.time - self.beat_offsets[key]) + 0.5)
            if hold > 0:
                self.wait(hold)
        if os.environ.get("UPTO") == key:
            self.stopped = True

    def write_offsets(self, path="beat_offsets.json"):
        out = os.environ.get("BEAT_OFFSETS_OUT", path)
        Path(out).write_text(json.dumps(
            {"offsets": self.beat_offsets, "total": float(self.time)}, indent=1))

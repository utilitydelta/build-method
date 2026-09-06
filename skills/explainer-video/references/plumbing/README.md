# Plumbing templates

The content-independent half of a narrated build: render harness, narration synthesis, audio
assembly with srt/transcript, and the beat mixin that makes narration own the clock. In a
measured 33-minute build (2026-08, the preempt-timer explainer), authoring exactly these from
the prose description cost real minutes and produced the same files every video needs — so they
live here now. Copy them into the project dir and adapt; they are starting points, not a
framework. The scene itself stays yours.

- `narrated_scene.py` — `BeatMixin`: records each beat's actual start from `self.time`, holds
  for at least the beat's audio, writes `beat_offsets.json`. `UPTO=<key>` stops after a beat;
  `SKIP_HOLDS=1` drops audio holds for fast layout iteration.
- `synth.py` — piper each beat to `audio/<key>.wav`, record `durations.json`. Run this BEFORE
  animating: a three-minute script synthesises in seconds, and knowing every beat's floor
  duration up front is how timing gets designed in rather than retrofitted.
- `harness.py` — preview/full render, beat timing report, contact sheet. `--upto`, `--sheet`.
- `assemble.py` — lay wavs at recorded offsets (numpy + wave), loudnorm, mux, emit `.srt` from
  the same beat data, and a transcript skeleton (fill the number-provenance table per the
  correctness rules in SKILL.md).

Beats file schema (`beats.py`): `BEATS = [(key, subtitle, say), ...]` — `subtitle` is what the
`.srt` shows, `say` is what the synthesiser reads (spell out `CRC32C`, `p99`, units), `say=None`
for deliberate silence. `DUR` in the scene comes from `audio/durations.json`.

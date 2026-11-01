#!/usr/bin/env python3
"""Detect acoustic silences using FFmpeg, with no NumPy or shared temp files.
Pauses are NOT sentence boundaries or a transcript alignment.
Usage: find_pauses.py input.mp3 output.json [--threshold-db -35 --minimum .3]
"""
import argparse
import json
import re
import subprocess
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('audio', type=Path)
    p.add_argument('output', type=Path)
    p.add_argument('--threshold-db', type=float, default=-35)
    p.add_argument('--minimum', type=float, default=.3)
    a = p.parse_args()
    if a.minimum <= 0 or a.threshold_db >= 0:
        p.error('minimum must be positive and threshold-db negative')
    dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', str(a.audio)]))
    result = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(a.audio), '-af', f'silencedetect=noise={a.threshold_db}dB:d={a.minimum}', '-f', 'null', '-'], capture_output=True, text=True, check=True)
    pauses = []; start = None
    for line in result.stderr.splitlines():
        found = re.search(r'silence_start: ([\d.]+)', line)
        if found:
            start = float(found[1])
        found = re.search(r'silence_end: ([\d.]+)', line)
        if found and start is not None:
            end = float(found[1]); pauses.append({'start': start, 'end': end, 'dur': round(end-start, 6)}); start = None
    if start is not None:
        pauses.append({'start': start, 'end': dur, 'dur': dur-start})
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps({'duration_s': dur, 'method': 'ffmpeg_silencedetect', 'threshold_db': a.threshold_db, 'minimum_s': a.minimum, 'warning': 'Acoustic silence candidates only; not sentence or word alignment.', 'pauses': pauses}, indent=2)+'\n')
    print(f'{len(pauses)} silence intervals written to {a.output}')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Preserve the supplied reference picture exactly and add the supplied audio.
This is a mux, NOT a newly generated animation. Video packets are copied.
"""
import argparse
import json
import subprocess
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('video', type=Path)
    p.add_argument('audio', type=Path)
    p.add_argument('output', type=Path)
    args = p.parse_args()
    meta = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(args.video)]))
    duration = float(meta['format']['duration'])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'warning', '-y', '-i', str(args.video), '-i', str(args.audio), '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-af', f'apad,atrim=duration={duration}', '-c:a', 'aac', '-b:a', '192k', '-t', str(duration), '-movflags', '+faststart', '-metadata', 'comment=Supplied reference picture copied without re-encoding; supplied narration added. Not a code-generated reconstruction.', str(args.output)], check=True)
    print(f'Wrote {args.output} ({duration:.6f}s). Original video stream preserved.')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Extract the narration SRT from a supplied Markdown production blueprint."""
import argparse
import re
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('blueprint', type=Path)
p.add_argument('output', type=Path)
a = p.parse_args()
text = a.blueprint.read_text(encoding='utf-8')
blocks = re.findall(r'```srt\s*\n([\s\S]*?)```', text, flags=re.I)
if len(blocks) != 1:
    raise SystemExit(f'Expected exactly one fenced SRT block; found {len(blocks)}')
srt = blocks[0].strip() + '\n'
# The supplied cue 13 drops the hour field and uses a colon before milliseconds.
srt = srt.replace('01:08:500 --> 00:01:17,500',
                  '00:01:08,500 --> 00:01:17,500')
if len(re.findall(r'-->', srt)) != 64:
    raise SystemExit('Expected 64 narration cues')
a.output.parent.mkdir(parents=True, exist_ok=True)
a.output.write_text(srt, encoding='utf-8')
print(f'Wrote 64 cues to {a.output}')

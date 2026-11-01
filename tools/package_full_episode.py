#!/usr/bin/env python3
"""Bundle the completed full episode, editable toolkit, and reference evidence."""
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEM = 'Turag_Full_Episode'
video = ROOT / 'output' / f'{STEM}.mp4'
report = video.with_name(video.name + '.render.json')
if not video.exists() or not report.exists():
    raise SystemExit('Complete the guarded full-episode render first.')
info = json.loads(report.read_text())
if info.get('frames') != 19118:
    raise SystemExit('Unexpected frame count for this full episode.')
archive = ROOT.parent / 'Turag_Full_Episode_Toolkit.zip'
allowed_dirs = {'assets', 'audio', 'director', 'engine', 'episodes',
                'reference', 'script', 'tests', 'tools', 'output'}
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=3) as bundle:
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in {'node_modules', '__pycache__', '.git'} for part in rel.parts):
            continue
        if len(rel.parts) > 1 and rel.parts[0] not in allowed_dirs:
            continue
        if rel.parts[0] == 'output' and not rel.parts[1].startswith(STEM):
            continue
        if rel.parts[0] == 'engine' and path.suffix == '.html' and path.name not in {
            'player-template.html', f'{STEM}.html', 'character-sheet.html', 'animation-lab.html'
        }:
            continue
        if path.name.endswith('.partial.mp4'):
            continue
        bundle.write(path, Path('turag-video-kit') / rel)
with zipfile.ZipFile(archive) as bundle:
    bad = bundle.testzip()
    if bad:
        raise SystemExit(f'Archive integrity failed: {bad}')
print(json.dumps({'archive': str(archive), 'bytes': archive.stat().st_size}))

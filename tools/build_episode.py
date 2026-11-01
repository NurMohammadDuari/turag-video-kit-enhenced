#!/usr/bin/env python3
"""Build an offline, self-contained, seekable HTML episode from a JSON plan."""
import argparse
import base64
import json
import mimetypes
import re
from pathlib import Path
from prepare_episode import ROOT, validate, probe
from cast_registry import resolve_cast


def data_url(path):
    return 'data:' + (mimetypes.guess_type(path.name)[0] or 'application/octet-stream') + ';base64,' + base64.b64encode(path.read_bytes()).decode()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('episode', type=Path)
    p.add_argument('--output', required=True, type=Path)
    a = p.parse_args()
    ep = json.loads(a.episode.read_text(encoding='utf-8'))
    validate(ep)
    ep = resolve_cast(ep)
    if any(b.get('scene') == 'compose' for b in ep['beats']) and ep.get('planningStatus') != 'authored':
        raise ValueError('This is a planning scaffold. The AI must analyze each line, author/refine its shot, inspect style references, and set planningStatus=authored before building. See 08_DIRECTOR_RULES.md.')
    audio = (ROOT / ep['audio']).resolve()
    if probe(audio)+.15<ep['duration']:raise ValueError('Narration shorter than episode; refusing a silently padded full video')
    css = (ROOT / 'assets/fonts/fonts.css').read_text()
    css = re.sub(r'url\(([^)]+)\)', lambda m: 'url(' + data_url(ROOT / 'assets/fonts' / m[1]) + ')', css)
    template = (ROOT / 'engine/player-template.html').read_text(encoding='utf-8')
    code = '\n'.join((ROOT / 'engine' / name).read_text(encoding='utf-8') for name in ['characters.js', 'runtime.js', 'composer.js', 'custom-props.js', 'player.js'])
    out = template.replace('/* EMBED_FONTS */', css).replace('__EPISODE_JSON__', json.dumps(ep, ensure_ascii=False).replace('<', '\\u003c')).replace('__AUDIO_URL__', data_url(audio)).replace('/* EMBED_ENGINE */', code.replace('</script', '<\\/script'))
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(out, encoding='utf-8')
    print(f'Built {a.output}: {len(out.encode()) / 1024 / 1024:.1f} MiB, offline fonts + audio + complete renderer.')


if __name__ == '__main__':
    main()

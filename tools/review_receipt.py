"""Bind an AI's visual inspection record to the exact portable player reviewed."""
import argparse
import hashlib
import json
from pathlib import Path


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify(html, receipt, beat_ids):
    data = json.loads(Path(receipt).read_text())
    if data.get('htmlSha256') != digest(html):
        raise ValueError('Visual approval is stale: inspect the rebuilt player and record a new review.')
    records = data.get('shots', [])
    if len(records) != len(beat_ids) or {r.get('id') for r in records} != set(beat_ids):
        raise ValueError('Visual review must cover every shot exactly once.')
    for record in records:
        for key in ['meaning', 'style', 'motion', 'contact', 'timing']:
            if len(str(record.get(key, '')).split()) < 4:
                raise ValueError(f"{record.get('id')}: missing concrete {key} inspection")
        if record.get('unresolved') or record.get('approved') is not True:
            raise ValueError(f"{record.get('id')}: unresolved visual review")
    return data


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('html', type=Path)
    p.add_argument('notes', type=Path, help='JSON with shots array authored after visual inspection')
    p.add_argument('--output', required=True, type=Path)
    a = p.parse_args()
    notes = json.loads(a.notes.read_text())
    notes['htmlSha256'] = digest(a.html)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(notes, ensure_ascii=False, indent=2)+'\n')
    print(a.output)

"""Split an episode into editable scene briefs; safely reassemble reviewed edits."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
from prepare_episode import validate


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def split(manifest, directory):
    episode = json.loads(manifest.read_text(encoding='utf-8'))
    validate(episode)
    directory.mkdir(parents=True, exist_ok=False)
    entries = []
    for i, beat in enumerate(episode['beats']):
        filename = f'{i+1:04}.json'
        packet = {
            'index': i, 'sourceBeatHash': fingerprint(beat),
            'context': {
                'previousLine': episode['beats'][i-1]['scriptLine'] if i else None,
                'nextLine': episode['beats'][i+1]['scriptLine'] if i+1<len(episode['beats']) else None,
                'episodeDesign': episode.get('episodeDesign', {}),
                'cast': episode.get('cast', {}),
                'audio': episode['audio'],
                'referencePolicy': 'Inspect styleRefs. Invent missing artwork in the shared grammar.'},
            'beat': beat,
            'repairNotes': []}
        write_json(directory/filename, packet)
        entries.append({'index': i, 'id': beat['id'], 'file': filename})
    write_json(directory/'index.json', {'source': str(manifest.resolve()),
        'sourceHash': fingerprint(episode), 'scenes': entries})
    (directory/'README.md').write_text(
        '# Scene workspace\n\nEdit each packet’s beat, using its neighboring narration and shared episode design. '
        'Record concrete repairs in repairNotes. Keep id, cueIndex, scriptLine and cue ownership unchanged. '
        'Add missing shared artwork in engine/custom-props.js. These are scene-specific authoring packets, not templates. '
        'Merge creates a draft manifest; rebuild and visually review changed shots before approval.\n', encoding='utf-8')


def merge(manifest, directory, output):
    if output.resolve() == manifest.resolve() or output.exists():
        raise ValueError('Choose a new output file; source and existing revisions are preserved.')
    episode = json.loads(manifest.read_text(encoding='utf-8'))
    index = json.loads((directory/'index.json').read_text())
    if index['sourceHash'] != fingerprint(episode):
        raise ValueError('Source changed since split. Regenerate packets before merging.')
    if len(index['scenes']) != len(episode['beats']):
        raise ValueError('Scene count mismatch')
    result = copy.deepcopy(episode)
    changed = []
    seen = set()
    for entry in index['scenes']:
        i = entry['index']
        if type(i) is not int or i in seen or not 0 <= i < len(episode['beats']):
            raise ValueError('Invalid or duplicate scene index')
        seen.add(i)
        filename = entry['file']
        if Path(filename).name != filename:
            raise ValueError('Packet filename must be local')
        packet = json.loads((directory/filename).read_text(encoding='utf-8'))
        old, new = episode['beats'][i], packet['beat']
        if packet['index'] != i or packet['sourceBeatHash'] != fingerprint(old):
            raise ValueError('Packet provenance mismatch')
        for field in ['id', 'cueIndex', 'scriptLine', 't0', 't1']:
            if new.get(field) != old.get(field):
                raise ValueError(f'Scene {i+1}: changed protected field {field}')
        if fingerprint(new) != fingerprint(old):
            new.setdefault('review', {})['approved'] = False
            changed.append(old['id'])
        result['beats'][i] = new
    if changed:
        result['directorStatus'] = 'draft'
    result['sceneWorkspaceMerge'] = {'changed': changed, 'sourceHash': index['sourceHash']}
    validate(result)
    output.parent.mkdir(parents=True, exist_ok=True)
    write_json(output, result)
    return changed


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['split', 'merge'])
    parser.add_argument('manifest', type=Path)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.operation == 'split':
        split(args.manifest, args.directory)
        print(args.directory/'index.json')
    else:
        if not args.output: parser.error('merge requires --output')
        print(json.dumps({'changed': merge(args.manifest, args.directory, args.output)}))

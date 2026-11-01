#!/usr/bin/env python3
"""Import a UTF-8 script and audio into an editable, validated episode plan.

Timecoded Markdown and SRT are supported. Untimed scripts receive ESTIMATED
word-weighted timings, never a claim of speech recognition or forced alignment.
"""
import argparse
import json
import math
import hashlib
import shutil
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def probe(path):
    data = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(path)]))
    if not any(s['codec_type'] == 'audio' for s in data['streams']):
        raise ValueError('Input has no audio stream')
    return float(data['format']['duration'])


def seconds(value):
    parts = value.replace(',', '.').split(':')
    if any(float(v)<0 for v in parts) or float(parts[-1])>=60 or (len(parts)==3 and float(parts[1])>=60):raise ValueError('Invalid clock timestamp: '+value)
    return sum(float(v) * 60 ** i for i, v in enumerate(reversed(parts)))


def clean(value):
    return re.sub(r'\*+', '', value).strip()


def parse_script(text, duration):
    cues = []
    # User-provided Markdown [00:04 – 00:10] sentence.
    pattern = r'\[(\d{1,2}:\d{2}(?::\d{2})?(?:[.,]\d+)?)\s*[–—-]\s*(\d{1,2}:\d{2}(?::\d{2})?(?:[.,]\d+)?)\]\s*\*?\*?\s*(.*)'
    text=text.replace('\r\n','\n')
    for line in text.splitlines():
        found = re.search(pattern, line)
        if found:
            cues.append({'t0': seconds(found[1]), 't1': seconds(found[2]), 'text': clean(found[3])})
        elif re.search(r'\[\d.*[:–—]',line):
            raise ValueError('Malformed timestamped script line: '+line)
        elif cues and line.strip() and not line.lstrip().startswith('#'):
            cues[-1]['text'] += ' '+clean(line)

    if not cues:
        srt_count=0
        for block in re.split(r'\n\s*\n', text.strip()):
            found = re.search(r'(\d+:\d+:\d+[.,]\d+)\s*-->\s*(\d+:\d+:\d+[.,]\d+)\s*\n([\s\S]+)', block)
            if '-->' in block:srt_count+=1
            if found:
                cues.append({'t0': seconds(found[1]), 't1': seconds(found[2]), 'text': clean(found[3].replace('\n', ' '))})
        if srt_count!=len(cues):raise ValueError('Malformed SRT cue; refusing to drop narration')
    if cues:
        return cues, {'method': 'user_supplied_timecodes', 'verified': False, 'note': 'Timecodes are supplied editorial cues, not independently forced-aligned to speech.'}
    if '-->' in text or re.search(r'\[\d+:',text):
        raise ValueError('Unrecognized timecodes; refusing to silently estimate supplied timing')
    lines = [clean(s) for s in text.splitlines() if clean(s) and not s.lstrip().startswith('#')]
    if not lines:
        raise ValueError('Script contains no narration')
    weights = [max(1, len(s.split())) for s in lines]
    total = sum(weights)
    cursor = 0
    for line, weight in zip(lines, weights):
        end = cursor + duration * weight / total
        cues.append({'t0': round(cursor, 4), 't1': round(end, 4), 'text': line})
        cursor = end
    cues[-1]['t1'] = duration
    return cues, {'method': 'estimated_word_weight', 'verified': False, 'note': 'NOT speech alignment. Listen and adjust cues before final delivery; pause detection alone cannot align words.'}


def suggest_scene(text):
    groups = [('rice_field', ['ধান', 'হারভেস্ট', 'কৃষি']), ('garment', ['গার্মেন্ট', 'সেলাই', 'কাপড়']), ('robot_hand', ['রোবট']), ('doctors', ['ডাক্তার', 'হাসপাতাল']), ('government', ['সরকার', 'বিসিএস', 'নিয়োগ']), ('bank_atm', ['ব্যাংক', 'বিকাশ', 'টাকা পাঠা']), ('night_desk', ['কোড', 'ভিডিও', 'এডিটর']), ('survey', ['সার্ভে', 'গবেষণা']), ('laptop_tasks', ['ইউজ', 'স্কিল']), ('street', ['মানুষ', 'দেশ'])]
    return next((name for name, words in groups if any(w in text for w in words)), 'task_tiles')


def validate(episode):
    duration = episode['duration']
    if not isinstance(duration,(int,float)) or isinstance(duration,bool) or not math.isfinite(duration) or duration<=0:
        raise ValueError('Duration must be finite and positive')
    def finite_tree(value):
        if isinstance(value,float) and not math.isfinite(value):raise ValueError('Non-finite scene data')
        if isinstance(value,dict):
            for v in value.values():finite_tree(v)
        if isinstance(value,list):
            for v in value:finite_tree(v)
    finite_tree(episode)
    if 'progressDuration' in episode and episode['progressDuration']<duration:raise ValueError('progressDuration cannot be shorter than the excerpt')
    ids=[b.get('id') for b in episode['beats']]
    if any(not isinstance(i,str) or not i for i in ids) or len(set(ids))!=len(ids):raise ValueError('Beat IDs must be unique nonempty strings')

    composed = [b for b in episode['beats'] if b.get('scene') == 'compose']
    if composed:
        indices = [b.get('cueIndex') for b in composed]
        if any(type(i) is not int for i in indices) or len(composed) != len(episode['beats']) or indices != list(range(len(episode['cues']))):
            raise ValueError('Every cue needs exactly one composed shot with its cueIndex')
        for b in composed:
            if b.get('scriptLine') != episode['cues'][b['cueIndex']]['text']:
                raise ValueError('Shot scriptLine must match its narration cue')
            cue=episode['cues'][b['cueIndex']]
            if b['t0']>cue['t0']+1e-6 or b['t1']<cue['t1']-1e-6:raise ValueError('Composed beat must cover its own cue')
            if not isinstance(b.get('visualIntent'),str) or not b['visualIntent'].strip():raise ValueError('Composed beat needs visualIntent')
            objects=b.get('shot',{}).get('objects',[]);object_ids=[o.get('id') for o in objects]
            if any(not isinstance(i,str) or not i for i in object_ids) or len(set(object_ids))!=len(object_ids):raise ValueError('Object IDs must be unique nonempty strings')
            for o in objects:
                if any(type(o.get(k)) not in [int,float] for k in ['x','y']):raise ValueError('Object coordinates must be numeric')
                if 'attachTo' in o and o['attachTo'] not in object_ids:raise ValueError('Missing attachment target')
                for k in ['enter','exit','reveal']:
                    if k in o and (type(o[k]) not in [int,float] or o[k]<0):raise ValueError('Invalid object '+k)
                if 'exit' in o and o['exit']<=o.get('enter',0):raise ValueError('Object exits before it enters')
                for k in o.get('keyframes',[]):
                    if type(k.get('at')) not in [int,float] or k['at']<0:raise ValueError('Invalid keyframe time')
            if not b.get('shot', {}).get('objects'):

                raise ValueError('A composed shot must contain objects')
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError('Duration must be finite and positive')
    for field in ['cues', 'beats']:
        previous = 0
        for i, item in enumerate(episode[field]):
            a, b = item['t0'], item['t1']
            if not all(isinstance(n, (int, float)) and math.isfinite(n) for n in [a, b]) or a < 0 or b <= a or b > duration + 1e-6:
                raise ValueError(f'{field}[{i}] has invalid timing {a}..{b}')
            if field=='cues' and not str(item.get('text','')).strip():raise ValueError('Empty narration cue')
            if a < previous - .001:
                raise ValueError(f'{field}[{i}] overlaps the previous item')
            if field == 'beats' and abs(a - previous) > .001:
                raise ValueError(f'Gap before beats[{i}]: {previous}..{a}')
            previous = b
        if not episode[field]:
            raise ValueError(f'{field} is empty')
        if field=='cues' and duration-previous>3 and not episode.get('tailHoldReason'):
            raise ValueError('Script ends more than 3 seconds before audio. Supply the missing cues, or author tailHoldReason for a verified silent/outro hold.')
        if field == 'beats' and abs(previous - duration) > .001:
            raise ValueError('Beats must cover the entire episode')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--script', required=True, type=Path)
    p.add_argument('--audio', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--scene-plan', type=Path)
    args = p.parse_args()
    duration = probe(args.audio)
    cues, timing = parse_script(args.script.read_text(encoding='utf-8'), duration)
    if args.scene_plan:
        plan = json.loads(args.scene_plan.read_text(encoding='utf-8'))
        beats = plan['beats'] if isinstance(plan, dict) else plan
    else:
        beats = []
        for i, cue in enumerate(cues):
            # Cover gaps with the preceding cue's image; never invent speech.
            beats.append({'id': f'beat-{i + 1:03}', 't0': 0 if i == 0 else cue['t0'], 't1': cues[i + 1]['t0'] if i + 1 < len(cues) else duration, 'scene': 'compose', 'cueIndex': i, 'scriptLine': cue['text'], 'visualIntent': 'AI must compose the concrete meaning and action of this line.', 'shot': __import__('compose_episode').suggest(cue['text'], i), 'chapter': 1, 'chapterTitle': 'নতুন পর্ব', 'heading': '', 'label': '', 'items': []})
    def local_copy(source,folder):
        source=source.resolve()
        try:return str(source.relative_to(ROOT))
        except ValueError:
            digest=hashlib.sha256(source.read_bytes()).hexdigest()[:10]
            dest=ROOT/folder/(source.stem+'-'+digest+source.suffix)
            dest.parent.mkdir(parents=True,exist_ok=True)
            if not dest.exists():shutil.copy2(source,dest)
            return str(dest.relative_to(ROOT))
    episode = {'version': 2, 'planningStatus': 'scaffold', 'directorVersion': 1,
      'directorStatus': 'draft',
      'episodeDesign': {'thesis':'','emotionalArc':'','chapterArc':[],
        'castBible':{},'locationBible':{},'visualMotifs':[],
        'densityRhythm':'','chapterCardPlan':[],'continuityRisks':[]},
      'id': args.output.stem, 'title': args.script.stem, 'duration': duration,
      'fps': 30, 'width': 1280, 'height': 720,
      'audio': local_copy(args.audio,'audio'), 'script': local_copy(args.script,'script'),
      'timing': timing, 'cues': cues, 'beats': beats,
      'planning': 'Draft only. The operating AI must complete the director dossier, replace heuristic suggestions, inspect renders, run director_audit.py, then mark planningStatus authored and directorStatus approved.'}
    for beat in episode['beats']:
        beat['semanticAnalysis']={'actors':[],'action':'','setting':'','facts':[],
          'relationship':'','tone':'','negation':'','uncertainty':'','notes':''}
        beat['designDecision']={'alternatives':[],'mechanism':'','composition':'','visibleChange':'',
          'actionPeak':'','cameraPurpose':'','transition':'','why':''}
        beat['styleRefs']=[];beat['referenceUse']=[]
        beat['copyLedger']=[];beat['factBasis']=[]
        beat['animationPlan']={'primaryAction':'','motivation':'','anticipation':'','contact':'','weightShift':'','actionPeak':'','followThrough':'','secondaryMotion':'','gaze':'','cameraMotivation':'','intentionalHold':False,'holdReason':''}
        beat['continuity']={'cast':'','place':'','props':''}
        beat['review']={'start':'','middle':'','end':'','issues':[],'fixes':[],'approved':False}
    validate(episode)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(episode, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Wrote {len(cues)} cues, {len(beats)} beats, {duration:.3f}s to {args.output}. Timing: {timing["method"]}; verified=false.')


if __name__ == '__main__':
    main()

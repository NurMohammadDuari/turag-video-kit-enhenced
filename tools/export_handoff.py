"""Export exact cue subtitles and an editable scene timeline from the manifest."""
import argparse
import csv
import json
from pathlib import Path
from prepare_episode import validate


def timestamp(seconds):
    ms = round(seconds*1000)
    hours, ms = divmod(ms,3600000)
    minutes, ms = divmod(ms,60000)
    secs, ms = divmod(ms,1000)
    return f'{hours:02}:{minutes:02}:{secs:02},{ms:03}'


def export(episode, directory):
    validate(episode)
    directory.mkdir(parents=True,exist_ok=True)
    srt=[]
    for i,cue in enumerate(episode['cues']):
        if round(cue['t1']*1000)<=round(cue['t0']*1000):
            raise ValueError('Cue too short for millisecond subtitle resolution')
        srt.append(f'{i+1}\n{timestamp(cue["t0"])} --> {timestamp(cue["t1"])}\n{cue["text"]}\n')
    (directory/'captions.srt').write_text('\n'.join(srt),encoding='utf-8')
    with (directory/'timeline.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['id','start_seconds','end_seconds','chapter','script','visual_intent'])
        writer.writeheader()
        for b in episode['beats']:
            writer.writerow({'id':b['id'],'start_seconds':b['t0'],'end_seconds':b['t1'],'chapter':b.get('chapterTitle',''),
                             'script':b['scriptLine'],'visual_intent':b['visualIntent']})
    chapters=[];previous=None
    for b in episode['beats']:
        identity=(b.get('chapter'),b.get('chapterTitle',''))
        if identity!=previous:
            chapters.append({'at':b['t0'],'title':identity[1],'chapter':identity[0]});previous=identity
    (directory/'chapters.json').write_text(json.dumps(chapters,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (directory/'timing-provenance.json').write_text(json.dumps({'timing':episode.get('timing',{}),
        'duration':episode['duration'],'audio':episode['audio'],
        'note':'These exports preserve supplied manifest timing. Exporting subtitles does not independently verify speech alignment.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest',type=Path);p.add_argument('directory',type=Path);a=p.parse_args()
    export(json.loads(a.manifest.read_text(encoding='utf-8')),a.directory)
    print(a.directory)

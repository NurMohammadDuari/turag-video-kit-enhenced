#!/usr/bin/env python3
"""Add a director dossier scaffold and emit a whole-episode cue briefing."""
import argparse, json
from pathlib import Path

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('manifest',type=Path)
p.add_argument('--output',type=Path)
a=p.parse_args();data=json.loads(a.manifest.read_text(encoding='utf-8'))
data.setdefault('directorVersion',1);data['directorStatus']='draft'
data.setdefault('episodeDesign',{
 'thesis':'','emotionalArc':'','chapterArc':[],'castBible':{},'locationBible':{},
 'visualMotifs':[],'densityRhythm':'','chapterCardPlan':[],'continuityRisks':[]})
for beat in data['beats']:
 beat.setdefault('semanticAnalysis',{'actors':[],'action':'','setting':'','facts':[],
  'relationship':'','tone':'','negation':'','uncertainty':'','notes':''})
 beat.setdefault('designDecision',{'alternatives':[],'mechanism':'','composition':'','visibleChange':'',
  'actionPeak':'','cameraPurpose':'','transition':'','why':''})
 beat.setdefault('referenceUse',[])
 beat.setdefault('copyLedger',[]);beat.setdefault('factBasis',[])
 beat.setdefault('animationPlan',{'primaryAction':'','motivation':'','anticipation':'','contact':'','weightShift':'','actionPeak':'','followThrough':'','secondaryMotion':'','gaze':'','cameraMotivation':'','intentionalHold':False,'holdReason':''})
 old=beat.get('continuity')
 if not isinstance(old,dict):beat['continuity']={'cast':str(old or ''),'place':'','props':''}
 else:
  for key in ['cast','place','props']:old.setdefault(key,'')
 beat.setdefault('review',{'start':'','middle':'','end':'','issues':[],'fixes':[],'approved':False})
out=a.output or a.manifest;out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
brief=out.with_suffix('.director.md');lines=['# Director briefing: '+data.get('title',out.stem),'','Read the whole script before filling this file. Every answer must be reflected in the JSON and rendered shot.','']
for i,(cue,beat) in enumerate(zip(data['cues'],data['beats'])):
 prev=data['cues'][i-1]['text'] if i else '(opening)';nxt=data['cues'][i+1]['text'] if i+1<len(data['cues']) else '(ending)'
 lines += [f'## {i+1:03} · {cue["t0"]:.3f}–{cue["t1"]:.3f}',f'**Line:** {cue["text"]}',f'**Previous:** {prev}',f'**Next:** {nxt}','',
  '- What must the viewer understand?','- Who does what to which object?','- What visibly changes during the cue?','- Which fact, number, negation or uncertainty must be preserved?','- Account for every on-screen phrase in copyLedger and every data-like number in factBasis.','- What are two materially different ways to visualize it?','- Which reference mechanism fits, and why is it selected?','- What is the anticipation, contact, weight shift, action peak and follow-through?','- Where do head and gaze lead the action?','- What secondary motion and camera movement support the action?','- How does this enter from and leave for its neighbors?','- What did start/middle/end inspection reveal?','']
brief.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'manifest':str(out),'briefing':str(brief),'cues':len(data['cues']),'directorStatus':'draft'},indent=2))

"""Directed actions and continuity pass for the first-minute episode."""
import json,copy
from pathlib import Path
x=json.load(open('episodes/ep02-first-minute.json'))
for i,b in enumerate(x['beats']):
 for o in b['shot']['objects']:
  if o['type']=='office_station':
   o['phase']=o.get('variant',0)*1.73
   if i in [1,2] and o.get('z')==-2 and o.get('variant') in [2,3]:o['receiveAt']=5+(o.get('variant',0)-2)*.6
   if i==2 and o.get('z')==-2 and o.get('variant')==3:o['departAt']=10.3
  if o['type']=='person':
   if o.get('pose')=='walk':o['action']='carry';o['phase']=o.get('variant',0)*1.1
   if o.get('pose')=='phone':o['action']='phone';o['keyframes']=[{'at':0,'actionTime':b['t0']-36},{'at':b['t1']-b['t0'],'actionTime':b['t1']-36}]
   if o.get('pose')=='point':o['action']='explain'
   if o.get('pose')=='sit':o['action']='typing'
  if o['type']=='envelope':
   o.pop('motion',None);o['keyframes']=[{'at':0,'y':180,'opacity':0},{'at':.55,'y':263,'opacity':1},{'at':1.4,'y':287,'opacity':1},{'at':2.5,'y':309,'opacity':0}]
  if o.get('motion',{}).get('kind')=='walk' and i in [4,5]:o['motion']['offset']=b['t0']-17
 # Never move detached carry boxes beside workers: the rig draws a held box.
 if i in [4,5]:b['shot']['objects']=[o for o in b['shot']['objects'] if o['type']!='box']
 if i==5:
  n=next(o for o in b['shot']['objects'] if o['type']=='number');n.update(type='count_number',from_=0,to=120000,seconds=2.5)
 if i in [6,7]:
  for o in b['shot']['objects']:
   if o['type']=='bar':
    o['type']='stat_tower';o['accent']=i==7 and o.get('text')=='২০২৬';height=o['h'];o['keyframes']=[{'at':0,'h':2},{'at':1.15,'h':height}]
   if o['type']=='person':o.update(action='explain',rightHandFrames=[[0,.10,-.50],[.6,.27,-.64],[1.2,.36,-.78],[2.3,.35,-.76],[3.5,.20,-.56]])
 if i in [10,11,12,13]:
  # Actors continue their own task while the camera follows the narration.
  for o in b['shot']['objects']:
   if o['type']=='blackboard':o['y']=395
   if o['type']=='sewing_machine':o['y']=400
   if o['type']=='person' and o.get('role')=='doctor':
    o.update(action='explain',phase=.4,keyframes=[{'at':0,'actionTime':b['t0']-46},{'at':b['t1']-b['t0'],'actionTime':b['t1']-46}])
   elif o['type']=='person' and o.get('pose')=='point':
    o['x']=445;o.update(action='write',dir=1,keyframes=[{'at':0,'actionTime':b['t0']-49},{'at':b['t1']-b['t0'],'actionTime':b['t1']-49}])
   elif o['type']=='person' and o.get('pose')=='sit' and o['x']==690:
    o['x']=708;o.update(action='sew',phase=.7,keyframes=[{'at':0,'actionTime':b['t0']-52},{'at':b['t1']-b['t0'],'actionTime':b['t1']-52}])
   elif o['type']=='person' and o.get('pose')=='sit':o['action']='rest'
  b['shot']['objects'].append({'id':f'chalk-{i}','type':'chalk_strokes','x':515,'y':310,'enter':max(0,49-b['t0'])})
  b['shot']['objects'].append({'id':f'cloth-{i}','type':'sewing_fabric','x':761,'y':394,'enter':max(0,52-b['t0'])})
  if i==10:b['shot']['camera']={'x':480,'y':270,'zoom':1,'keyframes':[{'at':0,'x':480,'zoom':1},{'at':3.5,'x':480,'zoom':1},{'at':5,'x':248,'y':295,'zoom':1.28}]}
  if i==11:b['shot']['camera']={'x':248,'y':295,'zoom':1.28,'keyframes':[{'at':0,'x':248},{'at':2.5,'x':258,'zoom':1.4}]}
  if i==12:b['shot']['camera']={'x':258,'y':295,'zoom':1.4,'keyframes':[{'at':0,'x':258},{'at':.65,'x':490}]}
  if i==13:b['shot']['camera']={'x':490,'y':295,'zoom':1.4,'keyframes':[{'at':0,'x':490},{'at':.65,'x':738}]}
 # Give changes a continuous environmental hold instead of re-fading each room.
 for o in b['shot']['objects']:
  if o['type'] in ['office_windowwall','office_station','room_outline','bed','blackboard','desk','sewing_machine','tea_stall','palm'] or i in [10,11,12,13]:o['reveal']=.001
 b['visualIntent']+=' | Motion revision: staged articulated actor actions, attached held props, task-specific hand movement and continuous framing.'
x['title']='আপনার চাকরি কি আসলেই সেফ? · প্রথম মিনিট · সংশোধিত';x['id']='ep02-first-minute-revised';x['motionRevision']='Articulated two-bone arms; script-timed gestures and phone raise; asynchronous typing; held boxes; chalk writing; cloth-feed sewing; continuous inter-room camera; animated statistic geometry.'
Path('episodes/ep02-first-minute-revised.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')

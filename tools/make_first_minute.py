import copy,json
from pathlib import Path
x=json.load(open('episodes/ep02-composed.json'));x['audio']='audio/ep02_first_minute.mp3';x['id']='ep02-first-minute';x['title']='আপনার চাকরি কি আসলেই সেফ? · প্রথম ১ মিনিট';x['duration']=60;x['cues']=[copy.deepcopy(c) for c in x['cues'] if c['t0']<60];x['beats']=[copy.deepcopy(b) for b in x['beats'] if b['t0']<60]
for c in x['cues']:c['t1']=min(c['t1'],60)
for b in x['beats']:b['t1']=min(b['t1'],60)
def O(type,x,y=455,**kw):return dict(type=type,x=x,y=y,**kw)
def shot(i,backdrop,objects,camera=None,intent=None):
 b=x['beats'][i];b['shot']={'backdrop':backdrop,'floor':False,'objects':[dict(o,id=f'opening-{i}-{j}',enter=o.get('enter',0)) for j,o in enumerate(objects)],'links':[]}
 if camera:b['shot']['camera']=camera
 if intent:b['visualIntent']=intent
 else:b['visualIntent']=b['scriptLine']+' → '+', '.join(o['type'] for o in objects)
def office():return [O('office_windowwall',480,455,z=-20),*[O('office_station',-15+j*141,355,s=.93,variant=j,z=-5) for j in range(8)],*[O('office_station',30+j*166,461,s=1.10,variant=j+1,z=-2,color='#9B9DAE') for j in range(6)]]
shot(0,'night',office()+[O('label',57,143,text='আপনার চাকরি কি',align='left',size=65,maxWidth=760,color='#E9E4D2',revealFrom=35),O('label',57,218,text='আসলেই',align='left',size=65,maxWidth=320,color='#E9E4D2',enter=.12,revealFrom=35),O('label',305,218,text='সেফ?',align='left',size=65,maxWidth=240,color='#FF3D17',enter=.25,revealFrom=35)],camera={'x':480,'y':270,'zoom':1,'keyframes':[{'at':0,'zoom':1.02},{'at':4,'zoom':1}]})
shot(1,'night',office()+[O('card',440,170,w=570,h=47,text='২৬ অক্টোবর · মাইক্রোসফট',size=26),O('label',445,210,text='MICROSOFT · VOLUNTARY EXIT OFFER',size=13,color='#E9E4D2',maxWidth=540),*[O('envelope',175+j*158,305,scale=.55,enter=j*.23,motion={'kind':'float','amplitude':4,'speed':2}) for j in range(5)]])
shot(2,'night',office()+[O('card',445,160,w=450,h=52,text='টাকা নেন, চাকরি ছাড়েন।',size=29),*[O('envelope',175+j*158,305,scale=.55,motion={'kind':'float','amplitude':4,'speed':2}) for j in range(5)]])
shot(3,'night',office()+[O('workforce_card',665,397,active=25,text='১/৪',revealFrom=25)])
def walkers():return [O('person',100+j*155,445,h=135,role='extra',pose='walk',variant=j,motion={'kind':'walk','speed':24}) for j in range(5)]+[O('box',135+j*155,387,scale=.38,motion={'kind':'walk','speed':24}) for j in range(5)]
shot(4,'city',walkers())
shot(5,'city',walkers()+[O('number',210,180,text='১.২ লাখ',label='এআই-জনিত ছাঁটাই · ৯ মাস',size=70,w=300)])
shot(6,'city',[O('number',205,180,text='৫৫ হাজার',label='২০২৫ · পুরো বছর',size=68,w=300),O('bar',650,445,w=100,h=135,text='২০২৫',color='#8A8CA0'),O('person',540,445,h=139,role='extra',pose='point')])
shot(7,'city',[O('number',205,180,text='১.২ লাখ',label='২০২৬ · প্রথম ৯ মাস',size=68,w=300),O('bar',620,445,w=100,h=125,text='২০২৫',color='#8A8CA0'),O('bar',790,445,w=100,h=265,text='২০২৬',keyframes=[{'at':0,'h':125},{'at':1.2,'h':265}]),O('label',790,140,text='দুই গুণের বেশি',size=24,color='#FF3D17')])
def street():return [O('palm',465,371,scale=.78,z=-3),O('tea_stall',780,465,scale=.88),O('person',310,465,h=190,role='guide',pose='phone'),O('person',630,465,h=140,role='extra',pose='sit',variant=3),O('rickshaw',80,411,scale=.46,motion={'kind':'walk','speed':30},z=-1)]
shot(8,'street',street()+[O('shield',450,284,scale=.85),O('chat',515,225,text='আমার কাজ এআই পারবে না।',scale=.9)])
shot(9,'street',street()+[O('shield',450,284,scale=.85,cracked=True)],camera={'x':480,'y':270,'zoom':1,'keyframes':[{'at':0,'zoom':1},{'at':1.7,'zoom':1.06,'x':440}]})
def rooms():return [O('room_outline',190,453,label='ডাক্তার'),O('room_outline',480,453,label='টিচার'),O('room_outline',770,453,label='গার্মেন্টস'),O('person',124,450,h=150,role='doctor',pose='point'),O('bed',215,405,scale=.62),O('blackboard',495,314,scale=.8),O('person',419,450,h=151,role='extra',pose='point',variant=1),O('person',550,450,h=102,role='extra',pose='sit'),O('person',690,450,h=140,role='extra',pose='sit',variant=2),O('desk',755,450,monitor=False,scale=.82),O('sewing_machine',755,393,scale=.65)]
shot(10,'paper',rooms())
shot(11,'paper',rooms()+[O('shield',220,235,scale=.55)],camera={'x':290,'y':295,'zoom':1.15})
shot(12,'paper',rooms()+[O('shield',510,209,scale=.55)],camera={'x':490,'y':295,'zoom':1.15})
shot(13,'paper',rooms()+[O('shield',805,235,scale=.55)],camera={'x':690,'y':295,'zoom':1.15})
shot(14,'paper',[O('vector',480,455,shapes=[{'kind':'rect','x':-230,'y':-300,'w':460,'h':300,'fill':'#12141C'}]),O('label',480,141,text='AI LAB',size=15,maxWidth=200),O('orb',480,270,r=36),*[O('office_station',300+j*135,455,s=.9,ai=True,variant=j) for j in range(3)],O('clipboard',790,354,scale=.8,checked=1,enter=2.3)])
x['planningStatus']='authored';x['planning']='First-minute reference-informed composition pass. Script/audio supplied by user. Uses source-office density, grounded street details and adjacent profession-room camera framing. Timing retains supplied editorial timecodes.'
Path('episodes/ep02-first-minute.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
print(len(x['beats']),'shots; 60 seconds')

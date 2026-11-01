#!/usr/bin/env python3
"""Make a per-line editable scene-graph scaffold. An AI must refine visual meaning.
No language model API is hidden here; this deterministic suggestion pass is optional.
"""
import argparse, json
from pathlib import Path
from prepare_episode import validate

def object_(id, type, x, y=455, **kw):
    return dict(id=id,type=type,x=x,y=y,**kw)

def suggest(text, index):
    # Suggestions are composable objects, never a route into canned scene functions.
    objects=[]; backdrop='paper'
    def add(kind,x=520,y=455,**kw):
        objects.append(object_(f'object-{len(objects)+1}',kind,x,y,**kw))
    if any(w in text for w in ['হাসপাতাল','ডাক্তার','রোগী','নার্স']):
        add('hospital',730,label='হাসপাতাল');add('bed',400,414);add('person',290,role='doctor',pose='point');add('person',570,h=155,variant=2)
    elif any(w in text for w in ['ধান','কৃষ','হারভেস্ট']):
        backdrop='field';add('palm',130);add('person',330,pose='point',variant=3);add('person',590,pose='walk',variant=1);add('box',740,text='ধান')
    elif any(w in text for w in ['ক্যালেন্ডার','অক্টোবর','বছর','মাস','২০৩০']):
        add('calendar',650,390,text='২০৩০' if '২০৩০' in text else '২৬',label='সময়');add('person',325,role='guide',pose='point');add('clock' if False else 'paper_stack',470,count=6)
    elif any(w in text for w in ['ফোন','চ্যাট','বিকাশ','মোবাইল']):
        backdrop='street';add('person',290,role='guide',pose='phone');add('phone',580,340,scale=1.6,ai=True);add('chat',725,225,text='মানুষ মানুষই চায়' if 'মানুষ' in text else 'AI',scale=.85)
    elif any(w in text for w in ['ব্যাংক','এটিএম','কাস্টমার']):
        add('atm',730);add('desk',350);add('person',305,pose='sit',role='guide');add('person',495,variant=2);add('person',570,variant=3)
    elif any(w in text for w in ['রোবট','গার্মেন্ট','কাপড়','সেলাই']):
        backdrop='office';add('robot',650);add('desk',380,monitor=False);add('person',270,pose='sit',variant=2);add('box',440,385,color='#FF3D17')
    elif any(w in text for w in ['সরকার','বিসিএস','নিয়োগ','চেয়ার','ছাঁটাই','এডিটর']):
        backdrop='office';add('chair',590);add('desk',690);add('person',310,pose='walk',variant=1);add('paper_stack',730,382,count=10);add('label',590,240,text='চাকরি',size=34)
    elif any(w in text for w in ['কোড','ভিডিও','অফিস','ডেস্ক','সফটওয়্যার']):
        backdrop='night' if 'ভিডিও' in text else 'office';add('desk',420,ai=True);add('person',345,pose='sit',role='guide');add('orb',650,320);add('paper_stack',770)
    elif any(w in text for w in ['সার্ভে','রিসার্চ','গবেষণা','পার্সেন্ট','হিসাব','সংখ্যা','জন']):
        add('grid',460,365,count=40,cols=10,active=24);add('person',270,role='guide',pose='point');add('card',780,380,w=180,h=170,text='কাজের হিসাব',size=23)
    elif any(w in text for w in ['রিল্যাক্স','অজুহাত','সেফ','ভয়']):
        backdrop='city';add('person',360,role='guide',pose='phone');add('shield',640,320,cracked='না' in text);add('phone',795,395)
    else:
        # Abstract task objects; AI should replace these when a literal image fits.
        add('person',280,role='guide',pose='point');add('desk',590);add('orb',755,320);add('box',460,435,text='কাজ')
    # Preserve per-line identity, with staggered entrances and deterministic variation.
    for i,o in enumerate(objects):
        o['enter']=round(i*.12,2);o['revealFrom']=12;o['z']=i
        if o['type']=='person':o.setdefault('variant',(index+i)%4)
    return dict(backdrop=backdrop,objects=objects,links=[])

def compose(ep):
    ep['beats']=[]
    chapters=[(0,1,'চাকরি কি সেফ?'),(41,2,'সবার একটা অজুহাত'),(144,3,'কাজের বান্ডেল'),(233,4,'চাকরি যায় চুপচাপ'),(308,5,'অফিস ও ফ্যাক্টরি'),(432,6,'অন্য দিকটা'),(565,7,'আমাদের কী করার?')]
    for i,cue in enumerate(ep['cues']):
        start=0 if i==0 else cue['t0'];end=ep['cues'][i+1]['t0'] if i+1<len(ep['cues']) else ep['duration']
        chapter=next(c for c in reversed(chapters) if start>=c[0])
        ep['beats'].append(dict(id=f'line-{i+1:03}',t0=start,t1=end,scene='compose',cueIndex=i,scriptLine=cue['text'],visualIntent='Show the concrete subject and action of this narration line.',chapter=chapter[1],chapterTitle=chapter[2],shot=suggest(cue['text'],i)))
    ep['planning']='Per-line composed scene graphs. Initial object choices are heuristic suggestions, editable by AI. Not an automatic general language understanding model.'
    validate(ep)
    return ep

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('episode',type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args()
    ep=compose(json.loads(a.episode.read_text()));a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(ep,ensure_ascii=False,indent=2)+'\n');print(f'{len(ep["beats"])} per-line compositions -> {a.output}')
if __name__=='__main__':main()

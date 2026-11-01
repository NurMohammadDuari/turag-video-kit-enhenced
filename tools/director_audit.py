#!/usr/bin/env python3
"""Reject incomplete director dossiers and report common design failures."""
import argparse, collections, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

GENERIC=('show the concrete','ai must compose','→ person','→ label','→ grid','keyword','appropriate visual')
ACTIVE={'walk','phone','point','raise','typing','sew','write','carry','take','examine','explain'}
def words(value):return len(re.findall(r'\w+',str(value),re.UNICODE))
CONTENT_KEYS={'text','label','line1','line2','value','number'}
DATA_KEYS={'count','active','to','from_'}
def norm_number(value):
 table=str.maketrans('০১২৩৪৫৬৭৮৯','0123456789')
 return str(value).translate(table).replace(',','').replace(' ','')
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest',type=Path);p.add_argument('--report',type=Path);p.add_argument('--allow-draft',action='store_true');a=p.parse_args()
 ep=json.loads(a.manifest.read_text(encoding='utf-8'));errors=[];warnings=[]
 if ep.get('directorVersion')!=1:errors.append('directorVersion must be 1')
 if not a.allow_draft and ep.get('directorStatus')!='approved':errors.append('directorStatus must be approved')
 design=ep.get('episodeDesign',{})
 for key in ['thesis','emotionalArc','densityRhythm']:
  if words(design.get(key,''))<4:errors.append('episodeDesign.'+key+' is incomplete')
 for key in ['chapterArc','visualMotifs']:
  if not design.get(key):errors.append('episodeDesign.'+key+' is empty')
 signatures=collections.defaultdict(list);backdrops=collections.Counter();mechanisms=collections.Counter();props=collections.Counter()
 for i,b in enumerate(ep.get('beats',[])):
  label=f'beat {i+1:03}'
  sem=b.get('semanticAnalysis',{});dec=b.get('designDecision',{});rev=b.get('review',{});refs=b.get('styleRefs',[]);uses=b.get('referenceUse',[]);cont=b.get('continuity',{})
  for key in ['action','setting','relationship','tone']:
   if words(sem.get(key,''))<1:errors.append(f'{label}: semanticAnalysis.{key} missing')
  for key in ['mechanism','composition','visibleChange','actionPeak','transition','why']:
   if words(dec.get(key,''))<2:errors.append(f'{label}: designDecision.{key} too weak')
  alternatives=dec.get('alternatives',[])
  if len(alternatives)<2 or any(words(v)<2 for v in alternatives):errors.append(f'{label}: two meaningful visual alternatives required')
  if any(g in str(b.get('visualIntent','')).lower() for g in GENERIC):errors.append(f'{label}: generic visualIntent')
  if not refs or not all(isinstance(r,str) and r for r in refs):errors.append(f'{label}: styleRefs missing')
  for ref in refs:
   if isinstance(ref,str) and not (ROOT/ref).is_file():errors.append(f'{label}: styleRef does not exist: {ref}')
  if len(uses)!=len(refs) or any(words(u)<4 for u in uses):errors.append(f'{label}: referenceUse must explain every styleRef')
  copy=[str(o.get(k)) for o in b.get('shot',{}).get('objects',[]) for k in CONTENT_KEYS if o.get(k) not in [None,'']]
  ledger=b.get('copyLedger',[]);ledger_text=[str(v.get('text','')) for v in ledger if isinstance(v,dict)]
  for value in copy:
   if value not in ledger_text:errors.append(f'{label}: on-screen copy missing from copyLedger: {value!r}')
  for entry in ledger:
   if not isinstance(entry,dict) or entry.get('basis') not in {'script','derived','editorial','decorative'} or words(entry.get('explanation',''))<4:errors.append(f'{label}: invalid copyLedger entry')
  numeric=[]
  for o in b.get('shot',{}).get('objects',[]):
   for key in CONTENT_KEYS|DATA_KEYS:
    if key in o and (isinstance(o[key],(int,float)) or re.search(r'[0-9০-৯]',str(o[key]))):numeric.extend(re.findall(r'[0-9০-৯][0-9০-৯, ]*',str(o[key])))
  bases=b.get('factBasis',[]);known={norm_number(v.get('value','')) for v in bases if isinstance(v,dict)}
  for value in numeric:
   if norm_number(value) not in known:errors.append(f'{label}: number lacks factBasis: {value!r}')
  for entry in bases:
   if not isinstance(entry,dict) or entry.get('basis') not in {'script','derived','editorial','decorative'} or words(entry.get('explanation',''))<4:errors.append(f'{label}: invalid factBasis entry')
  animation=b.get('animationPlan',{})
  for key in ['primaryAction','motivation','anticipation','contact','weightShift','actionPeak','followThrough','secondaryMotion','gaze','cameraMotivation']:
   if words(animation.get(key,''))<2:errors.append(f'{label}: animationPlan.{key} too weak')
  if animation.get('intentionalHold') and words(animation.get('holdReason',''))<3:errors.append(f'{label}: intentional hold needs a reason')
  if not isinstance(cont,dict) or any(k not in cont for k in ['cast','place','props']):errors.append(f'{label}: continuity needs cast/place/props')
  for key in ['start','middle','end']:
   if words(rev.get(key,''))<3:errors.append(f'{label}: review.{key} lacks inspection evidence')
  if not rev.get('approved'):errors.append(f'{label}: review not approved')
  if rev.get('issues') and not rev.get('fixes'):errors.append(f'{label}: issues recorded without fixes')
  shot=b.get('shot',{});objects=shot.get('objects',[]);backdrops[shot.get('backdrop','')]+=1;mechanisms[dec.get('mechanism','')]+=1
  sig=(shot.get('backdrop'),tuple(sorted((o.get('type'),round(o.get('x',0)/20),round(o.get('y',0)/20)) for o in objects if o.get('type') not in {'label','number','count_number','chat'})))
  signatures[sig].append(i+1)
  for o in objects:props[o.get('type')]+=1
  people=[o for o in objects if o.get('type') in {'person','office_station'}]
  if people and not any(o.get('type')=='office_station' or o.get('action') in ACTIVE or o.get('pose') in ACTIVE or o.get('motion') or o.get('keyframes') for o in people):warnings.append(f'{label}: characters appear static')
  if len(objects)<2:warnings.append(f'{label}: very sparse composition')
 for ids in signatures.values():
  if len(ids)>1:warnings.append('Repeated arrangement: '+','.join(map(str,ids)))
 total=max(1,len(ep.get('beats',[])))
 for name,count in backdrops.items():
  if name not in {'paper',''} and count/total>.45:warnings.append(f'Backdrop {name!r} used in {count}/{total} cues')
 for name,count in mechanisms.items():
  if name and count/total>.30:warnings.append(f'Mechanism {name!r} used in {count}/{total} cues')
 for name,count in props.items():
  if name in {'orb','card'} and count/total>.65:warnings.append(f'Prop {name!r} may be a crutch: {count} uses')
 report={'manifest':str(a.manifest),'cues':len(ep.get('cues',[])),'errors':errors,'warnings':warnings,'counts':{'backdrops':backdrops,'mechanisms':mechanisms,'props':props},'passed':not errors}
 target=a.report or a.manifest.with_suffix('.director-report.json');target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
 raise SystemExit(0 if not errors else 2)
if __name__=='__main__':main()

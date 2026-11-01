#!/usr/bin/env python3
"""Package the finished toolkit and verify the completed video decode."""
import hashlib,json,subprocess,zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
video=root/'output/Turag_EP02_composed.mp4'
report=video.with_name(video.name+'.render.json')
if not report.exists():raise SystemExit('Render not complete; run this after the renderer reports success.')
subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(video),'-f','null','-'],check=True)
info=json.loads(report.read_text());info['full_decode_verified']=True;info['sha256']=hashlib.sha256(video.read_bytes()).hexdigest()
(root/'output/final-video-verification.json').write_text(json.dumps(info,indent=2)+'\n')
archive=root.parent/'Turag_Reference_Composer_v3.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=5) as z:
 for p in sorted(root.rglob('*')):
  if not p.is_file():continue
  rel=p.relative_to(root)
  if any(x in rel.parts for x in ['node_modules','__pycache__','.git']):continue
  if len(rel.parts)>1 and rel.parts[:2]==('output','qa'):continue
  if p.name.endswith('.partial.mp4'):continue
  z.write(p,Path('turag-video-kit')/rel)
with zipfile.ZipFile(archive) as z:
 bad=z.testzip()
 if bad:raise SystemExit('ZIP integrity error: '+bad)
print(json.dumps({'zip':str(archive),'zip_bytes':archive.stat().st_size,'video':str(video),'frames':info['frames'],'duration':info['duration'],'decode_verified':True}))

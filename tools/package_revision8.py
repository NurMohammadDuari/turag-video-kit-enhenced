"""Package the autonomous-director toolkit, latest sample and review evidence."""
from pathlib import Path
import zipfile,json
root=Path(__file__).resolve().parents[1];archive=root.parent/'Turag_Autonomous_Director_v8.zip'
video=root/'output/Turag_First_Minute_v8.mp4';report=video.with_name(video.name+'.render.json')
assert video.exists() and report.exists(),'Finish the v8 render before packaging'
assert json.loads(report.read_text())['frames']==1800
allowed={'Turag_First_Minute_v8-qa','Turag_First_Minute_v8-director-review'}
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=3) as z:
 for p in sorted(root.rglob('*')):
  if not p.is_file():continue
  r=p.relative_to(root)
  if any(k in r.parts for k in ['node_modules','__pycache__','.git']):continue
  if r.parts[0]=='output' and not (r.name.startswith('Turag_First_Minute_v8') or len(r.parts)>1 and r.parts[1] in allowed):continue
  if r.parts[0]=='engine' and p.suffix=='.html' and p.name not in ['player-template.html','Turag_First_Minute_v8.html','character-sheet.html']:continue
  if p.name.endswith('.partial.mp4'):continue
  z.write(p,Path('turag-video-kit')/r)
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print(archive,archive.stat().st_size)

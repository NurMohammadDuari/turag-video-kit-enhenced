"""Package current tools and reference evidence with the technical research preview."""
from pathlib import Path
import json
import zipfile
root=Path(__file__).resolve().parents[1]
archive=root.parent/'Turag_Research_Enhanced_Toolkit.zip'
video=root/'output/Turag_Research_Preview.mp4'
report=video.with_name(video.name+'.render.json')
if not video.exists() or not report.exists():raise SystemExit('Render the research preview first')
if json.loads(report.read_text())['frames']!=1800:raise SystemExit('Unexpected preview frame count')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=3) as z:
 for p in sorted(root.rglob('*')):
  if not p.is_file():continue
  r=p.relative_to(root)
  if any(v in r.parts for v in ['node_modules','__pycache__','.git']):continue
  if r.parts[0]=='output' and not (r.parts[1].startswith('Turag_Research_') or r.parts[1]=='animation-lab.png'):continue
  if r.parts[0]=='engine' and p.suffix=='.html' and p.name not in ['player-template.html','Turag_Research_Revision.html','character-sheet.html','animation-lab.html']:continue
  if p.name.endswith('.partial.mp4'):continue
  z.write(p,Path('turag-video-kit')/r)
 z.writestr('turag-video-kit/RESEARCH_DELIVERY.txt','Research enhancement package. Turag_Research_Preview.mp4 is a technically tested 60-second reconstruction, not a visually approved full episode or exact reference clone. Read 13_2026_WORKFLOW_RESEARCH.md and HOW_TO_USE.md.\n')
with zipfile.ZipFile(archive) as z:
 if z.testzip() is not None:raise SystemExit('Archive integrity failed')
print(archive)

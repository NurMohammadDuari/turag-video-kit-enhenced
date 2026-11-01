"""Package current code/reference evidence and the revised sample, omitting old renders."""
import zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
video=root/'output/Turag_First_Minute_Revised.mp4'
assert video.exists() and video.with_name(video.name+'.render.json').exists(), 'Render must finish before packaging'
out=root.parent/'Turag_Reference_Composer_v5.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=3) as z:
 for p in sorted(root.rglob('*')):
  if not p.is_file():continue
  rel=p.relative_to(root)
  if any(s in rel.parts for s in ['node_modules','__pycache__','.git']):continue
  if rel.parts[0]=='output' and not (rel.name.startswith('Turag_First_Minute_Revised') or len(rel.parts)>1 and rel.parts[1] in ['first-minute-fresh-qa','first-minute-action-qa']):continue
  if p.name.endswith('.partial.mp4'):continue
  z.write(p,Path('turag-video-kit')/rel)
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
print(out, out.stat().st_size)

#!/usr/bin/env python3
"""Decode and inventory every file in the two supplied image folders.
Pillow only. Individual JPEG hashes differ from source-video frame hashes.
"""
import csv,hashlib,json,math,re,sys,time
from pathlib import Path
from PIL import Image,ImageDraw,ImageStat,ImageChops
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'reference/folder_audit';BASE.mkdir(parents=True,exist_ok=True)
folders=[Path('/home/mint/Downloads/turag/video2_images'),Path('/home/mint/Downloads/turag/frames')]
allreports=[]
for folder in folders:
 out=BASE/folder.name;out.mkdir(exist_ok=True)
 files=sorted(p for p in folder.rglob('*') if p.is_file());errors=[];dims={}; hashes={};prev=None;selected=[];cutpoints=[];start=time.time();nimages=0
 with (out/'files.csv').open('w',newline='') as file:
  w=csv.writer(file);w.writerow(['relative_path','bytes','sha256','status','width','height','frame_number_filename','mean_r','mean_g','mean_b','mean_abs_diff_thumbnail','duplicate_of'])
  for i,p in enumerate(files):
   data=p.read_bytes();sha=hashlib.sha256(data).hexdigest();dup=hashes.get(sha,'');hashes.setdefault(sha,str(p.relative_to(folder)))
   try:
    with Image.open(p) as im:
     width,height=im.size;im.draft('RGB',(160,90));im.load();thumb=im.convert('RGB').resize((160,90));small=thumb.resize((80,45));means=ImageStat.Stat(small).mean
     diff=sum(ImageStat.Stat(ImageChops.difference(small,prev)).mean)/3 if prev is not None else 0;prev=small
     dims[f'{width}x{height}']=dims.get(f'{width}x{height}',0)+1;nimages+=1
     num=int(re.search(r'(\d+)(?=\.[^.]+$)',p.name)[1]) if re.search(r'(\d+)(?=\.[^.]+$)',p.name) else None
     w.writerow([str(p.relative_to(folder)),len(data),sha,'decoded',width,height,num,*[round(x,3) for x in means],round(diff,3),dup])
     if folder.name=='frames' or i%120==0:
      selected.append((p.name,thumb.copy()))
     if diff>24:cutpoints.append({'file':p.name,'index':i,'difference':round(diff,3)})
   except Exception as e:
    errors.append({'file':str(p),'error':str(e)});w.writerow([str(p.relative_to(folder)),len(data),sha,'error:'+str(e)])
   if (i+1)%2000==0:print(folder.name,i+1,'files decoded',flush=True)
 for page in range(math.ceil(len(selected)/24)):
  sheet=Image.new('RGB',(1280,6*195),'#12141c');d=ImageDraw.Draw(sheet)
  for j,(name,im) in enumerate(selected[page*24:(page+1)*24]):
   x=j%4*320;y=j//4*195;sheet.paste(im.resize((320,180)),(x,y));d.text((x+4,y+181),name,fill='white')
  sheet.save(out/f'overview_{page:02}.jpg',quality=87)
 report={'source':str(folder),'recursive_files':len(files),'decoded_images':nimages,'dimensions':dims,'unique_file_hashes':len(hashes),'byte_duplicate_files':len(files)-len(hashes),'errors':errors,'overview_images':len(selected),'overview_sheets':math.ceil(len(selected)/24),'overview_sampling':'every image' if folder.name=='frames' else 'every 120th filename (approximately 4s if sequential 30fps extraction); filenames are indices, not independently verified timestamps','large_visual_changes':cutpoints,'wall_seconds':round(time.time()-start,2),'visual_review_note':'Every image decoded using JPEG reduced-resolution decoding and measured; full source-video frames were decoded separately in reference/analysis.  Overview viewing is separate from exhaustive computational file coverage.'}
 (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n');allreports.append(report);print(json.dumps({k:report[k] for k in ['source','recursive_files','decoded_images','errors','overview_sheets']}),flush=True)
(BASE/'summary.json').write_text(json.dumps(allreports,indent=2)+'\n')

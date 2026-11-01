#!/usr/bin/env python3
"""Decode every reference frame, record metrics, and create a browsable frame atlas.
Requires ffmpeg/ffprobe, Python 3, Pillow and numpy. Never changes source media.
Usage: python3 tools/analyze_reference.py reference/video2/video2_picture_only.mp4
"""
import argparse, csv, hashlib, json, math, subprocess, sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W,H=320,180
TW,TH=160,90

def stamp(t):
    return f'{int(t)//60:02d}:{t%60:06.3f}'

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('video',type=Path)
    ap.add_argument('--output',type=Path,default=Path('reference/analysis'))
    args=ap.parse_args(); out=args.output; out.mkdir(parents=True,exist_ok=True)
    for folder in ['atlas','overview','keyframes']:(out/folder).mkdir(exist_ok=True)
    info=probe(args.video); vs=next(s for s in info['streams'] if s['codec_type']=='video')
    fps=float(Fraction(vs['avg_frame_rate']))
    times=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','frame=best_effort_timestamp_time,pkt_duration_time','-of','json',str(args.video)]))['frames']
    cmd=['ffmpeg','-v','error','-threads','2','-i',str(args.video),'-map','0:v:0','-vf',f'scale={W}:{H}:flags=area','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','pipe:1','-map','0:v:0','-fps_mode','passthrough','-f','framemd5','-y',str(out/'decoded_frames.framemd5')]
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    prev=None; palette=Counter(); metrics=[]; candidate=[]; overview=[]; atlas=None; atlas_n=0; sample_step=round(fps*2)
    csvf=(out/'frames.csv').open('w',newline=''); writer=csv.writer(csvf)
    writer.writerow(['frame','pts_seconds','timecode','mean_rgb_difference_0_255','changed_pixel_fraction_gt12','mean_luma_0_255','near_black_fraction','thumbnail_sha256','atlas_sheet','atlas_tile'])
    while True:
        raw=p.stdout.read(W*H*3)
        if not raw:break
        if len(raw)!=W*H*3:raise RuntimeError('Partial decoded frame')
        i=len(metrics); t=float(times[i].get('best_effort_timestamp_time',i/fps))
        a=np.frombuffer(raw,dtype=np.uint8).reshape(H,W,3)
        luma=(a[:,:,0]*.2126+a[:,:,1]*.7152+a[:,:,2]*.0722)
        if prev is None:diff=0.; changed=0.
        else:
            d=np.abs(a.astype(np.int16)-prev)
            diff=float(d.mean()); changed=float((d.max(axis=2)>12).mean())
        row={'frame':i,'t':t,'difference':round(diff,4),'changed':round(changed,5),'luma':round(float(luma.mean()),3),'black':round(float((luma<8).mean()),5)}
        metrics.append(row); prev=a.astype(np.int16)
        # Palette samples every second; quantization stabilizes antialiasing/compression.
        if i%round(fps)==0:
            q=(a[::2,::2,:]//8)*8
            keys=(q[:,:,0].astype(np.int32)<<16)+(q[:,:,1].astype(np.int32)<<8)+q[:,:,2]
            vals,counts=np.unique(keys,return_counts=True);palette.update(dict(zip(vals.tolist(),counts.tolist())))
        im=Image.frombytes('RGB',(W,H),raw)
        if i%100==0:
            atlas=Image.new('RGB',(TW*10,(TH+16)*10),'#111318'); ad=ImageDraw.Draw(atlas)
        k=i%100; x=(k%10)*TW;y=(k//10)*(TH+16)
        atlas.paste(im.resize((TW,TH),Image.Resampling.LANCZOS),(x,y))
        ad.text((x+3,y+TH+1),f'{i:05d}  {stamp(t)}',fill='#eeeeee')
        if k==99:
            atlas.save(out/'atlas'/f'frames_{i//100:03d}.jpg',quality=78);atlas_n+=1
        writer.writerow([i,f'{t:.6f}',stamp(t),f'{diff:.4f}',f'{changed:.5f}',f'{luma.mean():.3f}',f'{(luma<8).mean():.5f}',hashlib.sha256(raw).hexdigest(),f'frames_{i//100:03d}.jpg',k])
        if i%sample_step==0:
            overview.append((i,t,im.copy()))
        if diff>15 and changed>.3:
            candidate.append(row)
            # Save every candidate for reproducible scene-cut review.
            im.save(out/'keyframes'/f'cut_{i:05d}_{t:08.3f}.jpg',quality=90)
        if i%3000==0:print(f'Decoded {i} frames ({stamp(t)})',flush=True)
    if len(metrics)%100:
        atlas.save(out/'atlas'/f'frames_{(len(metrics)-1)//100:03d}.jpg',quality=78);atlas_n+=1
    csvf.close(); stderr=p.stderr.read().decode(); code=p.wait()
    if code:raise RuntimeError(stderr)
    if len(metrics)!=len(times):raise RuntimeError(f'Decoded {len(metrics)} but probe reports {len(times)}')
    for page in range(math.ceil(len(overview)/30)):
        sheet=Image.new('RGB',(W*5,(H+26)*6),'#111318');sd=ImageDraw.Draw(sheet)
        for k,(i,t,im) in enumerate(overview[page*30:(page+1)*30]):
            x=k%5*W;y=k//5*(H+26);sheet.paste(im,(x,y));sd.text((x+7,y+H+5),f'frame {i:05d}   {stamp(t)}',fill='white')
        sheet.save(out/'overview'/f'overview_{page:02d}.jpg',quality=90)
    md5=[]
    for line in (out/'decoded_frames.framemd5').read_text().splitlines():
        if line and not line.startswith('#'):md5.append(line.split(',')[-1].strip())
    duplicate_count=sum(a==b for a,b in zip(md5,md5[1:]));runs=[];start=0
    for i in range(1,len(md5)+1):
        if i==len(md5) or md5[i]!=md5[start]:
            if i-start>=2:runs.append({'start_frame':start,'end_frame':i-1,'frames':i-start,'start':metrics[start]['t'],'end':metrics[i-1]['t']+1/fps})
            start=i
    # Group nearby cut flashes into transition windows without pretending all are scene cuts.
    cutgroups=[]
    for r in candidate:
        if cutgroups and r['t']-cutgroups[-1]['end']<.4:
            cutgroups[-1]['end']=r['t'];cutgroups[-1]['frames'].append(r['frame'])
        else:cutgroups.append({'start':r['t'],'end':r['t'],'frames':[r['frame']]})
    total=sum(palette.values());colors=[{'hex':f'#{int(k):06X}','sample_share':round(v/total,5)} for k,v in palette.most_common(24)]
    summary={'source':str(args.video.resolve()),'source_sha256':hashlib.sha256(args.video.read_bytes()).hexdigest(),'source_width':vs['width'],'source_height':vs['height'],'fps':fps,'decoded_frames':len(metrics),'decoded_md5_rows':len(md5),'duration':float(info['format']['duration']),'last_frame_pts':metrics[-1]['t'],'first_frame_pts':metrics[0]['t'],'audio_streams':sum(s['codec_type']=='audio' for s in info['streams']),'exact_duplicate_adjacent_frames':duplicate_count,'unique_decoded_frame_hashes':len(set(md5)),'exact_hold_runs':runs,'candidate_transition_windows':cutgroups,'candidate_cut_threshold':{'mean_rgb_difference_gt':15,'changed_fraction_gt':.3,'metric_resolution':[W,H]},'palette_quantization':8,'palette_top':colors,'atlas_sheets':atlas_n,'atlas_every_frame':True,'overview_interval_seconds':2,'overview_sheets':math.ceil(len(overview)/30),'coverage_note':'Every encoded video frame was decoded and fingerprinted at full resolution. Metrics and atlas images use resized frames. Overview sheets sample one frame every two seconds. A visual review of these samples is not a manual inspection of every full-resolution frame.'}
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    (out/'scene_candidates.json').write_text(json.dumps(cutgroups,indent=2))
    (out/'palette.json').write_text(json.dumps(colors,indent=2))
    (out/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Turag: every-frame reference atlas</title><style>body{background:#111318;color:#e9e4d2;font:16px system-ui;margin:24px}input{width:140px;padding:8px}img{max-width:100%;image-rendering:auto}button{padding:8px;margin:6px}a{color:#83aaff}.bar{position:sticky;top:0;background:#111318;padding:8px}</style><h1>Every-frame reference atlas</h1><p>Every decoded frame has a thumbnail. Sheet tiles run left to right, then top to bottom. Each label shows the zero-based frame index and presentation time. Full-resolution details remain in the source video; thumbnails are inspection aids.</p><div class="bar"><button onclick="move(-1)">Previous 100</button><input id="f" type="number" min="0" value="0"><button onclick="go()">Go to frame</button><button onclick="move(1)">Next 100</button> <span id="s"></span></div><img id="im"><script>const count='''+str(len(metrics))+''';let page=0;function show(){page=Math.max(0,Math.min(Math.ceil(count/100)-1,page));document.getElementById('im').src='atlas/frames_'+String(page).padStart(3,'0')+'.jpg';document.getElementById('s').textContent='Frames '+(page*100)+'–'+Math.min(count-1,page*100+99)+' of '+count}function go(){page=Math.floor(Number(document.getElementById('f').value)/100);show()}function move(n){page+=n;show()}show()</script>''')
    print(json.dumps({k:summary[k] for k in ['decoded_frames','duration','unique_decoded_frame_hashes','exact_duplicate_adjacent_frames','atlas_sheets','overview_sheets']},indent=2))
if __name__=='__main__':main()

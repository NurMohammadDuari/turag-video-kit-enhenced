#!/usr/bin/env python3
"""Validate, build, check and render a complete AI-authored episode."""
import argparse,json,subprocess
from pathlib import Path
from prepare_episode import ROOT,validate,probe
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('episode',type=Path)
p.add_argument('--name',help='Output filename stem (default: manifest filename)')
p.add_argument('--check-only',action='store_true',help='Build and check without encoding MP4')
p.add_argument('--workers',type=int,choices=[1,2,3,4],default=1,help='Parallel renderer pages; choose according to available memory')
p.add_argument('--review-receipt',type=Path,help='Visual inspection record bound to the exact built player')
p.add_argument('--legacy-technical-check',action='store_true',help='Allow an old example without a director dossier; never use for a new deliverable')
a=p.parse_args();manifest=a.episode.resolve();ep=json.loads(manifest.read_text());validate(ep)
if ep.get('planningStatus')!='authored':raise SystemExit('AI must author and review the scene plan first; an importer scaffold cannot be rendered.')
if not a.legacy_technical_check:
 run_audit=['python3',ROOT/'tools/director_audit.py',manifest,'--report',ROOT/'output'/(manifest.stem+'-director-report.json')]
 subprocess.run([str(v) for v in run_audit],cwd=ROOT,check=True)
name=a.name or manifest.stem
if Path(name).name!=name or name in ['.','..']:raise SystemExit('--name must be a filename stem, not a path')
audio=(ROOT/ep['audio']).resolve()
if probe(audio)+.15<ep['duration']:raise SystemExit('Audio is shorter than the planned full video. Correct the plan or supply the complete audio.')
html=ROOT/'engine'/f'{name}.html';video=ROOT/'output'/f'{name}.mp4';qa=ROOT/'output'/f'{name}-qa'
def run(args):subprocess.run([str(v) for v in args],cwd=ROOT,check=True)
run(['python3',ROOT/'tools/build_episode.py',manifest,'--output',html])
run(['node',ROOT/'tools/qa_episode.js',html,qa])
run(['node',ROOT/'tools/director_review.js',html,ROOT/'output'/f'{name}-director-review'])
run(['node',ROOT/'tools/animation_review.js',html,ROOT/'output'/f'{name}-animation-review'])
run(['python3',ROOT/'tools/review_shot_variety.py',manifest])
run(['python3',ROOT/'tools/export_handoff.py',manifest,ROOT/'output'/f'{name}-handoff'])
if not a.check_only:
 from review_receipt import verify
 if not a.review_receipt:raise SystemExit('Review boards are ready. Inspect every shot, record tools/review_receipt.py notes, then pass --review-receipt. No final export is approved by field presence alone.')
 verify(html,a.review_receipt,[b['id'] for b in ep['beats']])
 run(['node',ROOT/'tools/render_mp4.js',html,audio,video,'--fps',str(ep.get('fps',30)),'--width',str(ep.get('width',1280)),'--workers',str(a.workers)])
 run(['ffmpeg','-v','error','-i',video,'-f','null','-'])
print(json.dumps({'manifest':str(manifest),'preview':str(html),'video':str(video) if not a.check_only else None,'qa':str(qa),'duration':ep['duration']},indent=2))

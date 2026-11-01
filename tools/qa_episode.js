#!/usr/bin/env node
'use strict';
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const puppeteer=require('puppeteer-core'),{chromePath}=require('./render_mp4');
(async()=>{
  const [html='engine/episode.html',out='output/qa']=process.argv.slice(2);fs.mkdirSync(out,{recursive:true});
  const b=await puppeteer.launch({executablePath:chromePath(),headless:true,args:['--no-sandbox','--disable-dev-shm-usage','--font-render-hinting=none']});
  try{
    const p=await b.newPage(),errors=[],requests=[];p.on('pageerror',e=>errors.push(e.message));p.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url());});
    await p.goto(pathToFileURL(path.resolve(html)).href);await p.waitForFunction('window.__ready===true || window.__qa?.errors?.length',{timeout:60000});const failure=await p.evaluate(()=>window.__qa.errors);if(failure.length)throw Error(failure.join('\n'));
    const report=await p.evaluate(()=>{
      const ep=window.EPISODE,cv=document.getElementById('c'),points=new Set([0,ep.duration-1/30]);
      for(const b of ep.beats)for(const t of [b.t0,b.t0+.1,(b.t0+b.t1)/2,b.t1-1/30])points.add(Math.max(0,Math.min(ep.duration-1e-5,t)));
      for(const c of ep.cues)for(const t of [c.t0,(c.t0+c.t1)/2,c.t1-.01])points.add(t);
      // Sample the authored events, not just evenly spaced stills. Short hand
      // transitions and chapter-card exits can fall between ordinary samples.
      const eventTimes=[];
      for(const beat of ep.beats){const localEvents=[0,beat.t1-beat.t0];for(const o of beat.shot?.objects||[]){const enter=o.enter||0;localEvents.push(enter);if(o.exit!==undefined)localEvents.push(o.exit);for(const f of o.keyframes||[])localEvents.push(f.at);for(const a of o.actions||[])localEvents.push(enter+a.at,enter+a.at+(a.blend??.2));for(const key of ['rightHandFrames','leftHandFrames'])for(const f of o[key]||[])localEvents.push(enter+f[0]);}for(const f of beat.shot?.camera?.keyframes||[])localEvents.push(f.at);for(const local of localEvents)if(local>=0&&local<=beat.t1-beat.t0){const at=beat.t0+local;eventTimes.push(at);for(const offset of [-1/(ep.fps||30),0,1/(ep.fps||30)])points.add(Math.max(0,Math.min(ep.duration-1e-5,at+offset)));}}
      let maxMs=0,blank=[];const samples=[];for(const t of [...points].sort((a,b)=>a-b)){const st=performance.now();window.seek(t);maxMs=Math.max(maxMs,performance.now()-st);const px=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data;let lo=255,hi=0;for(let i=0;i<px.length;i+=400){lo=Math.min(lo,px[i]);hi=Math.max(hi,px[i]);}if(hi-lo<15)blank.push(t);}
      let nondeterministic=[];for(const beat of ep.beats){const t=(beat.t0+beat.t1)/2;window.seek(t);const before=cv.toDataURL();window.seek(0);window.seek(ep.duration-1);window.seek(t);if(before!==cv.toDataURL())nondeterministic.push(t);samples.push({id:beat.id,scene:beat.scene,t});}
      return {duration:ep.duration,beats:ep.beats.length,cues:ep.cues.length,sceneTypes:[...new Set(ep.beats.map(b=>b.scene))],testedTimes:points.size,authoredEventTimes:[...new Set(eventTimes)].sort((a,b)=>a-b),maxDrawMs:maxMs,blank,nondeterministic,samples,...window.__qa};
    });
    report.browserErrors=errors;report.networkRequests=requests;
    for(const s of report.samples){const img=await p.evaluate(t=>{window.seek(t);return document.getElementById('c').toDataURL('image/jpeg',.9).split(',')[1];},s.t);fs.writeFileSync(path.join(out,`${s.id}-${s.scene}.jpg`),Buffer.from(img,'base64'));}
    fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({...report,samples:`${report.samples.length} saved frames`},null,2));
    if(errors.length||report.errors.length||report.blank.length||report.nondeterministic.length||requests.length||report.maxSubtitleWidth>840)throw Error('QA failed; inspect report.json');
  }finally{await b.close();}
})().catch(e=>{console.error(e.stack);process.exitCode=1;});

#!/usr/bin/env node
/* Deterministic offline renderer; Node 22.12+, puppeteer-core, Chrome, FFmpeg. */
'use strict';
const fs=require('fs'),path=require('path'),os=require('os');
const {spawn,execFileSync}=require('child_process'),{pathToFileURL}=require('url');
const puppeteer=require('puppeteer-core');
function chromePath(){
  if(process.env.CHROME_PATH&&fs.existsSync(process.env.CHROME_PATH))return process.env.CHROME_PATH;
  for(const f of ['/usr/bin/google-chrome','/usr/bin/chromium','/usr/bin/chromium-browser','/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'])if(fs.existsSync(f))return f;
  throw Error('Set CHROME_PATH to an installed Chrome/Chromium executable.');
}
function run(cmd,args){return new Promise((resolve,reject)=>{const p=spawn(cmd,args,{stdio:['ignore','ignore','pipe']});let err='';p.stderr.on('data',d=>err=(err+d).slice(-12000));p.on('error',reject);p.on('close',c=>c===0?resolve():reject(Error(cmd+': '+err)));});}
async function main(){
  const [html,audio,out,...rest]=process.argv.slice(2);
  if(!out)throw Error('Usage: render_mp4.js episode.html audio.mp3 out.mp4 [--fps 30 --width 1280 --workers 2 --start 0 --duration 10]');
  const o={fps:30,width:1280,start:0,workers:1,crf:18};
  for(let i=0;i<rest.length;i+=2){let k=rest[i].replace(/^--/,'');if(!['fps','width','start','duration','workers','crf'].includes(k)||rest[i+1]===undefined)throw Error('Bad option '+rest[i]);o[k]=Number(rest[i+1]);}
  if(Object.values(o).some(x=>!Number.isFinite(x))||o.fps<1||o.fps>60||o.width<320||o.width>3840||o.width%32||o.start<0||o.workers<1||o.workers>4||!Number.isInteger(o.workers)||(o.duration!==undefined&&o.duration<=0)||o.crf<0||o.crf>51)throw Error('Invalid render settings');
  for(const f of [html,audio])if(!fs.existsSync(f))throw Error('Missing '+f);
  if([html,audio].some(f=>path.resolve(f)===path.resolve(out)))throw Error('Output must not overwrite an input');
  const output=path.resolve(out),pending=output+'.partial.mp4';fs.mkdirSync(path.dirname(output),{recursive:true});
  const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'turag-render-')),children=new Set();let browser;
  try{
    browser=await puppeteer.launch({executablePath:chromePath(),headless:true,args:['--no-sandbox','--disable-dev-shm-usage','--autoplay-policy=no-user-gesture-required','--font-render-hinting=none']});
    async function open(){const p=await browser.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));await p.setRequestInterception(true);p.on('request',r=>{if(/^https?:/.test(r.url())){errors.push('Remote asset blocked: '+r.url());r.abort();}else r.continue();});await p.goto(pathToFileURL(path.resolve(html)).href);await p.waitForFunction('window.__ready===true || window.__qa?.errors?.length',{timeout:60000});const failure=await p.evaluate(()=>window.__qa.errors);if(failure.length)throw Error(failure.join('\n'));await p.evaluate(w=>window.resize(w),o.width);return {p,errors};}
    const inputAudio=JSON.parse(execFileSync('ffprobe',['-v','error','-show_streams','-show_format','-of','json',path.resolve(audio)],{encoding:'utf8'}));if(!inputAudio.streams.some(s=>s.codec_type==='audio'))throw Error('Input has no audio stream');
    const first=await open(),D=await first.p.evaluate(()=>window.DURATION);if(o.start>=D)throw Error('Start outside episode');
    const duration=Math.min(o.duration??D-o.start,D-o.start),frames=Math.ceil(duration*o.fps-1e-6),workers=Math.min(o.workers,frames),segments=[];if(Number(inputAudio.format.duration)+.15<o.start+frames/o.fps)throw Error('Narration is shorter than the requested video; refusing to silently pad missing narration');let complete=0;const began=Date.now();
    const timer=setInterval(()=>console.log(`${complete}/${frames} frames (${(100*complete/frames).toFixed(1)}%), ${(complete/((Date.now()-began)/1000)).toFixed(1)} fps`),15000);
    try{await Promise.all(Array.from({length:workers},async(_,wi)=>{
      const {p,errors}=wi===0?first:await open(),a=Math.floor(frames*wi/workers),b=Math.floor(frames*(wi+1)/workers),dest=path.join(tmp,`seg-${wi}.mp4`);segments[wi]=dest;
      const ff=spawn('ffmpeg',['-hide_banner','-loglevel','error','-y','-f','image2pipe','-vcodec','mjpeg','-framerate',String(o.fps),'-i','pipe:0','-an','-c:v','libx264','-preset','fast','-threads','1','-crf',String(o.crf),'-pix_fmt','yuv420p','-fps_mode','cfr',dest],{stdio:['pipe','ignore','pipe']});children.add(ff);let err='';ff.stderr.on('data',d=>err+=d);ff.stdin.on('error',()=>{});
      const done=new Promise((res,rej)=>{ff.on('error',rej);ff.on('close',c=>{children.delete(ff);c===0?res():rej(Error('FFmpeg '+err));});});done.catch(()=>{});
      for(let i=a;i<b;i+=8){const jpgs=await p.evaluate(({i,end,fps,start})=>{const cv=document.getElementById('c'),images=[];for(let j=i;j<end;j++){window.seek(start+j/fps);images.push(cv.toDataURL('image/jpeg',.97).split(',')[1]);}return images;},{i,end:Math.min(i+8,b),fps:o.fps,start:o.start});
        for(const jpg of jpgs){if(ff.exitCode!==null)throw Error('Encoder exited '+err);if(!ff.stdin.write(Buffer.from(jpg,'base64')))await new Promise((res,rej)=>{const error=e=>{ff.stdin.off('drain',drain);rej(e);},drain=()=>{ff.stdin.off('error',error);res();};ff.stdin.once('drain',drain);ff.stdin.once('error',error);});complete++;}}
      ff.stdin.end();await done;if(errors.length)throw Error(errors.join('\n'));await p.close();
    }));}finally{clearInterval(timer);}
    const list=path.join(tmp,'segments.txt');fs.writeFileSync(list,segments.map(f=>`file '${f}'`).join('\n'));
    await run('ffmpeg',['-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',list,'-ss',String(o.start),'-i',path.resolve(audio),'-map','0:v:0','-map','1:a:0','-c:v','copy','-af',`apad,atrim=duration=${frames/o.fps}`,'-c:a','aac','-b:a','192k','-t',String(frames/o.fps),'-movflags','+faststart','-metadata','comment=Code-rendered toolkit reconstruction, not original reference pixels.',pending]);
    const meta=JSON.parse(execFileSync('ffprobe',['-v','error','-count_frames','-show_streams','-show_format','-of','json',pending],{encoding:'utf8'})),v=meta.streams.find(s=>s.codec_type==='video');
    if(!meta.streams.some(s=>s.codec_type==='audio')||Number(v.nb_read_frames)!==frames||v.width!==o.width||v.height!==o.width*9/16||Math.abs(Number(meta.format.duration)-frames/o.fps)>.15)throw Error('Output validation failed');
    fs.renameSync(pending,output);fs.writeFileSync(output+'.render.json',JSON.stringify({html:path.basename(html),audio:path.basename(audio),...o,frames,duration:frames/o.fps,wallSeconds:(Date.now()-began)/1000,streams:meta.streams},null,2)+'\n');
    console.log(`Verified ${output}: ${frames} frames, ${v.width}x${v.height}, ${frames/o.fps}s, AAC audio.`);
  }finally{for(const p of children)p.kill('SIGKILL');if(browser){await Promise.race([browser.close().catch(()=>{}),new Promise(r=>{const timer=setTimeout(()=>{browser.process()?.kill('SIGKILL');r();},4000);timer.unref();})]);}fs.rmSync(tmp,{recursive:true,force:true});fs.rmSync(pending,{force:true});}
}
if(require.main===module)main().catch(e=>{console.error(e.stack);process.exitCode=1;});
module.exports={chromePath};

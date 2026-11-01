/* Audio is the playback clock. Offline seeking is pure and never starts audio. */
(() => {
  'use strict';
  const ep = JSON.parse(document.getElementById('episode').textContent);
  const cv = document.getElementById('c'), ctx = cv.getContext('2d', {alpha:false});
  const voice = document.getElementById('voice'), scrub = document.getElementById('scrub');
  const play = document.getElementById('play'), status = document.getElementById('status');
  const P = {paper:'#E9E4D2',ink:'#12141C',red:'#FF3D17',blue:'#2F3BFF'};
  window.EPISODE = ep; window.DURATION = ep.duration; window.__ready = false;
  window.__qa = {fonts:[],errors:[],maxSubtitleWidth:0};
  const clamp = (n,a,b) => Math.min(b,Math.max(a,n));
  const time = n => `${String(Math.floor(n/60)).padStart(2,'0')}:${String(Math.floor(n%60)).padStart(2,'0')}`;
  function find(list,t) {let l=0,r=list.length-1;while(l<=r){const m=(l+r)>>1; if(t<list[m].t0)r=m-1;else if(t>=list[m].t1)l=m+1;else return list[m];}return null;}
  function subtitle(c,t) {
    const cue=find(ep.cues,t);if(!cue || !cue.text || cue.kind==='card')return;
    c.font='600 19px "Hind Siliguri"';c.textAlign='center';c.textBaseline='alphabetic';
    // Paginate at measured word boundaries; never squeeze or clip Bengali glyphs.
    const pages=[];let line='';
    for(const word of cue.text.split(/\s+/)){const trial=line?line+' '+word:word;if(line&&c.measureText(trial).width>810){pages.push(line);line=word;}else line=trial;}if(line)pages.push(line);
    const tx=pages[Math.min(pages.length-1,Math.floor((t-cue.t0)/(cue.t1-cue.t0)*pages.length))];
    const w=c.measureText(tx).width;window.__qa.maxSubtitleWidth=Math.max(window.__qa.maxSubtitleWidth,w);
    c.fillStyle='#0E1018';c.fillRect(480-w/2-13,485,w+26,33);c.fillStyle=P.red;c.fillRect(480-w/2-13,485,3,33);c.fillStyle='#fff';c.fillText(tx,480,508);
  }
  function chrome(c,t,b) {
    const dark=b.shot?.backdrop==='night'||['title_office','night_city','night_desk','empty_chair','end_card'].includes(b.scene);
    const fg=dark?P.paper:P.ink;
    c.strokeStyle=fg;c.globalAlpha=.33;c.lineWidth=.65;
    for(const [x,y] of [[22,22],[938,22],[22,518],[938,518]]){c.beginPath();c.arc(x,y,4,0,Math.PI*2);c.moveTo(x-7,y);c.lineTo(x+7,y);c.moveTo(x,y-7);c.lineTo(x,y+7);c.stroke();}
    c.globalAlpha=1;c.fillStyle=P.red;c.fillRect(0,0,960*t/(ep.progressDuration||ep.duration),2);
    [P.ink,P.blue,P.red,'#AAA99B'].forEach((x,i)=>{c.fillStyle=x;c.globalAlpha=.5;c.fillRect(40+i*9,517,7,5);});
    c.fillStyle=fg;c.font='400 7px "Space Mono"';c.textAlign='right';c.fillText(`${ep.episodeNumber?'EP.'+ep.episodeNumber:'SHOT'} · ${String(ep.beats.indexOf(b)+1).padStart(2,'0')}`,914,522);c.globalAlpha=1;
    const onChapterCard=b.shot?.objects?.some(o=>o.type==='chapter_card'&&t-b.t0+1e-9>=(o.enter||0)&&(o.exit===undefined||t-b.t0+1e-9<o.exit));
    if(!onChapterCard && b.scene!=='end_card' && !(b.scene==='title_office'&&t<4)){
      c.fillStyle=fg;c.fillRect(54,47,24,16);c.fillStyle=dark?P.ink:P.paper;c.textAlign='center';c.font='800 11px "Anek Bangla"';c.fillText(String(b.chapter||1).replace(/\d/g,d=>'০১২৩৪৫৬৭৮৯'[d]),66,59);
      c.fillStyle=fg;c.textAlign='left';c.font='600 11px "Hind Siliguri"';c.fillText(b.chapterTitle||'',86,60);
    }
    if(b.source){c.font='400 6.5px "Space Mono"';c.fillStyle=fg;c.globalAlpha=.55;c.textAlign='left';c.fillText(b.source.slice(0,130),54,473);c.globalAlpha=1;}
    subtitle(c,t);
  }
  window.seek = function(t) {
    t=clamp(Number(t)||0,0,ep.duration-1e-6);
    const b=find(ep.beats,t);if(!b)throw new Error(`No beat at ${t}`);
    ctx.setTransform(cv.width/960,0,0,cv.height/540,0,0);ctx.globalAlpha=1;ctx.setLineDash([]);ctx.textAlign='left';ctx.textBaseline='alphabetic';
    const index=ep.beats.indexOf(b),transition=b.shot?.transitionIn,duration=Math.max(.001,transition?.duration||0),u=clamp((t-b.t0)/duration,0,1),previous=index>0?ep.beats[index-1]:null;
    if(previous&&transition&&u<1){ctx.save();TuragScenes.draw(ctx,previous.t1-1e-6,previous);ctx.restore();ctx.save();if(transition.type==='wipe'){ctx.beginPath();const from=transition.from==='right'?960*(1-u):0;ctx.rect(from,0,960*u,540);ctx.clip();}else ctx.globalAlpha=u;TuragScenes.draw(ctx,t,b);ctx.restore();}
    else{ctx.save();TuragScenes.draw(ctx,t,b);ctx.restore();}
    ctx.save();chrome(ctx,t,b);ctx.restore();
    return b.id;
  };
  window.resize = function(w){cv.width=w;cv.height=w*9/16;window.seek(voice.currentTime||0);};
  window.scoreSound = () => {}; // Reference is picture-only: no invented soundtrack is enabled.
  const update = t => {window.seek(t);scrub.value=t;document.getElementById('time').textContent=`${time(t)} / ${time(ep.duration)}`;};
  function fail(e){window.__qa.errors.push(String(e));document.getElementById('error').textContent=String(e);status.textContent='Unable to load episode';}
  play.onclick=async()=>{try{if(!voice.paused){voice.pause();return;}if(voice.currentTime>=ep.duration-.1)voice.currentTime=0;await voice.play();}catch(e){fail(e);}};
  voice.onplay=()=>{play.textContent='Pause';};voice.onpause=()=>{play.textContent='Play';};voice.onended=()=>{update(ep.duration-.001);play.textContent='Replay';};
  voice.onerror=()=>fail(new Error('Narration could not be decoded'));
  scrub.oninput=()=>{voice.currentTime=+scrub.value;update(+scrub.value);};
  document.getElementById('mute').onclick=()=>{voice.muted=!voice.muted;document.getElementById('mute').textContent=voice.muted?'Unmute':'Mute';};
  const chapters=document.getElementById('chapters'), seen=new Set();
  for(const b of ep.beats){if(seen.has(b.chapter))continue;seen.add(b.chapter);const o=document.createElement('option');o.value=b.t0;o.textContent=`${time(b.t0)} · ${b.chapterTitle}`;chapters.appendChild(o);}
  chapters.onchange=()=>{voice.currentTime=+chapters.value;update(+chapters.value);};
  document.getElementById('title').textContent=ep.title;document.title=ep.title;scrub.max=ep.duration;
  const tick=()=>{if(!voice.paused){if(voice.currentTime>=ep.duration){voice.pause();update(ep.duration-.001);play.textContent='Replay';}else update(voice.currentTime);}requestAnimationFrame(tick);};
  (async()=>{try{
    for(const f of ['800 32px "Anek Bangla"','600 19px "Hind Siliguri"','400 10px "Space Mono"','700 10px "Space Mono"']){await document.fonts.load(f,'বাংলা কর্মী ক্ষ জ্ঞ ১২৩ Aa');if(!document.fonts.check(f))throw new Error('Missing font: '+f);window.__qa.fonts.push(f);}
    await document.fonts.ready;
    const supported=new Set(TuragScenes.names||[]);for(const b of ep.beats){if(supported.size&&!supported.has(b.scene))throw new Error('Unregistered scene: '+b.scene);if(b.scene==='compose')TuragComposer.validate(b.shot);}
    update(0);window.__ready=true;status.textContent=`${ep.beats.length} scenes · ${ep.cues.length} narration cues · offline fonts and audio · code recreation`;requestAnimationFrame(tick);
  }catch(e){fail(e);}})();
})();

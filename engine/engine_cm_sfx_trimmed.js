// CM + trimmed SFX kit used in my builds. The ORIGINAL full engine (full SFX, player with voiceover loader) is in the Nafay 3D Style Library prompt: attach that too.

const CM=(()=>{const clamp=(v,a=0,b=1)=>v<a?a:v>b?b:v,lerp=(a,b,u)=>a+(b-a)*u,hash=s=>{s=String(s);let h=2166136261;for(let i=0;i<s.length;i++)h=Math.imul(h^s.charCodeAt(i),16777619);return h>>>0};
const rng=seed=>{let a=typeof seed==='number'?seed>>>0:hash(seed);return()=>{a=(a+0x6D2B79F5)>>>0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}};return{clamp,lerp,rng}})();
const SFX=(()=>{function kit(ac,o={}){const SR=ac.sampleRate,T0=o.from||0,base=ac.currentTime+(o.lead||0),at=t=>base+t-T0;
const comp=ac.createDynamicsCompressor(),m=ac.createGain();m.gain.value=.8;comp.connect(m);m.connect(o.dest||ac.destination);
const nb=ac.createBuffer(1,SR*2,SR),d=nb.getChannelData(0),r=CM.rng('nz');for(let i=0;i<d.length;i++)d[i]=r()*2-1;
const env=(g,t,pk,du,a=.004)=>{g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(pk,t+a);g.gain.exponentialRampToValueAtTime(1e-4,t+du)};
const voice=(time,p)=>{const du=p.dur||.2,t=at(time);if(t+du<ac.currentTime)return;const os=ac.createOscillator();os.type=p.type||'sine';const f=p.f;if(Array.isArray(f)){os.frequency.setValueAtTime(f[0][1],t);for(let i=1;i<f.length;i++)os.frequency.exponentialRampToValueAtTime(f[i][1],t+f[i][0])}else os.frequency.value=f||440;const g=ac.createGain();env(g,t,p.gain||.3,du,p.a);os.connect(g);g.connect(comp);os.start(t);os.stop(t+du+.03)};
const hiss=(time,p)=>{const du=p.dur||.1,t=at(time);if(t+du<ac.currentTime)return;const s=ac.createBufferSource();s.buffer=nb;s.loop=true;const f=ac.createBiquadFilter();f.type=p.filter||'bandpass';f.Q.value=p.q||1;const ff=p.ff||1500;if(Array.isArray(ff)){f.frequency.setValueAtTime(ff[0],t);f.frequency.exponentialRampToValueAtTime(ff[1],t+du)}else f.frequency.value=ff;const g=ac.createGain();env(g,t,p.gain||.2,du,p.a);s.connect(f);f.connect(g);g.connect(comp);s.start(t,.3);s.stop(t+du+.03)};
return{voice,hiss}}
function live(score,from){const ac=new(window.AudioContext||window.webkitAudioContext)(),k=kit(ac,{from:from||0,lead:.04});score(k);return()=>{try{ac.close()}catch(e){}}}
async function render(score,dur,sr=48000){const len=Math.ceil(dur*sr),ac=new OfflineAudioContext(2,len,sr);score(kit(ac,{from:0}));const b=await ac.startRendering(),L=b.getChannelData(0),R=b.getChannelData(1),inter=new Float32Array(len*2);for(let i=0;i<len;i++){inter[2*i]=L[i];inter[2*i+1]=R[i]}return{inter,sr,frames:len}}
return{kit,live,render}})();


/* Script-driven scene graph: the AI authors each shot, the engine draws it.
 * A prop is a reusable object, never a fixed scene. Coordinates: 960 x 540. */
(function(g){'use strict';
const H=g.TuragScenes.helpers,P=g.TuragScenes.palette,props=new Map();
const {rect,line,poly,oval,text,mono,wrap}=H;
const register=(name,draw)=>{if(typeof name!=='string'||typeof draw!=='function')throw Error('Invalid prop registration');props.set(name,draw)};
register('person',(c,t,o)=>g.TuragCharacters.draw(c,{x:0,y:0,h:o.h||180,t,actionTime:o.actionTime??o.localTime,action:o.action,actions:o.actions,phase:o.phase,look:o.look,bodyLean:o.bodyLean,breathe:o.breathe,autoProps:o.autoProps,rightHandFrames:o.rightHandFrames,leftHandFrames:o.leftHandFrames,role:o.role||'extra',pose:o.pose||'stand',variant:o.variant||0,dir:o.dir||1,visor:o.visor,color:o.color,legColor:o.legColor}));
register('desk',(c,t,o)=>{rect(c,-65,-69,145,5,o.color||P.ink);line(c,-60,-64,-60,0,o.color||P.slate,3);line(c,74,-64,74,0,o.color||P.slate,3);if(o.monitor!==false)H.monitor(c,5,-128,61,o.ai);});
register('chair',(c,t,o)=>{const col=o.color||P.slate;line(c,-23,-108,-23,-40,col,3);line(c,-23,-40,28,-40,col,4);line(c,-20,-40,-20,0,col,3);line(c,24,-40,24,0,col,3)});
register('calendar',(c,t,o)=>{H.panel(c,-52,-122,104,122);rect(c,-52,-122,104,23,P.red);for(const x of [-29,29])line(c,x,-130,x,-113,P.ink,4);text(c,o.text||'',0,-36,51,P.ink,'center',92);if(o.label)text(c,o.label,0,-77,14,P.ink,'center',92);});
register('phone',(c,t,o)=>{rect(c,-24,-88,48,88,P.ink);rect(c,-19,-81,38,66,o.ai?P.blue:P.paper);oval(c,0,-7,3,3,P.paper);if(o.text)text(c,o.text,0,-48,17,o.ai?P.paper:P.ink,'center',34);});
register('chat',(c,t,o)=>{H.panel(c,-100,-99,200,88);poly(c,[[-65,-11],[-62,8],[-42,-11]],P.paper,P.ink);wrap(c,o.text||'',-85,-71,168,17,P.ink,23)});
register('atm',(c,t,o)=>{rect(c,-47,-174,94,174,P.slate);rect(c,-35,-160,70,65,P.blue);rect(c,-25,-84,50,7,P.ink);rect(c,-20,-57,40,19,P.paper);mono(c,o.label||'ATM',0,-114,15,P.paper,'center')});
register('hospital',(c,t,o)=>{H.building(c,-110,0,220,195,o.label||'হাসপাতাল');rect(c,-23,-174,46,12,P.red);rect(c,-6,-191,12,46,P.red);if(o.text)text(c,o.text,0,-210,23,P.green,'center',230)});
register('bed',(c)=>H.bed(c,-80,-20,160));
register('paper_stack',(c,t,o)=>H.paperStack(c,-32,0,o.count||12,o.w||50));
register('orb',(c,t,o)=>H.orb(c,0,-(o.r||34),o.r||34,t));
register('monitor',(c,t,o)=>H.monitor(c,-60,-103,120,o.ai));
register('palm',(c,t)=>H.palm(c,0,0,170,t));
register('building',(c,t,o)=>H.building(c,-60,0,120,o.h||190,o.label||'অফিস'));
register('shield',(c,t,o)=>H.shield(c,0,-64,65,t,!!o.cracked));
register('robot',(c,t)=>H.robot(c,0,0,160,t));
register('label',(c,t,o)=>text(c,o.text||'',0,0,o.size||32,o.color||P.ink,o.align||'center',o.maxWidth||400));
register('card',(c,t,o)=>{H.panel(c,-(o.w||230)/2,-(o.h||140),o.w||230,o.h||140,o.color||P.paper);wrap(c,o.text||'',-(o.w||230)/2+15,-(o.h||140)+34,(o.w||230)-30,o.size||24);});
register('number',(c,t,o)=>H.hero(c,o.text||'',o.label||'',-(o.w||180)/2,-90,o.size||68));
register('bar',(c,t,o)=>{const w=o.w||70,h=o.h||180;rect(c,-w/2,-h,w,h,o.color||P.blue);if(o.text)text(c,o.text,0,25,20,P.ink,'center',160)});
register('grid',(c,t,o)=>{const n=o.count??100,cols=o.cols||10;for(let i=0;i<n;i++){const x=(i%cols)*17,y=-Math.ceil(n/cols)*25+Math.floor(i/cols)*25;g.TuragCharacters.icon(c,x,y+22,24,i<(o.active??n)?(o.color||P.blue):P.pale)}});
register('box',(c,t,o)=>{rect(c,-28,-45,56,45,o.color||P.pale,P.ink);line(c,-28,-45,0,-30,P.ink);line(c,28,-45,0,-30,P.ink);if(o.text)text(c,o.text,0,-8,14,P.ink,'center',48)});
/* For previously unseen props the AI can register a function, or supply paths.
 * Only data primitives are allowed: no eval, scripts, remote images or HTML. */
const pathCache=new Map();
register('vector',(c,t,o)=>{for(const original of o.shapes||[]){const local=o.localTime??t;if(local<(original.enter??0)||local>=(original.exit??Infinity))continue;const s=interpolate(original,original.keyframes,local),color=s.fill||P.ink;c.save();c.globalAlpha*=Math.max(0,Math.min(1,s.opacity??1));c.translate(s.translateX??0,s.translateY??0);c.rotate((s.rotation??0)*Math.PI/180);c.scale(s.scale??1,s.scale??1);
 if(s.kind==='path'){if(typeof s.d!=='string'||!s.d.trim())throw Error('Vector path needs SVG path data');let p=pathCache.get(s.d);if(!p){p=new Path2D(s.d);if(pathCache.size>=256)pathCache.delete(pathCache.keys().next().value);pathCache.set(s.d,p);}if(s.fill!=='none'){c.fillStyle=color;c.fill(p,s.fillRule||'nonzero');}if(s.stroke){c.strokeStyle=s.stroke;c.lineWidth=s.width??1.5;c.lineCap=s.lineCap||'round';c.lineJoin='round';c.stroke(p);}}
 else if(s.kind==='rect')rect(c,s.x,s.y,s.w,s.h,color,s.stroke);else if(s.kind==='ellipse')oval(c,s.x,s.y,s.rx,s.ry,color);else if(s.kind==='line')line(c,s.x,s.y,s.x2,s.y2,s.stroke||color,s.width||2);else if(s.kind==='polygon')poly(c,s.points,color,s.stroke,s.width||1.5);else if(s.kind==='text')text(c,s.text,s.x,s.y,s.size||22,color,s.align||'left',s.maxWidth||200);else throw Error('Unknown vector primitive '+s.kind);c.restore();}});
function validate(shot){if(!shot||!Array.isArray(shot.objects))throw Error('compose requires shot.objects');const ids=new Set();for(const o of shot.objects){if(!o.id||ids.has(o.id))throw Error('Each object needs a unique id');ids.add(o.id);if(!props.has(o.type))throw Error('Unknown prop '+o.type+'; register it or draw vector shapes');for(const k of ['x','y'])if(!Number.isFinite(o[k]))throw Error('Object '+o.id+' needs finite '+k);}for(const o of shot.objects){
 if(o.type==='person'&&o.action&&!g.TuragCharacters.actionNames().includes(o.action))throw Error('Unknown character action '+o.action+' on '+o.id);
 if(o.type==='vector'){if(!Array.isArray(o.shapes)||!o.shapes.length)throw Error('Vector needs shapes');for(const s of o.shapes){if(!['path','rect','ellipse','line','polygon','text'].includes(s.kind))throw Error('Unknown vector primitive '+s.kind);if(s.kind==='path'&&(typeof s.d!=='string'||!s.d.trim()))throw Error('Vector path needs SVG path data');for(const key of ['translateX','translateY','rotation','scale','opacity','enter','exit'])if(s[key]!==undefined&&!Number.isFinite(s[key]))throw Error('Invalid vector '+key);if((s.scale??1)<0||(s.opacity??1)<0||(s.opacity??1)>1)throw Error('Invalid vector scale/opacity');if(s.exit!==undefined&&s.exit<=(s.enter??0))throw Error('Vector exit precedes entry');}}
 if(o.actions){if(o.type!=='person'||!Array.isArray(o.actions))throw Error('Action tracks require a person');let previous=-1;for(const a of o.actions){if(!Number.isFinite(a.at)||a.at<0||a.at<=previous||!g.TuragCharacters.actionNames().includes(a.action)||!Number.isFinite(a.blend??.2)||(a.blend??.2)<0)throw Error('Invalid action track on '+o.id);previous=a.at;}}
 if(o.attachTo){const parent=shot.objects.find(p=>p.id===o.attachTo);if(!parent||parent.type!=='person'||parent.attachTo)throw Error('Attachment requires a root person');if(o.hand&&!['left','right'].includes(o.hand))throw Error('Unknown hand');if(o.socket&&!['rightHand','leftHand','head','torso','pelvis'].includes(o.socket))throw Error('Unknown character socket');}
 for(const k of ['scale','rotation','opacity','enter','exit','reveal'])if(o[k]!==undefined&&!Number.isFinite(o[k]))throw Error('Invalid '+k+' on '+o.id);
 if((o.opacity??1)<0||(o.opacity??1)>1||(o.scale??1)<0)throw Error('Invalid opacity/scale on '+o.id);
 if(o.exit!==undefined&&o.exit<=(o.enter||0))throw Error('Exit precedes entry on '+o.id);
}
for(const target of [...shot.objects,...shot.objects.flatMap(o=>o.shapes||[]),...(shot.camera?[shot.camera]:[])]){const times=new Set();for(const k of target.keyframes||[]){if(!Number.isFinite(k.at)||k.at<0||times.has(k.at))throw Error('Invalid or duplicate keyframe time');times.add(k.at);for(const v of Object.values(k))if(typeof v==='number'&&!Number.isFinite(v))throw Error('Non-finite keyframe');}}
for(const l of shot.links||[])if(!ids.has(l.from)||!ids.has(l.to))throw Error('Link references absent object');}
function backdrop(c,t,s){H.bg(c,s.backdrop==='night');if(s.backdrop==='city'||s.backdrop==='street'){H.skyline(c,410,P.pale,false);if(s.backdrop==='street'){rect(c,0,371,960,110,'#676B7D');for(let x=0;x<960;x+=66)rect(c,x,424,34,3,P.paper);}}if(s.backdrop==='field'){rect(c,0,339,960,130,P.green);H.dots(c,0,339,960,130,P.paper,7,.65);oval(c,751,224,80,80,P.red);}if(s.backdrop==='office'){for(let x=60;x<940;x+=180){rect(c,x,100,140,144,P.pale);line(c,x+70,100,x+70,244,P.slate,3);}}if(s.floor!==false)H.floor(c,s.floorY||465,s.backdrop==='night');}
function interpolate(base,frames,time){
 const sorted=[...(frames||[])].sort((a,b)=>a.at-b.at),out={...base};
 const keys=new Set(sorted.flatMap(f=>Object.keys(f)).filter(k=>k!=='at'));
 for(const key of keys){let previous={at:0,value:base[key]};let next;
  for(const f of sorted){if(!(key in f))continue;if(f.at<=time+1e-9)previous={at:f.at,value:f[key]};else{next=f;break;}}
  out[key]=previous.value;
  if(next&&typeof previous.value==='number'&&typeof next[key]==='number'){const u=H.ease(Math.max(0,Math.min(1,(time-previous.at)/(next.at-previous.at))));out[key]=previous.value+(next[key]-previous.value)*u;}
 }
 return out;
}
function resolveObjects(shot,local,t){
 const objects=shot.objects.map(raw=>{
  const o={...interpolate(raw,raw.keyframes,local),localTime:local-(raw.enter||0)},age=o.localTime,enterDuration=(o.reveal??.35)||.001,enter=H.ease(Math.min(1,Math.max(0,age)/enterDuration)),exitDuration=o.exitDuration??.25,exit=o.exit===undefined?1:Math.max(0,Math.min(1,(o.exit-local)/Math.max(.001,exitDuration)));
  o.visible=local+1e-9>=(o.enter||0)&&(o.exit===undefined||local+1e-9<o.exit);o.drawAlpha=(o.instant?1:enter)*exit*(o.opacity??1);
  const motion=o.motion||{},phase=motion.phase||0,speed=motion.speed??2,amplitude=motion.amplitude??4,q=age*speed+phase;
  if(motion.kind==='walk')o.x+=(age+(motion.offset||0))*(motion.speed??18);
  if(motion.kind==='float'||motion.kind==='bob')o.y+=Math.sin(q)*amplitude;
  if(motion.kind==='shake'){o.x+=Math.sin(q*2.17)*amplitude;o.y+=Math.sin(q*2.91)*amplitude*.35;}
  if(motion.kind==='pendulum')o.rotation=(o.rotation||0)+Math.sin(q)*amplitude;
  if(motion.kind==='pulse')o.scale=(o.scale??1)*(1+Math.sin(q)*amplitude/100);
  if(motion.kind==='orbit'){o.x+=Math.cos(q)*(motion.radiusX??amplitude);o.y+=Math.sin(q)*(motion.radiusY??amplitude);}
  const revealOffset=(o.revealFrom||0)*(1-enter);o.y+=revealOffset;
  if(o.enterStyle==='slideLeft')o.x-=(1-enter)*(o.enterDistance??80);if(o.enterStyle==='slideRight')o.x+=(1-enter)*(o.enterDistance??80);if(o.enterStyle==='rise')o.y+=(1-enter)*(o.enterDistance??35);if(o.enterStyle==='scale')o.scale=(o.scale??1)*(.72+.28*enter);
  if(o.exit!==undefined&&exit<1){if(o.exitStyle==='slideLeft')o.x-=(1-exit)*(o.exitDistance??80);if(o.exitStyle==='slideRight')o.x+=(1-exit)*(o.exitDistance??80);if(o.exitStyle==='drop')o.y+=(1-exit)*(o.exitDistance??40);if(o.exitStyle==='scale')o.scale=(o.scale??1)*(1-.25*(1-exit));}
  return o;
 });
 const byId=new Map(objects.map(o=>[o.id,o]));
 for(const o of objects){if(!o.attachTo)continue;const parent=byId.get(o.attachTo);if(!parent||parent.type!=='person'||parent.attachTo)throw Error('Attachment must target a root person: '+o.id);const socket=o.socket||(o.hand==='left'?'leftHand':'rightHand'),point=g.TuragCharacters.socket({...parent,t,actionTime:parent.actionTime??parent.localTime},socket),angle=(parent.rotation||0)*Math.PI/180,scale=parent.scale??1;o.x+=parent.x+scale*(point[0]*Math.cos(angle)-point[1]*Math.sin(angle));o.y+=parent.y+scale*(point[0]*Math.sin(angle)+point[1]*Math.cos(angle));o.visible=o.visible&&parent.visible;o.drawAlpha*=parent.drawAlpha;}
 return objects;
}

function draw(c,t,b){const original=b.shot;validate(original);const local=t-b.t0;
 const s={...original,objects:resolveObjects(original,local,t)};
 H.bg(c,original.backdrop==='night');c.save();const camera=interpolate({x:480,y:270,zoom:1,...s.camera},s.camera?.keyframes,local);c.translate(480,270);c.scale(camera.zoom,camera.zoom);c.translate(-camera.x,-camera.y);
 backdrop(c,t,s);const byId=new Map(s.objects.map(o=>[o.id,o]));
for(const l of s.links||[]){const a=byId.get(l.from),z=byId.get(l.to);if(!a.visible||!z.visible)continue;c.save();c.globalAlpha=Math.min(a.drawAlpha,z.drawAlpha);if(l.dashed)c.setLineDash([5,4]);line(c,a.x,a.y+(l.fromDy??-60),z.x,z.y+(l.toDy??-60),l.color||P.blue,l.width||2);c.restore();}
for(const o of [...s.objects].sort((a,b)=>(a.z||0)-(b.z||0))){if(!o.visible)continue;c.save();c.globalAlpha=o.drawAlpha;c.translate(o.x,o.y);c.rotate((o.rotation||0)*Math.PI/180);c.scale(o.scale??1,o.scale??1);props.get(o.type)(c,t,o);c.restore();}c.restore();}

const old=g.TuragScenes.draw;g.TuragScenes.draw=(c,t,b)=>b.scene==='compose'?draw(c,t,b):old(c,t,b);g.TuragScenes.names.push('compose');
g.TuragComposer={register,validate,draw,interpolate,resolveObjects,propNames:()=>[...props.keys()],version:'1.0.0'};
})(window);

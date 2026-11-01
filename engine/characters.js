/* Turag cast primitives. Reference: reference/characters/chars_v1.jpg and chars2.jpg.
 * All dimensions relative to standing height; animation depends only on t. */
(function(global){
'use strict';
const C={ink:'#12141C',red:'#FF3D17',blue:'#2F3BFF',paper:'#E9E4D2',skin:'#7B7D93',trousers:'#272A3A'};
const ACTIONS=['rest','typing','sew','phone','explain','raise','write','carry','examine','take','point','wave','handover','push','pull','lift','place','drink','read','listen','operate'];
function oval(c,x,y,rx,ry,col){c.fillStyle=col;c.beginPath();c.ellipse(x,y,rx,ry,0,0,Math.PI*2);c.fill()}
function limb(c,points,w,col){c.strokeStyle=col;c.lineWidth=w;c.lineCap='round';c.lineJoin='round';c.beginPath();points.forEach((p,i)=>i?c.lineTo(...p):c.moveTo(...p));c.stroke()}
function head(c,x,y,h,variant,skin,visor){
  // Hair is drawn behind the face: no eyes, nose, mouth or cartoon expression.
  if(variant===1){oval(c,x-.025*h,y+.024*h,.065*h,.105*h,C.ink)}
  c.fillStyle=skin;c.fillRect(x-.018*h,y+.045*h,.037*h,.071*h);
  oval(c,x,y,.051*h,.069*h,skin);
  c.beginPath();c.moveTo(x+.043*h,y-.012*h);c.lineTo(x+.068*h,y+.014*h);c.lineTo(x+.044*h,y+.024*h);c.fill();
  c.fillStyle=variant===3?C.paper:C.ink;c.beginPath();
  c.moveTo(x-.06*h,y+.002*h);c.bezierCurveTo(x-.058*h,y-.101*h,x+.062*h,y-.102*h,x+.064*h,y+.01*h);
  c.quadraticCurveTo(x+.012*h,y-.047*h,x-.06*h,y+.002*h);c.fill();
  if(variant===2)oval(c,x-.068*h,y-.045*h,.027*h,.028*h,C.ink);
  if(visor){c.fillStyle=visor===true?C.blue:visor;c.save();c.translate(x+.015*h,y);c.rotate(.12);c.fillRect(-h*.025,-h*.004,h*.067,h*.018);c.restore()}
}
const mix=(a,b,u)=>a+(b-a)*u;
function trajectory(keys,t){if(t<=keys[0][0])return keys[0].slice(1);for(let i=1;i<keys.length;i++)if(t<keys[i][0]){let u=(t-keys[i-1][0])/(keys[i][0]-keys[i-1][0]);u=u*u*(3-2*u);return [mix(keys[i-1][1],keys[i][1],u),mix(keys[i-1][2],keys[i][2],u)];}return keys[keys.length-1].slice(1);}
function actionPose(o={}){
 if(o.actions?.length){const time=o.actionTime??o.t??0,track=[...o.actions].sort((a,b)=>a.at-b.at);let index=-1;for(let i=0;i<track.length;i++)if(track[i].at<=time)index=i;
  const base={...o,actions:undefined},entry=track[index];if(!entry)return actionPose(base);
  const current=actionPose({...base,...entry,actions:undefined,actionTime:time-entry.at});const blend=entry.blend??.2;
  if(index>=0&&blend>0&&time-entry.at<blend){const previous=actionPose({...base,actions:track.slice(0,index),actionTime:entry.at});let u=Math.max(0,(time-entry.at)/blend);u=u*u*(3-2*u);for(const key of ['right','left'])current[key]=current[key].map((v,j)=>mix(previous[key][j],v,u));for(const key of ['lean','look','headY'])current[key]=mix(previous[key],current[key],u);}
  return current;
 }
 const t=o.actionTime??o.t??0,p=o.phase||0,mode=o.action||(o.pose==='sit'?'typing':o.pose==='phone'?'phone':o.pose==='point'?'explain':o.pose==='raise'?'raise':'rest');
 let right=[.09,-.49],left=[-.09,-.49],look=0,lean=0,headY=0,rightShape='relaxed',leftShape='relaxed';if(mode==='rest'&&o.pose==='sit'){right=[.18,-.33];left=[.08,-.34];}
 if(mode==='typing'){const q=t*8+p;right=[.31+.025*Math.sin(q*.53),-.54-.018*Math.max(0,Math.sin(q))];left=[.25+.022*Math.sin(q*.61+1),-.54-.018*Math.max(0,Math.sin(q+2.2))];look=2*Math.sin(t*1.6+p);}
 if(mode==='sew'){const q=t*4+p;right=[.37+.045*Math.sin(q),-.415-.012*Math.sin(q*2)];left=[.25+.045*Math.sin(q+.5),-.415];look=5+3*Math.sin(t*1.4+p);lean=.035;rightShape=leftShape='flat';}
 if(mode==='phone'){right=trajectory([[0,.11,-.50],[.25,.07,-.55],[.7,.22,-.78],[1.05,.19,-.84],[1.8,.20,-.81],[2.5,.27,-.73],[4,.21,-.80]],t);left=trajectory([[0,-.09,-.49],[1,-.12,-.59],[2.1,-.19,-.70],[3.1,-.09,-.49]],t);look=8*Math.min(1,t/.7);lean=-.025;rightShape='grip';leftShape='open';}
 if(mode==='explain'){right=trajectory([[0,.10,-.50],[.25,.07,-.54],[.45,.23,-.64],[1.15,.36,-.77],[1.45,.39,-.75],[1.9,.31,-.72],[2.7,.22,-.65],[3.4,.12,-.50]],t);left=trajectory([[0,-.09,-.49],[1,-.13,-.55],[2,-.08,-.49]],t);look=-3*Math.sin(t*1.8+p);lean=-.018;rightShape='open';leftShape='relaxed';}
 if(mode==='raise'){right=trajectory([[0,.09,-.49],[.6,.15,-.88],[1.1,.19,-1.07],[2.5,.19,-1.07]],t);look=-7;}
 if(mode==='write'){right=[.33+.05*Math.sin(t*3.5+p),-.91+.055*Math.cos(t*5+p)];left=[-.07,-.55];look=-6;lean=.035;rightShape='grip';}
 if(mode==='carry'){right=[.335,-.44+Math.sin(t*4.8+p)*.008];left=[.14,-.44+Math.sin(t*4.8+p)*.008];lean=.025;rightShape=leftShape='grip';}
 if(mode==='examine'){right=trajectory([[0,.16,-.55],[.25,.11,-.58],[.6,.28,-.72],[1.1,.30,-.79],[1.5,.27,-.76],[2.7,.20,-.67]],t);left=[-.13,-.58];look=5;lean=.025;rightShape='grip';leftShape='open';}
 if(mode==='take'){right=trajectory([[0,.32,-.49],[.25,.28,-.45],[.4,.39,-.58],[.9,.20,-.68],[1.25,.17,-.71],[1.7,.30,-.53],[2.5,.32,-.49]],t);left=[.24,-.49];lean=.03;rightShape='grip';}
 if(mode==='point'){right=trajectory([[0,.10,-.50],[.4,.24,-.66],[.85,.39,-.78],[1.7,.38,-.78],[2.4,.18,-.57]],t);look=-4;lean=-.02;rightShape='point';}
 if(mode==='wave'){right=trajectory([[0,.10,-.50],[.5,.18,-.88],[.9,.27,-.91],[1.25,.18,-.86],[1.6,.28,-.92],[2.2,.18,-.86]],t);look=-5;rightShape='open';}
 if(mode==='handover'){right=trajectory([[0,.11,-.50],[.35,.08,-.56],[.9,.35,-.63],[1.6,.39,-.63],[2.2,.22,-.55]],t);lean=-.025;rightShape='flat';}
 if(mode==='push'){right=trajectory([[0,.16,-.52],[.4,.10,-.58],[1.0,.38,-.62],[1.8,.43,-.62],[2.4,.30,-.57]],t);left=trajectory([[0,-.09,-.49],[.4,-.02,-.58],[1,.27,-.62],[1.8,.31,-.62]],t);lean=-.06;rightShape=leftShape='flat';}
 if(mode==='pull'){right=trajectory([[0,.39,-.61],[.7,.34,-.62],[1.5,.13,-.56],[2.2,.10,-.50]],t);left=trajectory([[0,.28,-.61],[.7,.24,-.62],[1.5,-.03,-.56],[2.2,-.08,-.50]],t);lean=.06;rightShape=leftShape='grip';}
 if(mode==='lift'){right=trajectory([[0,.28,-.37],[.45,.31,-.30],[1.1,.26,-.63],[1.8,.21,-.78],[2.5,.21,-.78]],t);left=trajectory([[0,.10,-.37],[.45,.12,-.30],[1.1,.08,-.63],[1.8,.04,-.78],[2.5,.04,-.78]],t);lean=.04;rightShape=leftShape='grip';}
 if(mode==='place'){right=trajectory([[0,.30,-.72],[.7,.34,-.62],[1.3,.31,-.48],[1.8,.25,-.43],[2.4,.12,-.50]],t);left=[-.09,-.49];lean=-.02;rightShape='flat';}
 if(mode==='drink'){right=trajectory([[0,.14,-.49],[.5,.20,-.71],[1.0,.15,-.88],[1.8,.15,-.88],[2.4,.16,-.60],[2.9,.12,-.49]],t);look=7;rightShape='grip';}
 if(mode==='read'){const settle=Math.exp(-t*2)*.06;right=[.24,-.66+settle];left=[.04,-.66+settle];look=7+Math.sin(t*.8+p)*2;lean=.025;rightShape=leftShape='grip';}
 if(mode==='listen'){right=[.10,-.49];left=trajectory([[0,-.09,-.49],[.55,-.16,-.77],[1.1,-.13,-.84],[2.5,-.13,-.84]],t);look=-6;leftShape='open';}
 if(mode==='operate'){const q=t*3+p;right=[.32+.035*Math.sin(q),-.54+.012*Math.cos(q*1.7)];left=[.20+.03*Math.sin(q+.9),-.54+.012*Math.cos(q*1.4)];look=3;lean=.02;rightShape=leftShape='flat';}
 if(o.rightHandFrames)right=trajectory(o.rightHandFrames,t);if(o.leftHandFrames)left=trajectory(o.leftHandFrames,t);
 headY=Math.sin(t*1.15+p)*.003;
 return {mode,right,left,look:o.look??look,lean:o.bodyLean??lean,headY,rightShape,leftShape};
}
function solveArm(shoulder,hand,length=.205){const dx=hand[0]-shoulder[0],dy=hand[1]-shoulder[1],distance=Math.hypot(dx,dy),d=Math.min(distance,length*1.995),ux=dx/(distance||1),uy=dy/(distance||1),target=[shoulder[0]+ux*d,shoulder[1]+uy*d],height=Math.sqrt(Math.max(0,length*length-d*d/4));return {target,elbow:[shoulder[0]+ux*d/2-uy*height,shoulder[1]+uy*d/2+ux*height]};}
function bodyPoint(o,point,pose){const t=o.t||0,p=o.phase||0,seated=o.pose==='sit',breathe=o.breathe===false?0:Math.sin(t*1.35+p)*.0035,bob=!seated&&(o.pose==='walk'||o.action==='carry')?Math.abs(Math.sin(t*4.8+p))*.008:0,a=pose.lean||0,co=Math.cos(a),si=Math.sin(a);let x=point[0],y=point[1];if(seated){y+=.31+breathe;const nx=co*x-si*y,ny=si*x+co*y;x=nx;y=ny-.31;}else{y+=breathe;const nx=co*x-si*y,ny=si*x+co*y;x=nx;y=ny-bob;}return [x*(o.dir===-1?-1:1)*(o.h||160),y*(o.h||160)];}
function socket(o={},name='rightHand'){const pose=actionPose(o),seated=o.pose==='sit';if(name==='rightHand'||name==='leftHand'){const side=name==='leftHand'?'left':'right',shoulder=[side==='left'?(seated?-.015:-.076):.072,seated?-.68:-.76],point=solveArm(shoulder,pose[side],pose.mode==='carry'?.225:.205).target;return bodyPoint(o,point,pose);}const points={head:[seated?.026:.006,(seated?-.83:-.905)+pose.headY],torso:[0,seated?-.58:-.62],pelvis:[0,seated?-.31:-.44]};if(!points[name])throw Error('Unknown character socket '+name);if(name==='pelvis'&&seated)return [0,-.31*(o.h||160)];return bodyPoint(o,points[name],pose);}
function handSocket(o={},side='right'){return socket(o,side==='left'?'leftHand':'rightHand');}
function drawHand(c,p,shape,skin,angle=0){c.save();c.translate(p[0],p[1]);c.rotate(angle);if(shape==='point'){limb(c,[[0,0],[.043,-.006]],.011,skin);oval(c,0,0,.018,.016,skin);}else if(shape==='open'||shape==='flat'){oval(c,0,0,.022,.014,skin);for(let i=-1;i<=1;i++)limb(c,[[.006,i*.009],[.035,i*.012]],.006,skin);}else if(shape==='grip'){oval(c,0,0,.021,.019,skin);limb(c,[[.005,-.008],[.028,.008]],.007,skin);}else oval(c,0,0,.019,.019,skin);c.restore();}
function arm(c,shoulder,hand,cloth,skin,length=.205,shape='relaxed'){const {target,elbow}=solveArm(shoulder,hand,length);limb(c,[shoulder,elbow,target],.037,cloth);drawHand(c,target,shape,skin,Math.atan2(target[1]-elbow[1],target[0]-elbow[0]));return target;}

function actingArms(c,o,pose,seated,cloth,skin){
 const shoulderY=seated?-.68:-.76;
 if(pose.mode==='carry'&&o.autoProps!==false){c.fillStyle=C.paper;c.strokeStyle=C.ink;c.lineWidth=.007;c.fillRect(.12,-.53,.29,.18);c.strokeRect(.12,-.53,.29,.18);limb(c,[[.12,-.53],[.265,-.445],[.41,-.53]],.006,C.ink);}
 arm(c,[seated?-.015:-.076,shoulderY],pose.left,cloth,skin,pose.mode==='carry'?.225:.205,pose.leftShape);
 const hand=arm(c,[.072,shoulderY],pose.right,cloth,skin,pose.mode==='carry'?.225:.205,pose.rightShape);
 if(pose.mode==='phone'&&o.autoProps!==false){c.save();c.translate(hand[0]+.007,hand[1]-.025);c.rotate(-.3);c.fillStyle=C.ink;c.fillRect(-.022,-.045,.044,.077);c.fillStyle=C.blue;c.fillRect(-.015,-.038,.030,.060);c.restore();}
 if(pose.mode==='examine'){c.save();c.translate(hand[0],hand[1]);c.rotate(-.15);c.fillStyle=C.ink;c.fillRect(-.04,-.10,.08,.11);c.fillStyle=C.paper;c.fillRect(-.03,-.09,.06,.09);for(let j=0;j<3;j++)limb(c,[[-.02,-.07+j*.02],[.02,-.07+j*.02]],.004,C.ink);c.restore();}
 if(pose.mode==='write'){limb(c,[[hand[0]-.006,hand[1]-.008],[hand[0]+.025,hand[1]-.035]],.008,C.paper);}
}
function actorHead(c,x,y,v,skin,visor,look,headY=0){c.save();c.translate(x,y+headY);c.rotate(look*Math.PI/180);head(c,0,0,1,v%4,skin,visor);c.restore();}
function draw(c,o={}){
  const x=o.x||0,y=o.y||0,h=o.h||160,t=o.t||0,dir=o.dir===-1?-1:1,role=o.role||'extra',v=role==='guide'?0:(o.variant==null?0:o.variant%6);
  const guide=role==='guide',doctor=role==='doctor',vendor=role==='vendor';
  const cloth=o.color||(guide?C.red:doctor||vendor||v===3?'#D4CBB5':['#8A8CA0','#6B6E85','#4A4D63','#E0D5B5','#8A8CA0','#6B6E85'][v]);
  const skin=guide?'#3A3C4E':C.skin,legs=o.legColor||C.trousers,pose=o.pose||'stand';
  const acting=actionPose(o);
  const breathe=o.breathe===false?0:Math.sin(t*1.35+(o.phase||0))*.0035;
  const dress=!guide&&!doctor&&!vendor&&(v===1||v===2||v===4),panjabi=v===3&&!guide&&!doctor;
  c.save();c.globalAlpha*=o.alpha==null?1:o.alpha;c.translate(x,y);c.scale(dir*h,h);
  oval(c,0,.005,.15,.018,'rgba(18,20,28,.14)');
  if(pose==='sit'){
    const chair=o.chairColor||'#6B6E85';limb(c,[[-.13,-.62],[-.13,-.28],[.08,-.28]],.014,chair);
    limb(c,[[-.12,-.28],[-.12,0]],.014,chair);limb(c,[[.07,-.28],[.07,0]],.014,chair);
    limb(c,[[.015,-.31],[.24,-.31],[.24,-.025]],.071,legs);limb(c,[[.24,-.025],[.31,-.025]],.047,C.ink);
    c.save();c.translate(0,-.31);c.rotate(acting.lean);c.translate(0,.31+breathe);
    c.fillStyle=cloth;c.beginPath();c.roundRect(-.087,-.74,.176,.40,.048);c.fill();
    actingArms(c,o,acting,true,cloth,skin);
    actorHead(c,.026,-.83,v,skin,o.visor===undefined?guide:o.visor,acting.look,acting.headY);
    c.restore();
  }else{
    const stride=(pose==='walk'||o.action==='carry')?Math.sin(t*4.8+(o.phase||0))*.19:0,bob=(pose==='walk'||o.action==='carry')?Math.abs(Math.sin(t*4.8+(o.phase||0)))*.008:0;
    c.translate(0,-bob);
    c.rotate(acting.lean);c.translate(0,breathe);
    if(dress||panjabi){
      c.fillStyle=cloth;c.beginPath();c.moveTo(-.085,-.79);c.lineTo(.085,-.79);c.lineTo(.12+stride*.13,-.065);c.lineTo(-.12+stride*.13,-.065);c.closePath();c.fill();
      if(dress){c.fillStyle=C.red;c.fillRect(-.117+stride*.13,-.107,.234,.018)}
      for(const s of[-1,1]){const q=t*4.8+(o.phase||0)+(s===-1?0:Math.PI),wave=(pose==='walk'||o.action==='carry')?Math.sin(q):0,lift=(pose==='walk'||o.action==='carry')?Math.max(0,Math.sin(q))*.045:0,foot=s*.06+wave*.09,fy=-.025-lift;limb(c,[[s*.045,-.07],[foot,fy]],.041,legs);limb(c,[[foot,fy],[foot+s*.035,fy]],.025,C.ink)}
    }else{
      // Rounded thigh tops sit visibly over the lower shirt, matching the source silhouette.
      for(const s of[-1,1]){const q=t*4.8+(o.phase||0)+(s===-1?0:Math.PI),wave=(pose==='walk'||o.action==='carry')?Math.sin(q):0,foot=s*.032+wave*.19,lift=(pose==='walk'||o.action==='carry')?Math.max(0,Math.sin(q))*.045:0,fy=-.025-lift;limb(c,[[s*.026,-.46],[foot*.55,-.245],[foot,fy]],.065,legs);limb(c,[[foot,fy],[foot+.045,fy]],.036,C.ink)}
    }
    c.fillStyle=cloth;c.beginPath();c.roundRect(-.091,-.805,.182,doctor?.43:.365,.044);c.fill();
    if(doctor){c.strokeStyle='#A5A7B8';c.lineWidth=.009;c.beginPath();c.moveTo(0,-.78);c.lineTo(0,-.42);c.moveTo(-.07,-.65);c.lineTo(-.015,-.65);c.stroke()}
    if(acting.mode!=='rest'){actingArms(c,o,acting,false,cloth,skin);}else{const swing=pose==='walk'?-stride*.55:0;limb(c,[[-.076,-.765],[-.11+swing*.5,-.62],[-.09+swing,-.49]],.037,cloth);drawHand(c,[-.09+swing,-.49],'relaxed',skin);limb(c,[[.076,-.765],[.11-swing*.5,-.62],[.09-swing,-.49]],.037,cloth);drawHand(c,[.09-swing,-.49],'relaxed',skin);}
    if(vendor){c.fillStyle=C.red;c.fillRect(-.045,-.80,.03,.22);c.fillRect(.02,-.80,.028,.15);c.fillStyle=C.paper;for(let i=0;i<4;i++)c.fillRect(-.05,-.78+i*.045,.105,.012)}
    actorHead(c,.006,-.905,v,skin,o.visor===undefined?guide:o.visor,acting.look,acting.headY);
  }
  c.restore();
}
function seated(c,o){draw(c,{...o,pose:'sit'})}
function icon(c,x,y,h,color=C.ink){oval(c,x,y-h*.81,h*.10,h*.10,color);c.fillStyle=color;c.beginPath();c.roundRect(x-h*.105,y-h*.65,h*.21,h*.59,h*.055);c.fill()}
global.TuragCharacters={draw,seated,icon,actionPose,handSocket,socket,actionNames:()=>[...ACTIONS],palette:C,version:'3.0.0'};
})(typeof window!=='undefined'?window:globalThis);

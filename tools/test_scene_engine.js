'use strict';
const assert=require('node:assert/strict'),fs=require('fs'),vm=require('vm'),path=require('path');
const env={console};env.window=env;env.globalThis=env;vm.createContext(env);
for(const file of ['characters.js','runtime.js','composer.js','custom-props.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,'../engine',file),'utf8'),env);
const C=env.TuragComposer,H=env.TuragCharacters;
const f=[{at:0,x:0,opacity:0},{at:1,x:100},{at:2,opacity:1},{at:3,y:60}];
assert.equal(C.interpolate({x:0,y:0,opacity:0},f,2.5).x,100,'x must persist through unrelated opacity/y keys');
assert.equal(C.interpolate({x:0,y:0,opacity:0},f,2.5).opacity,1);
assert.equal(C.interpolate({scale:1},[{at:1,scale:0}],1).scale,0);
const shot={objects:[{id:'person',type:'person',x:100,y:400,h:200,action:'take',instant:true,rotation:20,scale:.8,enter:1},{id:'letter',type:'offer_letter',attachTo:'person',hand:'right',x:0,y:0,instant:true}]};
assert.equal(C.resolveObjects(shot,.5,.5)[1].visible,false,'A held prop cannot precede its actor');
for(const time of [1,1.5,2,3]){const [person,letter]=C.resolveObjects(shot,time,time),h=H.handSocket({...person,t:time,actionTime:person.localTime},'right'),a=20*Math.PI/180;assert.ok(Math.abs(letter.x-(100+.8*(h[0]*Math.cos(a)-h[1]*Math.sin(a))))<1e-8);assert.ok(Math.abs(letter.y-(400+.8*(h[0]*Math.sin(a)+h[1]*Math.cos(a))))<1e-8);}
const boundary={objects:[{id:'card',type:'chapter_card',x:0,y:0,exit:2.4,instant:true}]};assert.equal(C.resolveObjects(boundary,43.4-41,43.4)[0].visible,false);
const stopped={objects:[{id:'p',type:'person',x:40,y:455,motion:{kind:'walk',speed:0}}]};assert.equal(C.resolveObjects(stopped,5,5)[0].x,40);
for(const a of H.actionNames()){for(const t of [.1,.45,.9,1.4,2.1])for(const s of ['leftHand','rightHand','head','torso','pelvis'])assert.ok(H.socket({action:a,actionTime:t,h:200,pose:['typing','sew'].includes(a)?'sit':'stand'},s).every(Number.isFinite),`${a}/${s} socket must stay finite`);}
for(const a of ['typing','phone','sew','write','examine','take','point','wave','handover','push','pull','lift','place','drink','read','operate']){const p=[.1,.45,.9,1.4,2.1].map(t=>H.handSocket({action:a,actionTime:t,h:200,pose:['typing','sew'].includes(a)?'sit':'stand'}));assert.ok(p.some(v=>Math.hypot(v[0]-p[0][0],v[1]-p[0][1])>1),a+' needs actual reachable wrist movement');}
for(const kind of ['walk','float','bob','shake','pendulum','pulse','orbit']){const o=C.resolveObjects({objects:[{id:'m',type:'label',x:10,y:20,rotation:0,scale:1,opacity:1,motion:{kind,speed:1,amount:12}}]},1.25,1.25)[0];for(const k of ['x','y','rotation','scale','opacity'])assert.ok(Number.isFinite(o[k]),`${kind}/${k} must stay finite`);}
assert.throws(()=>C.validate({objects:[{id:'p',type:'person',x:0,y:0,action:'teleport'}]}),/Unknown character action/);
assert.throws(()=>C.validate({objects:[{id:'p',type:'person',x:0,y:0},{id:'x',type:'label',x:0,y:0,attachTo:'p',socket:'elbow'}]}),/socket/);
console.log('PASS: timing, attachments, all sockets/actions, all motion kinds, validation and articulated movement.');
// Seated hips remain on the chair while the torso breathes and leans.
const sequence={action:'rest',actions:[{at:1,action:'read',blend:.3},{at:3,action:'point',blend:.3}],h:200};
const before=H.actionPose({...sequence,actionTime:.999999}),after=H.actionPose({...sequence,actionTime:1});
const overlapping={action:'rest',actions:[{at:0,action:'raise',blend:2},{at:.5,action:'point',blend:1},{at:.7,action:'read',blend:.5}]};
for(const boundary of [.5,.7]){const a=H.actionPose({...overlapping,actionTime:boundary-1e-7}),b=H.actionPose({...overlapping,actionTime:boundary});for(const side of ['left','right'])assert.ok(Math.hypot(a[side][0]-b[side][0],a[side][1]-b[side][1])<1e-5,'Overlapping transitions must start at the visible pose');}
assert.ok(Math.hypot(before.right[0]-after.right[0],before.right[1]-after.right[1])<.00001,'Action boundary must remain continuous');
assert.deepEqual(H.actionPose({...sequence,actionTime:4}),H.actionPose({...sequence,actionTime:4}),'Action seeking must be deterministic');
assert.throws(()=>C.validate({objects:[{id:'bad',type:'person',x:0,y:0,actions:[{at:1,action:'read'},{at:1,action:'point'}]}]}),/action track/);
for(const t of [0,.4,1.7,3]){const hip=H.socket({pose:'sit',action:'sew',h:200,t,bodyLean:.2},'pelvis');assert.equal(hip[0],0);assert.equal(hip[1],-62);}
// Supplying a crop/file/cloth prop must not leave a default envelope under it.
function drawCalls(options){const calls=[];const ctx=new Proxy({}, {get:(_,key)=>(...args)=>{calls.push([key,...args]);},set:()=>true});H.draw(ctx,{x:0,y:0,h:160,t:1,...options});return calls;}
const envelope=call=>call[0]==='fillRect'&&call[3]===.29&&call[4]===.18;
assert.ok(drawCalls({action:'carry'}).some(envelope),'Legacy carry keeps its default envelope');
assert.ok(!drawCalls({action:'carry',autoProps:false}).some(envelope),'External carried props suppress the default envelope');
const phone=call=>call[0]==='fillRect'&&call[3]===.044&&call[4]===.077;
assert.ok(drawCalls({action:'phone'}).some(phone));
assert.ok(!drawCalls({action:'phone',autoProps:false}).some(phone),'Attached phone must not duplicate the built-in phone');
assert.deepEqual(H.socket({action:'carry',t:1,autoProps:false}),H.socket({action:'carry',t:1}),'Suppressing artwork cannot change contact geometry');

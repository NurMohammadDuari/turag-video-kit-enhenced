'use strict';
const assert=require('node:assert/strict'),path=require('path'),{pathToFileURL}=require('url'),puppeteer=require('puppeteer-core'),{chromePath}=require('./render_mp4');
(async()=>{const browser=await puppeteer.launch({executablePath:chromePath(),headless:true,args:['--no-sandbox']});try{const page=await browser.newPage();await page.goto(pathToFileURL(path.resolve('engine/Turag_Research_Revision.html')).href);await page.waitForFunction('window.__ready');const result=await page.evaluate(()=>{
 const canvas=document.createElement('canvas');canvas.width=960;canvas.height=540;const c=canvas.getContext('2d');
 const shot={scene:'compose',t0:0,t1:4,shot:{backdrop:'paper',objects:[{id:'new-machine',type:'vector',x:480,y:400,instant:true,shapes:[
  {kind:'path',d:'M-90 0 L-90 -130 Q0 -185 90 -130 L90 0 Z',fill:'#4A4D63'},
  {kind:'rect',x:-65,y:-120,w:130,h:70,fill:'#2F3BFF'},
  {kind:'path',d:'M0 -100 C25 -145 65 -145 90 -100',fill:'none',stroke:'#E9E4D2',width:5,translateX:-45,translateY:80,keyframes:[{at:0,rotation:-20},{at:2,rotation:20}]}
 ]}]}};
 const render=t=>{TuragScenes.draw(c,t,shot);return canvas.toDataURL()};const a=render(0),b=render(1),d=render(2),again=render(0);return{changed:a!==b&&b!==d,deterministic:a===again,image:d};});assert.ok(result.changed,'Shape keyframes must change the rendered artwork');assert.ok(result.deterministic,'Vector seeking must be deterministic');console.log('PASS: SVG curves, strokes, part animation and deterministic seeking in Chrome');}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1});

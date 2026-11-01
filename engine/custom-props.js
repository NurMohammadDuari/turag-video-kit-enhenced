/* AI-authored prop extensions belong here. This file is bundled after composer.js.
Example:
TuragComposer.register('custom_machine', (ctx, absoluteTime, object) => {
  const H = TuragScenes.helpers, P = TuragScenes.palette;
  H.rect(ctx, -60, -110, 120, 110, P.blue);
  H.oval(ctx, -35, 0, 14, 14, P.ink);
  H.oval(ctx, 35, 0, 14, 14, P.ink);
});
The object origin is its ground anchor (0,0). Keep drawing deterministic.
Do not edit the character rig independently for a single shot.
*/
/* Full-episode reusable components. Coordinates are local anchors; all moving
 * parts are sampled from local time, so rendering and seeking agree. */
(function(){
const H=TuragScenes.helpers,P=TuragScenes.palette,R=TuragComposer.register;
const age=o=>Math.max(0,o.localTime??0),sat=x=>Math.max(0,Math.min(1,x)),ease=x=>1-Math.pow(1-sat(x),3);
function arrow(c,x,y,w=70,col=P.blue){H.line(c,x-w/2,y,x+w/2,y,col,3);H.poly(c,[[x+w/2,y],[x+w/2-14,y-8],[x+w/2-14,y+8]],col)}
function sheet(c,x,y,w=50,h=62,col=P.paper){H.rect(c,x,y,w,h,col,P.ink);for(let i=0;i<4;i++)H.line(c,x+8,y+12+i*10,x+w-8,y+12+i*10,col===P.blue?P.paper:P.slate,1)}
R('custom_machine',(c,t,o)=>{H.rect(c,-70,-165,140,165,P.slate,P.ink);H.rect(c,-55,-145,110,52,P.ink);for(let j=0;j<4;j++){H.rect(c,-50+j*27,-82,19,62,P.paper,P.ink);const active=(Math.floor(age(o)*3)+j)%4;H.rect(c,-45+j*27,-72+active*13,9,9,active%2?P.blue:P.red)}H.rect(c,-42,-137,84,35,P.blue);H.mono(c,'AI',0,-112,20,P.paper,'center')});
R('asset_bubble',(c,t,o)=>{const p=ease(age(o)/(o.seconds||1.5)),r=(o.startRadius||48)+((o.radius||165)-(o.startRadius||48))*p;H.oval(c,0,-55,o.startRadius||48,o.startRadius||48,P.blue);c.save();c.setLineDash([7,6]);c.beginPath();c.arc(0,-55,r,0,Math.PI*2);c.strokeStyle=P.red;c.lineWidth=5;c.stroke();c.restore();H.text(c,'আসল মূল্য',0,-47,17,P.paper,'center',80);H.text(c,'দাম',0,-55-r-14,24,P.red,'center')});
R('direction_arrow',(c,t,o)=>arrow(c,0,0,o.w||100));
R('cross_mark',(c,t,o)=>{const p=ease(age(o)/.4);H.line(c,-35,-30,35*p,30*p,P.red,5);H.line(c,-35,30,35*p,-30*p,P.red,5)});
R('survey_scale',(c,t,o)=>{H.line(c,-220,0,220,0,P.ink,3);for(let i=0;i<=10;i++)H.line(c,-220+i*44,-6,-220+i*44,6,P.ink,1);H.text(c,'০%',-220,35,21,P.ink,'center');H.text(c,'১০০%',220,35,21,P.ink,'center');const x=-220+440*ease(age(o)/2)*(o.progress??.5);H.oval(c,x,0,19,19,P.red);H.text(c,'?',x,8,27,P.paper,'center')});
R('percent_column',(c,t,o)=>{const v=sat(o.value/100),h=250;H.rect(c,-40,-h,80,h,P.paper,P.ink);H.rect(c,-38,-h*v*ease(age(o)/1.2),76,h*v*ease(age(o)/1.2),o.color||P.blue);H.text(c,o.label||'',0,25,21,P.ink,'center',190)});
R('chat_screen',(c,t,o)=>{H.rect(c,-115,-290,230,290,P.ink);H.rect(c,-106,-280,212,264,P.paper);H.rect(c,-106,-280,212,38,P.blue);H.text(c,'AI CHAT',0,-254,18,P.paper,'center');if(age(o)>.35){H.panel(c,-90,-225,155,50);H.text(c,'একটা প্রশ্ন',-12,-194,22,P.ink,'center',145)}if(age(o)>1){H.rect(c,-63,-155,155,57,P.pale);H.text(c,o.mistake?'ভুল উত্তর?':'উত্তর',14,-121,23,o.mistake?P.red:P.ink,'center',145)}H.oval(c,0,-7,3,3,P.paper)});
R('road_sign',(c,t,o)=>{H.line(c,0,-210,0,0,P.slate,5);H.rect(c,-90,-210,180,46,P.green);H.text(c,o.text||'',0,-178,22,P.paper,'center',168)});
R('workflow_strip',(c,t,o)=>{const labels=['ডাটা','চালানো','যাচাই'];for(let j=0;j<3;j++){const x=-175+j*175,active=age(o)>j*.7;H.panel(c,x-60,-115,120,115,active?P.blue:P.paper);H.text(c,labels[j],x,-22,22,active?P.paper:P.ink,'center',110);if(j===0)for(let k=0;k<3;k++)H.rect(c,x-35,-95+k*17,70,10,P.slate);if(j===1)H.monitor(c,x-38,-95,76,true);if(j===2)H.check(c,x-20,-85,35,P.paper);if(j<2)arrow(c,x+87,-57,40)}});
R('stage_curtain',(c,t,o)=>{const w=460*(1-sat(o.open)),h=330;for(const dir of[-1,1]){c.save();c.translate(dir*230,0);const x=dir<0?0:-w/2;H.rect(c,x,-h,w/2,h,P.slate);for(let j=0;j<w/2;j+=14)H.line(c,x+j,-h,x+j,0,P.grey,2);H.dots(c,x,-90,w/2,90,P.ink,7,1);c.restore()}});
R('scaffold',(c,t,o)=>{H.rect(c,-160,-280,320,280,P.blue);H.orb(c,0,-150,42,t);for(let j=0;j<5;j++)H.line(c,-190+j*95,-330,-190+j*95,0,P.slate,4);for(let j=0;j<5;j++)H.line(c,-190,-j*75,190,-j*75,P.slate,4);H.dots(c,-160,-100,320,100,P.ink,8,1.3)});
R('task_bundle',(c,t,o)=>{const q=sat(o.split),names=['ইমেইল','রিপোর্ট','মিটিং','সিদ্ধান্ত','হিসাব','পরিকল্পনা'];for(let j=0;j<6;j++){const tx=(j%3-1)*108,ty=(Math.floor(j/3)-.5)*82,x=tx*q,y=-75+ty*q;H.panel(c,x-48,y-32,96,64,j<2?P.blue:P.paper);H.text(c,names[j],x,y+8,19,j<2?P.paper:P.ink,'center',88)}if(q<.4){H.panel(c,-100,-125,200,110);H.text(c,'চাকরি',0,-55,45,P.ink,'center')}});
R('timebar',(c,t,o)=>{H.rect(c,-15,-86,30,86,P.paper,P.ink);const h=86*sat(o.value)*ease(age(o)/1.3);H.rect(c,-13,-h,26,h,P.blue);for(let i=0;i<3;i++)H.line(c,-8,-74+i*9,8,-74+i*9,P.slate,1)});
R('patient',(c,t,o)=>{H.oval(c,-52,-27,11,10,P.ink);H.poly(c,[[-38,-34],[58,-34],[68,-15],[-38,-15]],P.pale);H.line(c,-32,-31,34,-31,P.slate,3)});
R('task_matrix',(c,t,o)=>{const n=o.total||100,cols=o.cols||20,rows=Math.ceil(n/cols),w=520,h=230,dx=w/cols,dy=h/rows;const active=Math.round((o.active??n)*ease(age(o)/1.8));for(let j=0;j<n;j++)H.rect(c,-w/2+(j%cols)*dx,-h+Math.floor(j/cols)*dy,Math.max(2,dx-2),Math.max(2,dy-2),j<active?P.blue:P.pale)});
R('rice_patch',(c,t,o)=>{const w=o.w||800;H.rect(c,-w/2,-65,w,65,P.green);H.dots(c,-w/2,-65,w,65,P.paper,8,1);for(let j=0;j<Math.floor(w/11);j++){const x=-w/2+j*11,y=-4-(j%4)*11,h=x<(-w/2+w*(o.cut||0))?7:29;H.line(c,x,y,x+Math.sin(t*.7+j)*2,y-h,P.paper,1);if(h>10)H.line(c,x,y-14,x+6,y-24,P.pale,1)}});
R('rice_bundles',(c,t,o)=>{for(let j=0;j<3;j++){const x=j*30-30;H.poly(c,[[x-12,0],[x-9,-45],[x,-58],[x+9,-45],[x+12,0]],P.pale,P.ink);H.line(c,x-10,-24,x+10,-24,P.red,2)}});
R('combine_live',(c,t,o)=>{H.rect(c,-100,-100,140,75,P.paper,P.ink);H.rect(c,10,-152,57,80,P.green);H.rect(c,19,-143,38,34,P.pale);H.rect(c,-120,-49,230,15,P.slate);const a=age(o)*3;for(let j=0;j<10;j++){const x=-110+j*22;H.line(c,x,-43,x+Math.sin(a)*10,-24+Math.cos(a)*9,P.ink,3)}for(const x of[-60,64]){H.oval(c,x,-15,26,26,P.ink);H.line(c,x,-15,x+Math.cos(a)*20,-15+Math.sin(a)*20,P.pale,2)}});
R('editing_timeline',(c,t,o)=>{H.rect(c,-160,-145,320,145,P.ink,P.grey);for(let j=0;j<5;j++){H.rect(c,-146,-129+j*24,290,17,P.slate);H.rect(c,-140+j*10,-126+j*24,130+(j%3)*35,11,j%2?P.blue:P.pale)}const x=-140+280*sat(o.progress||0)*ease(age(o)/1.6);H.line(c,x,-139,x,-7,P.red,2)});
R('code_panel',(c,t,o)=>{H.panel(c,-160,-205,320,205);H.rect(c,-160,-205,320,30,P.blue);H.mono(c,'CLAUDE  /  ANIMATION',-145,-184,12,P.paper);const lines=['scene = compose(script)','actor.action = typing','draw(props, localTime)','render(frame)','check(output)'];for(let j=0;j<lines.length;j++)if(age(o)>j*.28)H.mono(c,lines[j],-142,-145+j*28,15,j%2?P.blue:P.ink)});
R('spotlight',(c,t,o)=>{H.poly(c,[[-40,-360],[40,-360],[190,0],[-190,0]],'rgba(233,228,210,.09)');H.poly(c,[[-32,-360],[32,-360],[20,-390],[-20,-390]],P.slate)});
R('ledger',(c,t,o)=>{H.panel(c,-230,-250,460,250);H.rect(c,-230,-250,460,43,P.red);H.line(c,0,-250,0,0,P.ink,2);H.text(c,o.left,-115,-220,26,P.paper,'center');H.text(c,o.right,115,-220,26,P.paper,'center');for(let j=0;j<6;j++)H.line(c,-225,-185+j*30,225,-185+j*30,P.pale,1);H.text(c,o.a||'',-115,-90,42,P.ink,'center');H.text(c,o.b||'',115,-90,42,P.ink,'center')});
R('newspaper',(c,t,o)=>{H.panel(c,-265,-190,530,190);H.text(c,'হেডলাইন',-242,-155,25,P.ink);H.line(c,-242,-143,242,-143,P.ink,2);H.text(c,o.text||'',0,-93,39,P.blue,'center',485);for(let j=0;j<5;j++)H.line(c,-242,-65+j*9,242,-65+j*9,P.grey,1)});
R('four_cells',(c,t,o)=>{for(let j=0;j<4;j++)H.rect(c,-125+j*65,-35,55,55,j<o.active&&age(o)>j*.25?P.blue:P.paper,P.ink);H.text(c,'৩ / ৪',0,64,35,P.blue,'center')});
R('cloth_gripper',(c,t,o)=>{const a=age(o),sway=Math.sin(a*2)*8;H.rect(c,-35,-12,70,12,P.slate);H.line(c,0,-12,-55,-120,P.blue,14);H.line(c,-55,-120,-90,-205+sway,P.blue,13);H.line(c,-90,-205+sway,-135,-215+sway,P.blue,9);H.line(c,-135,-215+sway,-148,-200+sway,P.ink,4);H.line(c,-135,-215+sway,-125,-198+sway,P.ink,4);c.beginPath();c.moveTo(-149,-197+sway);c.quadraticCurveTo(-200,-100+Math.sin(a)*15,-115,-50);c.lineTo(-65,-60);c.quadraticCurveTo(-160,-90,-126,-196+sway);c.closePath();c.fillStyle=P.red;c.fill();H.line(c,-149,-197+sway,-126,-196+sway,P.ink,2)});
R('copy_network',(c,t,o)=>{sheet(c,-25,-175,50,58,P.blue);for(let j=0;j<5;j++){const x=-220+j*110;H.line(c,0,-112,x,-46,P.blue,1);if(age(o)>j*.3)sheet(c,x-25,-45,50,58,P.blue)}});
R('recruitment_notice',(c,t,o)=>{H.panel(c,-105,-130,210,130);H.rect(c,-105,-130,210,32,P.green);H.text(c,'নিয়োগ',0,-106,24,P.paper,'center');for(let j=0;j<3;j++){H.line(c,-85,-75+j*22,85,-75+j*22,P.slate,2);if(o.closed)H.line(c,-85,-80+j*22,85,-80+j*22,P.red,2)}});
R('demand_flow',(c,t,o)=>{for(let j=0;j<8;j++){const x=-170+j%4*95,y=-50-Math.floor(j/4)*100;const show=o.growing?age(o)>.2*j:true;if(show){sheet(c,x,y-65,58,66);H.line(c,x+28,y+5,0,50,P.blue,1)}}H.rect(c,-45,40,90,25,P.blue)});
R('history_ledger',(c,t,o)=>{H.panel(c,-210,-250,420,250);H.text(c,'কেরানি',-105,-213,25,P.ink,'center');H.text(c,'অ্যাকাউন্ট্যান্ট',100,-213,24,P.ink,'center');for(let j=0;j<4;j++){TuragCharacters.icon(c,-165+j*36,-154,35,P.grey);H.line(c,-177+j*36,-184,-153+j*36,-152,P.red,2)}for(let j=0;j<6;j++)TuragCharacters.icon(c,28+j%3*50,-152+Math.floor(j/3)*48,35,P.red);H.text(c,'−৪ লাখ',-105,-37,34,P.red,'center');H.text(c,'+৬ লাখ',105,-37,34,P.blue,'center')});
R('village_hut',(c,t,o)=>{H.rect(c,-70,-110,140,110,P.pale,P.ink);H.poly(c,[[-85,-110],[0,-165],[85,-110]],P.slate);H.rect(c,-17,-58,34,58,P.ink);H.rect(c,33,-77,25,28,P.blue);for(let j=0;j<10;j++)H.line(c,-67+j*14,-108,-67+j*14,0,'rgba(18,20,28,.15)',1)});
R('health_route',(c,t,o)=>{H.orb(c,0,0,18,t);c.save();c.setLineDash([5,5]);for(const x of[-270,270]){c.beginPath();c.moveTo(0,0);c.quadraticCurveTo(x*.6,-100,x,110);c.strokeStyle=P.blue;c.lineWidth=2;c.stroke()}c.restore()});
R('bounded_requests',(c,t,o)=>{H.rect(c,-185,-175,370,175,P.paper,P.ink);for(let j=0;j<12;j++){const x=-170+j%6*58,y=-160+Math.floor(j/6)*76;sheet(c,x,y,45,60,j<8?P.pale:P.blue)}H.rect(c,-185,0,370,12,P.slate)});
R('magnifier',(c,t,o)=>{const x=Math.sin(age(o)*.8)*30;c.save();c.translate(x,0);c.beginPath();c.arc(0,-30,35,0,Math.PI*2);c.strokeStyle=P.ink;c.lineWidth=4;c.stroke();H.line(c,25,-5,65,40,P.ink,6);c.restore()});
R('podium',(c,t,o)=>{H.poly(c,[[-65,0],[65,0],[50,-95],[-50,-95]],P.slate);H.rect(c,-85,-110,170,15,P.ink);H.line(c,30,-110,46,-145,P.ink,2);H.oval(c,46,-145,4,4,P.ink)});
R('attribution_folder',(c,t,o)=>{H.panel(c,-160,-190,320,190);H.text(c,'খরচ কমানো',0,-137,31,P.ink,'center');if(age(o)>.7){c.save();c.rotate(-.05);H.rect(c,-130,-108,260,74,P.blue);H.text(c,'AI',0,-56,45,P.paper,'center');c.restore()}});
R('rank_list',(c,t,o)=>{H.panel(c,-210,-260,420,260,P.ink);for(let j=0;j<5;j++){const y=-230+j*47;H.text(c,String(j+1).replace(/[0-9]/g,n=>'০১২৩৪৫৬৭৮৯'[n]),-180,y+19,26,P.paper);H.rect(c,-140,y,300,29,j===4?P.blue:P.slate);if(j===4)H.text(c,'AI',0,y+23,25,P.paper,'center')}});
R('partial_picture',(c,t,o)=>{H.panel(c,-210,-245,420,245);H.rect(c,-210,-245,420,100,P.paper,P.ink);H.text(c,'ছাঁটাইয়ের তালিকা',0,-190,31,P.ink,'center');H.rect(c,-210,-145,420,145,P.slate);H.text(c,'নিয়োগ না হওয়া',0,-95,29,P.paper,'center');for(let j=0;j<4;j++){H.line(c,-130+j*85,-65,-130+j*85,-20,P.paper,2);H.line(c,-130+j*85,-40,-95+j*85,-40,P.paper,2)}});
R('late_report_wave',(c,t,o)=>{const h=35+ease(age(o)/4)*65;c.beginPath();c.moveTo(-480,20);for(let x=-480;x<=480;x+=10)c.lineTo(x,-h+Math.sin(x*.03+age(o))*7);c.lineTo(480,20);c.closePath();c.fillStyle=P.blue;c.fill();H.dots(c,-480,-h,960,h,P.ink,8,1.1)});
R('mobile_shop',(c,t,o)=>{H.rect(c,-110,-210,220,210,P.slate);H.rect(c,-120,-220,240,37,P.green);H.text(c,'মোবাইল ব্যাংকিং',0,-192,24,P.paper,'center');H.rect(c,-95,-165,190,100,P.ink);for(let j=0;j<4;j++)H.rect(c,-85+j*46,-155,36,24,j%2?P.blue:P.red);H.rect(c,-100,-55,200,55,P.pale);H.text(c,'লেনদেন',0,-19,24,P.ink,'center')});
R('speed_bump',(c,t,o)=>{H.poly(c,[[-70,0],[-50,-12],[50,-12],[70,0]],P.paper);for(let j=0;j<6;j++)H.line(c,-55+j*20,-2,-45+j*20,-10,P.ink,4)});
R('audit_tasks',(c,t,o)=>{const names=['ইমেইল','রিপোর্ট','ডাটা','পরিকল্পনা','সিদ্ধান্ত','যোগাযোগ'];for(let j=0;j<6;j++){const x=-160+j%3*113,y=-110+Math.floor(j/3)*90,ai=j<Math.round((o.progress||.5)*6);H.panel(c,x-48,y-30,96,65,ai?P.blue:P.paper);H.text(c,names[j],x,y+9,18,ai?P.paper:P.ink,'center',88);if(o.emphasizeHuman&&!ai){H.rect(c,x-50,y+39,100,6,P.red);H.line(c,x-52,y-34,x+52,y-34,P.red,2)}}});
})();
(function(){const H=TuragScenes.helpers,P=TuragScenes.palette,R=TuragComposer.register;
R('engine',(c,t,o)=>{H.rect(c,-65,-100,130,72,P.slate);for(let i=0;i<4;i++)H.rect(c,-54+i*29,-119,19,22,P.ink);H.oval(c,-36,-8,20,20,P.ink);H.oval(c,43,-8,20,20,P.ink);H.rect(c,-34,-70,68,20,P.blue)});
R('car',(c,t,o)=>{H.poly(c,[[-100,-35],[-80,-68],[-40,-75],[-15,-111],[55,-111],[84,-71],[107,-56],[107,-20],[-100,-20]],P.slate);H.rect(c,-10,-102,57,30,P.paper);for(const x of [-59,68])H.oval(c,x,-15,21,21,P.ink)});
R('harvester',(c,t,o)=>{H.rect(c,-100,-100,140,75,P.pale,P.ink);H.rect(c,10,-152,57,80,P.green);H.rect(c,19,-143,38,34,P.paper);H.rect(c,-115,-49,220,15,P.slate);for(let i=0;i<11;i++)H.line(c,-110+i*20,-50,-121+i*20,-18,P.ink,3);H.oval(c,-60,-15,26,26,P.ink);H.oval(c,64,-15,26,26,P.ink)});
R('blackboard',(c,t,o)=>{H.rect(c,-115,-200,230,120,P.green,P.slate);H.text(c,o.text||'ক খ গ',0,-135,38,P.paper,'center',210);H.line(c,-95,-108,95,-108,P.paper,2)});
R('task',(c,t,o)=>{H.panel(c,-43,-55,86,55,o.ai?P.blue:P.paper);H.text(c,o.text||'কাজ',0,-19,17,o.ai?P.paper:P.ink,'center',76)});
R('clock',(c,t,o)=>{H.oval(c,0,-60,43,43,P.paper);H.line(c,0,-60,0,-88,P.ink,2);H.line(c,0,-60,25,-46,P.red,2)});
R('hammock',(c,t,o)=>{H.palm(c,-150,0,200,t);H.palm(c,160,0,200,t);c.beginPath();c.moveTo(-142,-194);c.quadraticCurveTo(0,-80,168,-194);c.strokeStyle=P.ink;c.lineWidth=3;c.stroke();H.line(c,-83,-143,50,-125,P.red,17);H.line(c,50,-125,110,-144,P.ink,13);H.oval(c,-92,-149,12,12,P.ink)});
R('sewing_machine',(c)=>{H.rect(c,-65,-10,130,8,P.slate);H.poly(c,[[-48,-12],[-48,-75],[12,-75],[32,-58],[32,-28],[15,-28],[10,-55],[-19,-55],[-19,-12]],P.slate);H.line(c,22,-29,22,-13,P.ink,2);H.rect(c,34,-22,53,11,P.red)});
R('envelope',(c,t,o)=>{H.rect(c,-38,-48,76,48,P.paper,P.ink);H.line(c,-38,-48,0,-20,P.ink);H.line(c,38,-48,0,-20,P.ink);H.oval(c,0,-20,4,4,P.red)});
R('chart',(c,t,o)=>{H.panel(c,-175,-210,350,210);for(let i=0;i<5;i++)H.line(c,-160,-180+i*35,160,-180+i*35,P.pale,1);const values=Array.isArray(o.points)&&o.points.length>1?o.points:Array.from({length:17},(_,i)=>50+Math.sin(i*2)*7),lo=Math.min(...values),hi=Math.max(...values),span=Math.max(1,hi-lo),u=Math.max(0,Math.min(1,(o.localTime||0)/(o.seconds||1.3))),p=1-Math.pow(1-u,3),progress=Math.max(1,Math.ceil(values.length*p));for(let i=1;i<progress;i++){const x1=-155+(i-1)*310/(values.length-1),x2=-155+i*310/(values.length-1),y1=-25-(values[i-1]-lo)/span*145,y2=-25-(values[i]-lo)/span*145;H.line(c,x1,y1,x2,y2,o.color||P.ink,4)}if(o.label)H.mono(c,o.label,-155,-188,13,o.color||P.ink)});
})();
/* Supporting-detail props learned from the complete second image folder.
 * They remain independent objects, so the director composes their arrangement. */
(function(){const H=TuragScenes.helpers,P=TuragScenes.palette,R=TuragComposer.register;
R('tea_stall',(c,t,o)=>{H.rect(c,-100,-165,200,8,P.ink);H.poly(c,[[-110,-157],[110,-157],[98,-130],[-98,-130]],P.red);for(let i=0;i<9;i++)H.rect(c,-96+i*23,-156,11,25,P.paper);H.rect(c,-89,-130,3,130,P.ink);H.rect(c,87,-130,3,130,P.ink);H.rect(c,-84,-42,168,42,P.slate);H.rect(c,-84,-48,168,6,P.ink);for(let i=0;i<5;i++){H.rect(c,-56+i*23,-64,15,16,i%2?P.pale:P.paper);H.rect(c,-56+i*23,-67,15,3,P.red)}H.rect(c,-48,-158,96,26,P.paper);H.text(c,o.label||'গরম চা',0,-139,18,P.red,'center',90)});
R('rickshaw',(c,t,o)=>{H.oval(c,-47,-19,20,20,P.ink);H.oval(c,53,-19,20,20,P.ink);H.poly(c,[[-70,-40],[-56,-99],[-14,-124],[42,-116],[74,-80],[72,-29]],P.green);H.rect(c,-53,-93,53,44,P.ink);for(let i=0;i<4;i++)H.line(c,-43+i*11,-93,-43+i*11,-49,P.pale,2);H.rect(c,16,-76,42,35,P.paper);H.rect(c,-72,-34,145,9,P.slate)});
R('window',(c,t,o)=>{const w=o.w||190,h=o.h||150;H.rect(c,-w/2,-h,w,h,o.night?P.ink:P.pale,P.slate);for(let i=1;i<4;i++)H.line(c,-w/2+i*w/4,-h,-w/2+i*w/4,0,P.slate,3);H.line(c,-w/2,-h*.48,w/2,-h*.48,P.slate,3);if(o.night)for(let i=0;i<12;i++)if(i%3)H.rect(c,-w*.45+i%6*w/6,-h*.4+Math.floor(i/6)*h*.2,7,9,P.paper)});
R('fan',(c,t,o)=>{H.line(c,0,-75,0,-7,P.ink,2);c.save();c.rotate(Math.sin(t*3)*.08);H.oval(c,-32,0,34,6,P.ink);H.oval(c,32,0,34,6,P.ink);c.restore();H.oval(c,0,0,7,7,P.ink)});
R('plant',(c,t,o)=>{H.poly(c,[[-20,-32],[20,-32],[14,0],[-14,0]],P.red);for(let i=0;i<5;i++){const x=(i-2)*14;H.poly(c,[[0,-32],[x-7,-70-i%2*32],[x+5,-100-i%2*16],[x+11,-65],[4,-32]],P.green)}});
R('television',(c,t,o)=>{H.rect(c,-170,-270,340,186,P.ink);H.rect(c,-160,-260,320,166,o.ai?P.blue:P.slate);const cols=o.cols||7,n=o.cells??35;for(let i=0;i<n;i++){const x=-145+i%cols*43,y=-245+Math.floor(i/cols)*28;H.rect(c,x,y,36,21,i<(o.active??10)?P.red:P.grey);H.rect(c,x+13,y+7,9,6,P.paper)}H.rect(c,-160,-71,320,8,P.ink);H.rect(c,-158,-63,316,63,P.slate);for(let i=0;i<3;i++){H.rect(c,-148+i*104,-55,96,43,P.ink);H.rect(c,-109+i*104,-44,18,3,P.pale)}});
R('filing_cabinet',(c,t,o)=>{H.rect(c,-39,-190,78,190,P.slate);for(let i=0;i<4;i++){H.rect(c,-34,-183+i*44,68,38,P.grey);H.rect(c,-10,-171+i*44,20,4,P.paper)}});
R('clipboard',(c,t,o)=>{H.panel(c,-55,-158,110,158);H.rect(c,-22,-168,44,19,P.slate);for(let i=0;i<5;i++){H.rect(c,-40,-125+i*24,9,9,P.paper,P.ink);H.line(c,-21,-120+i*24,40,-120+i*24,P.slate,1.5);if(i<(o.checked||0))H.check(c,-40,-124+i*24,8,P.red)}});
R('conveyor',(c,t,o)=>{H.rect(c,-170,-22,340,22,P.slate);for(let x=-160;x<170;x+=18)H.oval(c,x,-11,4,4,P.pale);for(let i=0;i<7;i++){const x=-160+((t*22+i*48)%320);H.rect(c,x,-58,35,35,x>0?P.blue:P.paper,P.ink)}H.rect(c,-27,-145,62,123,P.blue);H.orb(c,4,-104,19,t)});
})();
/* Grounded office and professional-room components for the opening minute. */
(function(){const H=TuragScenes.helpers,P=TuragScenes.palette,R=TuragComposer.register;
R('office_windowwall',(c,t,o)=>{c.save();c.beginPath();c.rect(-480,-440,960,290);c.clip();H.skyline(c,-135,'#383C50',true);c.restore();for(let i=0;i<8;i++)H.rect(c,-480+i*142,-455,5,315,P.ink);H.rect(c,-480,-150,960,165,'#2C3040');H.dots(c,-480,-150,960,165,'rgba(140,145,166,.20)',8,1.4);H.rect(c,334,-400,72,22,P.paper);H.mono(c,'EXIT →',342,-385,10,P.ink)});
R('office_station',(c,t,o)=>H.desk(c,0,0,o.s||1,t,o.color||P.grey,o.variant||0,!!o.ai));
R('workforce_card',(c,t,o)=>{H.panel(c,-150,-310,300,300);for(let i=0;i<100;i++)TuragCharacters.icon(c,-122+(i%10)*25,-267+Math.floor(i/10)*19,18,i<(o.active??25)?P.red:P.grey);H.text(c,o.text||'১/৪',-129,-31,60,P.red,'left',130);H.text(c,'প্রায় ৬০ হাজার কর্মী',10,-50,19,P.ink,'left',133);H.text(c,'কোম্পানির চার ভাগের এক ভাগ',10,-23,14,P.ink,'left',135)});
R('room_outline',(c,t,o)=>{c.save();c.setLineDash([5,3]);c.strokeStyle=P.ink;c.lineWidth=1.2;c.strokeRect(-130,-340,260,340);c.restore();H.tag(c,o.label||'',-114,-326,P.ink)});
})();
/* Articulated actors: real hand/forearm actions, not a bobbed static drawing. */
(function(){const H=TuragScenes.helpers,P=TuragScenes.palette,R=TuragComposer.register;
R('office_station',(c,t,o)=>{c.save();c.scale(o.s||1,o.s||1);const departed=o.departAt!==undefined&&t>=o.departAt;
 if(!departed)TuragCharacters.draw(c,{x:0,y:0,h:106,t,role:'extra',pose:'sit',variant:o.variant||0,color:o.color||P.grey,action:o.receiveAt!==undefined&&t>=o.receiveAt&&t<o.receiveAt+2.5?'take':'typing',actionTime:o.receiveAt!==undefined&&t>=o.receiveAt&&t<o.receiveAt+2.5?t-o.receiveAt:t,phase:(o.variant||0)*1.73});
 H.monitor(c,45,-105,62,!!o.ai);H.rect(c,8,-54,116,5,P.slate);H.rect(c,12,-49,3,49,P.slate);H.rect(c,116,-49,3,49,P.slate);H.rect(c,20,-57,25,3,P.pale);
 if(departed&&t-o.departAt<6)TuragCharacters.draw(c,{x:18+(t-o.departAt)*33,y:0,h:106,t,role:'extra',variant:o.variant||0,pose:'walk',action:'carry',phase:(o.variant||0)*1.73});c.restore();});
R('count_number',(c,t,o)=>{const p=Math.min(1,Math.max(0,(o.localTime||0)/(o.seconds||2)));const n=Math.round((o.from||0)+((o.to||0)-(o.from||0))*(1-Math.pow(1-p,3)));H.hero(c,new Intl.NumberFormat('bn-BD').format(n),o.label||'',-(o.w||240)/2,-90,o.size||68)});
R('stat_tower',(c,t,o)=>{const w=o.w||90,h=o.h||120;H.rect(c,-w/2,-h,w,h,P.paper,P.ink);for(let x=-w/2+9;x<w/2;x+=12)H.line(c,x,-h,x,0,P.pale,.8);for(let y=-h;y<0;y+=12)H.line(c,-w/2,y,w/2,y,P.pale,.8);H.text(c,o.text||'',0,25,18,o.color||P.ink,'center',150);if(o.accent){c.save();c.setLineDash([5,4]);H.line(c,w/2+12,0,w/2+12,-h,P.red,2);c.restore();}});
R('chalk_strokes',(c,t,o)=>{const p=Math.max(0,Math.min(1,(o.localTime||0)/2));for(let i=0;i<3;i++){const q=Math.max(0,Math.min(1,(p-i*.25)*2));H.line(c,-40,-i*18,-40+75*q,-i*18,P.paper,2)}});
R('sewing_fabric',(c,t,o)=>{const move=(o.localTime||0)*9;H.rect(c,-25-move,-8,65,13,P.red);for(let i=0;i<4;i++)H.line(c,-20-move+i*14,-6,-20-move+i*14,3,P.pale,.7)});
})();
/* Reusable objects invented for the new script-directed opening. */
(function(){const H=TuragScenes.helpers,P=TuragScenes.palette,R=TuragComposer.register;
R('offer_letter',(c,t,o)=>{H.panel(c,-40,-75,80,75);H.text(c,'অফার',0,-49,17,P.red,'center',70);for(let j=0;j<3;j++)H.line(c,-28,-32+j*10,28,-32+j*10,P.slate,1)});
R('cash_packet',(c)=>{for(let j=0;j<4;j++)H.rect(c,-30+j*2,-20-j*3,60,25,P.green,P.ink);H.rect(c,-5,-29,13,34,P.paper)});
R('exit_door',(c)=>{H.rect(c,-50,-260,100,260,P.slate);H.rect(c,-43,-250,86,250,P.ink);H.rect(c,-40,-288,80,23,P.green);H.mono(c,'EXIT →',-30,-272,13,P.paper);H.oval(c,29,-119,3,3,P.paper)});
R('report_board',(c)=>{H.panel(c,-225,-300,450,300);H.mono(c,'EMPLOYMENT / REPORT',-200,-271,13,P.ink);H.line(c,-200,-255,200,-255,P.ink,2);for(let j=0;j<4;j++)H.line(c,-195,-80+j*17,195,-80+j*17,P.pale,2)});
R('claim_evidence',(c,t,o)=>{H.panel(c,-170,-180,340,180);H.text(c,'আমার কাজ এআই পারবে না',0,-110,26,P.ink,'center',310);H.line(c,-140,-65,140,-65,P.slate,2);const a=Math.min(1,(o.localTime||0)/1.2),x=-95+a*150;H.oval(c,x,-84,44,44,'rgba(233,228,210,.50)');c.strokeStyle=P.red;c.lineWidth=4;c.beginPath();c.arc(x,-84,44,0,Math.PI*2);c.stroke();H.line(c,x+31,-53,x+65,-15,P.ink,8)});
R('patient_bed',(c)=>{H.rect(c,-100,-95,220,9,P.slate);H.line(c,-100,-120,-100,0,P.slate,5);H.line(c,120,-95,120,0,P.slate,5);H.oval(c,-77,-117,13,13,P.slate);H.poly(c,[[-60,-128],[70,-123],[102,-101],[-60,-101]],P.pale);H.line(c,-55,-114,92,-108,P.grey,1)});
R('medical_stand',(c)=>{H.line(c,0,0,0,-210,P.slate,4);H.line(c,-22,-210,22,-210,P.slate,3);H.rect(c,5,-198,17,40,P.blue);H.line(c,14,-158,0,-92,P.slate,1);H.line(c,-23,0,23,0,P.slate,3)});
R('sewing_table',(c)=>{H.rect(c,-115,-82,260,7,P.slate);H.line(c,-105,-75,-105,0,P.slate,4);H.line(c,135,-75,135,0,P.slate,4);H.line(c,-60,-10,70,-10,P.slate,3)});
R('sewing_feed',(c,t,o)=>{const move=Math.min(30,(o.localTime||0)*10);H.rect(c,-60+move,-3,120,9,P.red);for(let j=0;j<8;j++)H.line(c,-55+move+j*14,0,-49+move+j*14,0,P.paper,1)});
R('sewing_machine_active',(c,t,o)=>{H.rect(c,-37,-5,100,5,P.slate);H.poly(c,[[50,-5],[50,-64],[-8,-64],[-30,-48],[-30,-23],[-15,-23],[-13,-44],[26,-44],[26,-5]],P.slate);H.line(c,-23,-23,-23,-7+Math.sin(t*30)*4,P.ink,2);H.oval(c,49,-43,12,12,P.ink);H.line(c,49,-43,49+8*Math.cos(t*14),-43+8*Math.sin(t*14),P.paper,2)});
R('fabric_rolls',(c)=>{for(let j=0;j<4;j++){H.rect(c,-40+j*20,-90-j%2*30,18,90+j%2*30,j%2?P.pale:P.green);H.oval(c,-31+j*20,-90-j%2*30,9,4,P.paper)}H.rect(c,-50,0,110,5,P.slate)});
R('lab_wall',(c,t)=>{H.rect(c,-180,-180,360,180,P.slate);for(let j=0;j<12;j++){const x=-163+j%4*84,y=-162+Math.floor(j/4)*49;H.rect(c,x,y,72,37,P.blue);for(let k=0;k<3;k++)H.line(c,x+7,y+9+k*8,x+20+((j+k)%4)*9,y+9+k*8,P.paper,1)}H.mono(c,'MODEL / TASKS',-163,-191,12,P.paper)});
})();
/* Chapter identity is shared across newly authored stories, not a story template. */
(function(){const H=TuragScenes.helpers,P=TuragScenes.palette;const masks=new Map();
TuragComposer.register('chapter_card',(c,t,o)=>{
 H.rect(c,0,0,960,540,P.blue);H.oval(c,704,280,171,171,P.red);
 const value=o.number||'০২',key=value;let glyph=masks.get(key);
 if(!glyph){glyph=document.createElement('canvas');glyph.width=960;glyph.height=540;const g=glyph.getContext('2d');H.text(g,value,680,425,370,P.paper,'center',430);g.globalCompositeOperation='source-atop';g.save();g.beginPath();g.rect(480,281,430,200);g.clip();for(let x=250;x<1000;x+=20)H.line(g,x,280,x+200,480,P.ink,8);g.restore();masks.set(key,glyph);}
 c.drawImage(glyph,0,0);H.mono(c,`CHAPTER ${String(o.chapter||2).padStart(2,'0')} / ${String(o.total||7).padStart(2,'0')}`,55,84,9,P.paper);
 H.text(c,o.line1||'সবার একটা',52,215,70,P.paper,'left',440);
 const second=o.line2||'অজুহাত';c.save();c.font='800 68px "Anek Bangla"';const w=Math.min(450,c.measureText(second).width+20);H.rect(c,52,242,w,67,P.ink);c.restore();H.text(c,second,62,294,68,P.paper,'left',430);
 c.save();c.setLineDash([12,6]);H.line(c,0,280,960,280,P.paper,2);c.restore();
});})();
/* Chalk is laid along the same reachable hand path as the teacher's rig. */
(function(){const H=TuragScenes.helpers,P=TuragScenes.palette;
TuragComposer.register('writing_marks',(c,t,o)=>{const h=o.actorHeight||190,end=Math.max(0,o.localTime||0),path=[];for(let at=0;at<=end;at+=.025){const p=TuragCharacters.handSocket({action:'write',actionTime:at,h,pose:'stand'});path.push([(o.actorX||0)+p[0]+.025*h,(o.actorY||0)+p[1]-.035*h]);}for(let i=1;i<path.length;i++)H.line(c,...path[i-1],...path[i],P.paper,1.5);});
TuragComposer.register('fan',(c,t)=>{H.line(c,0,-75,0,-7,P.ink,2);for(let j=0;j<3;j++){const a=t*2.4+j*Math.PI*2/3;H.line(c,0,0,Math.cos(a)*47,Math.sin(a)*8,P.ink,7)}H.oval(c,0,0,7,5,P.ink)});
})();
/* Interaction props. Their moving parts expose simple 0..1 controls so an AI
 * director can synchronize contact instead of faking motion with a static icon. */
(function(){const H=TuragScenes.helpers,P=TuragScenes.palette,R=TuragComposer.register,clamp=v=>Math.max(0,Math.min(1,Number(v)||0));
R('hinged_door',(c,t,o)=>{const q=clamp(o.open),w=o.w||105,h=o.h||250;H.rect(c,-w/2,-h,w,h,P.slate);c.save();c.transform(1,0,-q*.5,1,-w/2*q,0);H.rect(c,-w/2+7,-h+7,w-14,h-7,P.ink);H.oval(c,w*.28,-h*.48,4+q*2,4+q*2,P.paper);c.restore();});
R('live_drawer',(c,t,o)=>{const q=clamp(o.open),w=o.w||120;H.rect(c,-w/2,-90,w,90,P.slate);for(let j=0;j<3;j++){const active=j===(o.drawer??1),d=active?q*34:0;H.rect(c,-w/2+6,-82+j*27-d,w-12,22,active?P.paper:P.grey,P.ink);H.line(c,-10,-71+j*27-d,10,-71+j*27-d,P.slate,2)}});
R('hand_tool',(c,t,o)=>{const kind=o.kind||'pen';if(kind==='hammer'){H.rect(c,-5,-45,10,50,P.ink);H.rect(c,-24,-54,48,13,P.slate)}else if(kind==='wrench'){H.line(c,0,0,0,-42,P.slate,8);H.oval(c,0,-50,10,10,P.slate);H.oval(c,0,-50,5,5,P.paper)}else{H.line(c,0,0,4,-52,o.color||P.ink,4);H.poly(c,[[2,-52],[7,-52],[5,-61]],P.red)}});
R('drink_cup',(c,t,o)=>{H.poly(c,[[-15,-35],[17,-35],[13,0],[-11,0]],o.color||P.paper);c.strokeStyle=P.ink;c.lineWidth=2;c.stroke();c.beginPath();c.arc(18,-20,10,-Math.PI/2,Math.PI/2);c.stroke();if(o.steam!==false)for(let j=0;j<2;j++){const y=-48-((t*12+j*15)%30);H.line(c,-4+j*10,y,-1+j*10,y-9,P.slate,1)}});
R('rolling_cart',(c,t,o)=>{const d=Number(o.distance)||0,turn=d/17;H.rect(c,-70,-73,140,7,P.slate);H.line(c,-61,-66,-61,-14,P.slate,4);H.line(c,61,-66,61,-14,P.slate,4);for(const x of[-53,53]){H.oval(c,x,-10,12,12,P.ink);H.line(c,x,-10,x+Math.cos(turn)*9,-10+Math.sin(turn)*9,P.paper,2)}H.line(c,61,-73,86,-98,P.slate,4)});
R('flexible_sheet',(c,t,o)=>{const q=clamp(o.bend),w=o.w||85,h=o.h||60;c.beginPath();c.moveTo(-w/2,-h);c.quadraticCurveTo(0,-h-q*18,w/2,-h+q*7);c.lineTo(w/2,0);c.quadraticCurveTo(0,-q*9,-w/2,0);c.closePath();c.fillStyle=o.color||P.paper;c.fill();c.strokeStyle=P.ink;c.lineWidth=1.5;c.stroke();for(let j=0;j<3;j++)H.line(c,-w*.3,-h*.72+j*13,w*.28,-h*.68+j*13,P.slate,1)});
R('control_panel_live',(c,t,o)=>{const q=clamp(o.lever),pulse=.5+.5*Math.sin(t*5);H.panel(c,-80,-100,160,100);for(let j=0;j<3;j++)H.oval(c,-48+j*35,-72,8,8,j===(o.active??1)&&pulse>.5?P.red:P.grey);H.line(c,45,-18,45+Math.sin(q*1.7)*28,-18-Math.cos(q*1.7)*42,P.ink,7);H.oval(c,45,-18,8,8,P.slate)});
})();

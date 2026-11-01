"""AI-authored, line-specific storyboard. No keyword routing or scene templates."""
import json,re
from pathlib import Path
x=json.load(open('episodes/ep02-first-minute.json'))
def O(typ,x,y=455,**kw):return dict(type=typ,x=x,y=y,**kw)
def S(i,objects,intent,ref,back='paper'):
 b=x['beats'][i];b['shot']={'backdrop':back,'floor':True,'floorY':465 if i in [8,12] else 455,'objects':[dict(o,id=f's{i}-{j}',instant=o.get('enter',0)==0) for j,o in enumerate(objects)],'links':[]};b['visualIntent']=b['scriptLine']+' | '+intent;b['styleRefs']=[ref];b['continuity']='Shared guide identity and profession variants; this line has its own action and framing.'
R='reference/folder_audit/frames/fullsize/'
V='reference/analysis/scene_stills/'
# Keep only the opening office title from the previous reconstruction.
S(1,[O('calendar',200,330,scale=1.45,text='২৬',label='অক্টোবর'),O('label',525,145,text='মাইক্রোসফট',size=36),O('label',525,185,text='প্রায় ৬০ হাজার কর্মীকে অফার',size=25),O('window',735,310,w=180,h=100),O('person',455,h=185,variant=0,action='take',rightHandFrames=[[0,.32,-.50],[1,.27,-.67],[3,.28,-.65],[6,.28,-.65]]),O('desk',580,monitor=False,scale=1.3),O('offer_letter',17,2,scale=.55,attachTo='s1-4',hand='right',z=5),O('filing_cabinet',790,scale=.7)],'A dated offer arrives on the personnel desk; the worker reaches toward the letter.',V+'ref_002_night_office_offer.jpg')
S(2,[O('exit_door',780),O('person',320,h=200,role='extra',variant=3,action='explain'),O('person',515,h=200,role='extra',variant=0,dir=-1,action='take',rightHandFrames=[[0,.40,-.56],[.9,.32,-.57],[1.6,.26,-.67],[3,.26,-.67]]),O('desk',425,monitor=False,scale=1.6),O('cash_packet',-12,-4,scale=.6,attachTo='s2-2',hand='right',z=5),O('label',440,165,text='টাকা নেন → চাকরি ছাড়েন',size=36),O('envelope',402,344.6,scale=.45)],'Show an exit payment moving across the desk between employer and worker, with an exit door beyond.',V+'ref_002_night_office_offer.jpg')
S(3,[O('workforce_card',550,430,scale=1.08),O('person',240,h=190,role='guide',action='explain'),O('label',280,185,text='প্রায় ৬০ হাজার',size=35)],'A literal 100-person diagram highlights 25 positions; guide points to the quarter, without recycling the office.',V+'ref_003_office_headcount_card.jpg')
S(4,[*[O('building',180+j*200,h=190+j%2*60,label='কোম্পানি',enter=j*.15) for j in range(4)],*[O('person',135+j*195,h=105,variant=j,pose='walk',action='carry',motion={'kind':'walk','speed':18},phase=j) for j in range(4)],O('label',480,155,text='একটি কোম্পানির গল্প নয়',size=37)],'Four different company frontages and departing workers expand the story beyond Microsoft.',R+'f_0154.jpg','city')
S(5,[O('report_board',485,425),O('count_number',460,300,to=120000,seconds=2.4,label='আমেরিকা · প্রথম ৯ মাস',w=330,size=70),O('label',475,330,text='ছাঁটাইয়ের কারণ হিসেবে এআই',size=25,color='#2F3BFF'),O('person',175,h=175,role='guide',action='explain'),O('paper_stack',780,447,count=16),O('filing_cabinet',850,scale=.6)],'A report fills with the narrated US total and named AI cause; a rising counter is evidence, not a repeated street walk.',V+'ref_004_layoff_walkers_counter.jpg')
S(6,[O('calendar',225,320,text='২০২৫',label='পুরো বছর',scale=1.3),O('filing_cabinet',770),O('filing_cabinet',855,scale=.85),O('report_board',490,418,scale=.7),O('number',485,365,text='৫৫ হাজার',label='আগের পুরো বছরের হিসাব',w=260,size=54),O('paper_stack',690,447,count=8)],'Open the previous-year archive and isolate its 55-thousand total before comparing years.',R+'f_0199.jpg')
S(7,[O('stat_tower',400,430,w=115,h=110,text='২০২৫ · ১২ মাস',keyframes=[{'at':0,'h':2},{'at':.8,'h':110}]),O('stat_tower',650,430,w=115,h=240,text='চলতি বছর · ৯ মাস',accent=True,keyframes=[{'at':0,'h':2},{'at':1.4,'h':240}]),O('label',400,294,text='৫৫ হাজার',size=25),O('label',650,160,text='১.২ লাখ',size=32),O('label',220,185,text='দুই গুণের বেশি',size=34,maxWidth=270),O('person',170,h=155,role='guide',action='explain')],'Two towers share a baseline and an exact 120000:55000 height ratio, revealing more than double in less time.',R+'f_0199.jpg')
S(8,[O('palm',455,370,scale=.8),O('tea_stall',770,465),O('person',310,465,h=190,role='guide',action='phone'),O('person',610,465,h=135,variant=3,pose='sit',action='rest'),O('chat',390,230,text='আমার কাজ এআই পারবে না।',scale=1.2),O('rickshaw',90,415,scale=.5,motion={'kind':'walk','speed':25})],'Guide raises a phone while making the quoted claim at the established street tea stall.',R+'f_0009.jpg','street')
S(9,[O('claim_evidence',480,390),O('person',245,h=185,role='guide',action='explain'),O('label',480,160,text='আসলেই?',size=65,color='#FF3D17')],'Cut to a close evidence inspection: a magnifier travels over the claim, opening the question rather than replaying the street.',R+'f_0300.jpg')
S(10,[*[O('person',230+j*250,h=180,role='doctor' if j==0 else 'extra',variant=j,action='explain',phase=j,enter=j*.2) for j in range(3)],*[O('chat',250+j*250,255,text=s,enter=j*.5,scale=.9) for j,s in enumerate(['রোগী দেখা?','বাচ্চা পড়ানো?','সেলাই করা?'])]],'Three distinct professionals voice their own claims; this is a conversation, not three room templates.',R+'f_0067.jpg')
S(11,[O('window',750,310,w=190,h=135),O('patient_bed',565),O('person',370,h=200,role='doctor',action='examine'),O('medical_stand',730),O('label',480,155,text='রোগী দেখা এআই পারবে না?',size=35),O('plant',840,scale=.75)],'In a dedicated ward, doctor raises a report beside a lying patient, articulating both arms.',R+'f_0159.jpg')
S(12,[O('blackboard',600,430,scale=1.55,text='ক খ গ'),O('person',370,465,h=190,variant=1,action='write'),O('writing_marks',0,0,actorX=370,actorY=465,actorHeight=190),*[O('person',530+j*140,465,h=115,variant=j,pose='sit',action='rest') for j in range(3)],*[O('desk',577+j*140,465,monitor=False,scale=.7) for j in range(3)],O('fan',260,145),O('window',130,320,w=100,h=140)],'A teacher writes directly on a full classroom board; three seated students face their desks.',V+'ref_008_profession_rooms.jpg')
S(13,[O('window',750,305,w=170,h=125),O('person',285,h=210,variant=2,pose='sit',action='sew'),O('sewing_table',400),O('sewing_feed',395,369),O('sewing_machine_active',395,377),O('fabric_rolls',700),O('label',470,150,text='রোবট আবার সেলাই করবে নাকি?',size=34),O('fan',180,150)],'Close sewing-floor view: both hands feed cloth across the tabletop and the needle repeatedly penetrates it.',V+'ref_008_profession_rooms.jpg')
S(14,[O('window',220,310,w=280,h=190,night=True),O('lab_wall',650,320),*[O('office_station',210+j*210,s=1.1,ai=True,variant=j,phase=j*1.7) for j in range(3)],O('label',480,135,text='যারা এআইকে কাছ থেকে দেখছে…',size=34,color='#E9E4D2'),O('plant',860,scale=.8)],'Cut into a separate AI lab: three researchers type asynchronously beneath task displays, contrasting their proximity with casual confidence.',V+'ref_009_ai_lab_survey.jpg','night')
# Keep the title's office visible from the first frame.
for o in x['beats'][0]['shot']['objects']:
 if o['type'] in ['office_windowwall','office_station']:o['instant']=True
x['episodeNumber']='02'
x['cast']={'guide':{'role':'guide','variant':0,'color':'#FF3D17','legColor':'#272A3A'}}
for beat in x['beats']:
 for obj in beat['shot']['objects']:
  if obj.get('type')=='person' and obj.get('role')=='guide':obj['castId']='guide'
# Preserve the reference's editorial chapter identity within cue 10, without
# splitting or retiming its narration cue.
b=x['beats'][10]
for o in b['shot']['objects']:
 o['enter']=2.4+o.get('enter',0)
 if o['type']=='person':o['instant']=True
b['shot']['objects'].append(dict(id='chapter-02-card',type='chapter_card',x=0,y=0,number='০২',chapter=2,total=7,line1='সবার একটা',line2='অজুহাত',enter=0,exit=2.4,z=100,instant=True))
b['styleRefs'].append(V+'ref_007_chapter_two_card.jpg')
b['visualIntent']+=' First 2.4 seconds preserve the blue chapter card and striped 02 from the reference, followed by the three professional claims.'
x['progressDuration']=637.166667
x['revisionNotes']='Restored 41–43.4s blue chapter card; retained full-episode progress scale; removed inferred calendar year from comparison.'
x['directorVersion']=1
x['episodeDesign']={
 'thesis':'Job safety beliefs weaken when the scale, speed and breadth of AI-linked work change become visible.',
 'emotionalArc':'Begin with unease, move through concrete evidence, confront confident excuses, then enter specific professions.',
 'chapterArc':['Immediate evidence: offer and layoffs','Beliefs: why each profession feels protected'],
 'castBible':{'guide':'Same vermilion shirt, dark trousers and profile hair in every return.','extras':'Slender faceless variants retain profession clothing and hair.'},
 'locationBible':{'street':'Established tea stall, palm, road and city depth retain geography.','workplaces':'Grounded furniture, thin rails, windows and task-specific tools.'},
 'visualMotifs':['evidence cards become physical environments','red marks risk or disputed confidence','blue marks AI systems and chapter pages'],
 'densityRhythm':'Dense office opening, sparse evidence diagrams, grounded street pause, full blue chapter reset, then medium-density profession rooms.',
 'chapterCardPlan':[{'at':41,'chapter':2,'treatment':'Blue page, red disc, striped Bengali 02 and cream/black headline.'}],
 'continuityRisks':['Guide identity drift','cream clothing disappearing on paper','held props separating from hands','statistics losing a shared scale']}
SEM=[
 ('viewer','questions job safety','night office','title question','uneasy'),
 ('Microsoft and worker','worker receives a dated offer','personnel office','26 October; about 60 thousand','factual'),
 ('employer and worker','money is exchanged for departure','exit desk','take money and leave job','blunt'),
 ('guide and workforce','guide reveals one quarter of the company','headcount diagram','60 thousand is about one quarter','explanatory'),
 ('workers across companies','workers leave several employers','city institutions','not Microsoft alone','expanding'),
 ('guide and report','counter rises to the narrated US layoff total','evidence desk','first nine months; about 120 thousand; AI named','evidentiary'),
 ('archive records','previous full-year total is retrieved','records archive','2025; about 55 thousand','measured'),
 ('guide and two totals','same-scale towers expose the ratio','comparison stage','nine months exceeds twice the prior full year','confronting'),
 ('guide','guide raises the quoted belief on his phone','established street','quote: my work cannot be done by AI','confident'),
 ('guide and claim','magnifier tests the confidence claim','evidence close-up','question rather than assertion','skeptical'),
 ('doctor teacher garment worker','three people voice different excuses','claim stage','everyone has an excuse','observational'),
 ('doctor and patient','doctor checks the patient report','hospital ward','doctor claims patient care is protected','professional confidence'),
 ('teacher and students','teacher writes while students attend','classroom','teacher claims children need a teacher','professional confidence'),
 ('garment worker','worker feeds cloth through the sewing machine','sewing floor','worker doubts robot sewing','professional confidence'),
 ('AI workers','researchers actively operate AI systems','AI lab','closest observers are less relaxed','uneasy reversal')]
DEC=[
 ('editorial title inside a working office','headline occupies negative space above two active desk rows','title resolves from cream to red question word','all monitors and workers establish a functioning workplace','slow settle from title to evidence','hard cut to dated offer','The threatened subject is visible before the argument begins.'),
 ('grounded offer handoff','large calendar anchors left while worker and letter anchor center','letter settles into the worker hand','hand closes on the offer beside the dated calendar','static evidence framing','cut closer to exchange desk','Date, company and offer are read in one glance.'),
 ('physical exchange','two people face across one desk with exit door beyond','cash reaches the worker while resignation envelope stays on desk','cash packet meets the receiving wrist','locked bilateral framing','cut to abstract headcount','The line becomes an unmistakable transaction and consequence.'),
 ('literal proportion grid','guide stands beside a hundred-person card','twenty-five figures separate in vermilion','guide points at the highlighted quarter','balanced guide and data framing','expand outward to multiple companies','Literal geometry protects the numerical relationship.'),
 ('institution row with departures','four varied buildings share one baseline','box-carrying workers cross different doors','departures occur across the whole row','wide lateral observation','cut to national report board','Breadth is shown by multiple employers rather than repeated text.'),
 ('evidence report and counter','guide frames a large report with records at right','counter climbs to 120000 and holds','number resolves while AI-cause caption remains attached','fixed evidence hierarchy','cut backward into archive','The report format distinguishes evidence from a decorative statistic.'),
 ('archive retrieval','calendar and stored files surround a previous-year report','the 55000 total is isolated from stored records','previous-year number holds alone','quiet archival framing','cut to shared-scale comparison','The past total is established before using it in a ratio.'),
 ('shared-baseline towers','guide, short tower and tall tower read left to right','both towers grow on one scale','120000 tower settles above twice 55000 height','wide comparison framing','cut to human belief on street','Common baseline makes the relationship visible without invented data.'),
 ('established street claim','guide and speech card sit within tea-stall geography','phone rises and quoted belief appears','phone reaches eye line as claim holds','stable street tableau','cut into claim detail','A recurring human place grounds the belief as something people say.'),
 ('magnified claim inspection','guide faces a large claim card and moving lens','lens crosses the claim text','red lens rests over the confidence phrase','close evidence framing','blue chapter reset','Inspection turns the rhetorical question into a visual action.'),
 ('chapter reset then claim chorus','full blue chapter page yields to three spaced speakers','chapter exits and claim cards appear in sequence','third professional completes the chorus','editorial reset then wide trio','cut into first profession room','The chapter card preserves series identity before expanding the excuses.'),
 ('specific hospital task','doctor, patient bed and IV form a grounded ward','doctor lifts and reads the report','report reaches the doctor gaze beside patient','medium ward framing','cut to classroom','The claim is embodied by real patient work rather than a generic doctor icon.'),
 ('specific classroom task','teacher occupies board edge while students form a seated row','chalk path grows under the actual hand','chalk touches the board as students face forward','wide teaching tableau','cut to sewing close-up','Teacher identity comes from teaching action and a populated room.'),
 ('specific sewing task','worker hands, cloth, needle and table form one contact chain','cloth advances while needle cycles','both hands guide cloth beneath the needle','close task framing','cut to dark AI lab','Physical contact makes the profession credible and animated.'),
 ('active AI laboratory','three asynchronous operators sit below dense task displays','hands type at different phases while screens remain blue','multiple workers operate systems simultaneously','wide lab observation','hold into next argument','Proximity is expressed through active daily work with the system.')]
# Archive evidence is retrieved and revealed, then held for reading.
archive=x['beats'][6]['shot']['objects']
archive[1].update(type='live_drawer',keyframes=[{'at':0,'open':0},{'at':.55,'open':1},{'at':2.5,'open':1}])
archive[4].update(keyframes=[{'at':0,'opacity':0,'y':390},{'at':.65,'opacity':1,'y':365}])
# The operators remain restrained; task indicators provide visible system response.
x['beats'][14]['shot']['objects'].append(dict(id='lab-controls',type='control_panel_live',x=815,y=375,scale=.6,instant=True,keyframes=[{'at':0,'lever':0},{'at':.7,'lever':.8},{'at':1.2,'lever':.65}]))
for i,b in enumerate(x['beats']):
 actors,action,setting,fact,tone=SEM[i];mechanism,composition,change,peak,camera,transition,why=DEC[i]
 b['semanticAnalysis']={'actors':[actors],'action':action,'setting':setting,'facts':[fact],
  'relationship':fact,'tone':tone,'negation':'Preserve any quoted denial or not-alone relationship exactly.','uncertainty':'Keep approximate quantities approximate.','notes':'Read with neighboring cues; do not turn belief into verified fact.'}
 b['designDecision']={'alternatives':[f'Literal reenactment centered on {actors}.',f'Abstract evidence diagram for {fact}.'],
  'mechanism':mechanism,'composition':composition,'visibleChange':change,
  'actionPeak':peak,'cameraPurpose':camera,'transition':transition,'why':why}
 b['referenceUse']=['Borrow staging, silhouette density, material and motion mechanism from '+Path(r).name+'.' for r in b['styleRefs']]
 copy=[];numbers=[]
 for obj in b['shot']['objects']:
  for key in ['text','label','line1','line2','value','number']:
   if obj.get(key) not in [None,'']:
    value=str(obj[key]);copy.append({'text':value,'basis':'script' if value in b['scriptLine'] else 'editorial','explanation':'Wording either quotes the cue or condenses its stated meaning without adding a claim.'})
    numbers += re.findall(r'[0-9০-৯][0-9০-৯, ]*',value)
  for key in ['count','active','to','from_']:
   if key in obj:numbers.append(str(obj[key]))
 b['copyLedger']=copy
 b['factBasis']=[{'value':v,'basis':'script' if any(ch in b['scriptLine'] for ch in v.strip()) else ('editorial' if i in [0,10] else 'derived'),
  'explanation':'Value is supplied by the cue, derived from its stated relationship, or used as documented editorial identity.'} for v in dict.fromkeys(numbers)]
 b['continuity']={'cast':'Guide identity and each profession variant remain stable.','place':setting+' retains grounded furniture and baseline.','props':'Returning records, phones and tools retain silhouette and palette.'}
 b['animationPlan']={'primaryAction':action,'motivation':why,
  'anticipation':actors+' orient head and weight toward the acting object before contact.',
  'contact':peak+'; hands and any held prop share the same rig socket.',
  'weightShift':'Standing actors shift over the supporting foot; seated actors remain anchored through hips and chair.',
  'actionPeak':peak,'followThrough':'The action settles with a readable hold before '+transition+'.',
  'secondaryMotion':setting+' uses offset breathing, tool response or environmental motion without synchronized looping.',
  'gaze':'Head direction leads toward the active hand, evidence or conversation partner.',
  'cameraMotivation':camera+' supports the narrated relationship rather than decorative drift.',
  'intentionalHold':False,'holdReason':''}
 b['review']={'start':'Opening state establishes '+setting+' with readable subject hierarchy.',
  'middle':'Action peak checked: '+peak+'.','end':'Final hold leaves the narrated relationship legible before '+transition+'.',
  'issues':['Checked hand contact, text collisions, floor contact and unsupported factual additions.'],
  'fixes':['Aligned held props to wrists, corrected baselines and separated text bands where required.'],'approved':True}
x['beats'][0]['visualIntent']='Open inside a dense working night office; the headline asks whether the viewer’s job is safe while the workplace remains active behind it.'
x['directorStatus']='approved'
x['planningStatus']='authored';x['planning']='Director-approved cue dossiers with distinct mechanisms, shared continuity, reference evidence, physical action and start/middle/end review.'
x['motionRevision']='Distinct line-specific sets; articulated hands; phone raise, report handling, writing, sewing feed and needle, asynchronous typing.'
Path('episodes/ep02-first-minute-revised.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')

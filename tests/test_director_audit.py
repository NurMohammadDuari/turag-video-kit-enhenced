import copy,json,subprocess,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class DirectorAuditTests(unittest.TestCase):
 def fixture(self):
  return {'title':'Test','directorVersion':1,'directorStatus':'approved',
   'episodeDesign':{'thesis':'A concrete argument about changing work','emotionalArc':'Concern moves toward informed action','densityRhythm':'Dense opening then quiet evidence','chapterArc':['Evidence'],'visualMotifs':['grounded tools']},
   'cues':[{'t0':0,'t1':2,'text':'Ten workers leave.'}],
   'beats':[{'id':'b','scene':'compose','scriptLine':'Ten workers leave.','visualIntent':'Ten workers cross an office exit and leave empty desks behind.',
    'semanticAnalysis':{'actors':['workers'],'action':'workers leave','setting':'office','facts':['ten'],'relationship':'departure creates vacancies','tone':'concern'},
    'designDecision':{'alternatives':['literal office departure','abstract vacancy grid'],'mechanism':'grounded departure','composition':'exit beside desks','visibleChange':'desks become empty','actionPeak':'last worker exits','cameraPurpose':'hold on absence','transition':'cut to evidence','why':'absence explains the consequence'},
    'styleRefs':['REFERENCE_FIRST.md'],'referenceUse':['Borrow grounded furniture scale and walking silhouettes from the reference evidence.'],
    'continuity':{'cast':'same workers','place':'same office','props':'same desks'},
    'animationPlan':{'primaryAction':'workers depart','motivation':'show the vacancy consequence','anticipation':'heads orient toward exit','contact':'hands grip carried boxes','weightShift':'weight crosses supporting feet','actionPeak':'last worker exits','followThrough':'empty desks remain held','secondaryMotion':'boxes respond to gait','gaze':'workers face the exit','cameraMotivation':'wide view preserves consequence','intentionalHold':False,'holdReason':''},
    'copyLedger':[],'factBasis':[],
    'review':{'start':'Office is fully occupied.','middle':'Workers cross toward exit.','end':'Empty desks remain visible.','issues':[],'fixes':[],'approved':True},
    'shot':{'backdrop':'office','objects':[{'id':'p','type':'person','x':200,'y':455,'pose':'walk'}]}}]}
 def run_audit(self,data):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'x.json';p.write_text(json.dumps(data));return subprocess.run(['python3',ROOT/'tools/director_audit.py',p],cwd=ROOT,capture_output=True,text=True)
 def test_complete_dossier_passes(self):self.assertEqual(self.run_audit(self.fixture()).returncode,0)
 def test_missing_alternatives_fails(self):
  x=self.fixture();x['beats'][0]['designDecision']['alternatives']=[]
  self.assertEqual(self.run_audit(x).returncode,2)
 def test_unledgered_copy_fails(self):
  x=self.fixture();x['beats'][0]['shot']['objects'].append({'id':'t','type':'label','x':400,'y':200,'text':'Unsupported 99'})
  self.assertEqual(self.run_audit(x).returncode,2)

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from scene_workspace import split, merge

class SceneWorkspaceTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name);self.source=self.root/'source.json';self.folder=self.root/'scenes'
  self.ep={'duration':2,'audio':'audio/example.mp3','directorStatus':'approved','cues':[{'t0':0,'t1':2,'text':'A person reads.'}],
   'beats':[{'id':'a','cueIndex':0,'scene':'compose','t0':0,'t1':2,'scriptLine':'A person reads.','visualIntent':'A person reads a letter.',
   'shot':{'objects':[{'id':'actor','type':'person','x':400,'y':455}]},'review':{'approved':True}}]}
  self.source.write_text(json.dumps(self.ep));split(self.source,self.folder)
 def packet(self,change):
  p=self.folder/'0001.json';data=json.loads(p.read_text());change(data);p.write_text(json.dumps(data))
 def test_round_trip_and_new_revision(self):
  out=self.root/'new.json';self.assertEqual(merge(self.source,self.folder,out),[])
  self.assertEqual(json.loads(out.read_text())['beats'],self.ep['beats'])
  with self.assertRaises(ValueError):merge(self.source,self.folder,out)
 def test_edit_invalidates_approval(self):
  self.packet(lambda d:d['beat']['shot']['objects'][0].update(x=500))
  out=self.root/'new.json';self.assertEqual(merge(self.source,self.folder,out),['a'])
  result=json.loads(out.read_text());self.assertEqual(result['directorStatus'],'draft');self.assertFalse(result['beats'][0]['review']['approved'])
 def test_script_change_rejected(self):
  self.packet(lambda d:d['beat'].update(scriptLine='Different words'))
  with self.assertRaises(ValueError):merge(self.source,self.folder,self.root/'new.json')
 def test_stale_source_rejected(self):
  changed=copy.deepcopy(self.ep);changed['title']='Changed';self.source.write_text(json.dumps(changed))
  with self.assertRaises(ValueError):merge(self.source,self.folder,self.root/'new.json')

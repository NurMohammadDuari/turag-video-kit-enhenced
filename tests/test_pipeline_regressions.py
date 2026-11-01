import copy,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from prepare_episode import parse_script,validate
class RegressionTests(unittest.TestCase):
 def fixture(self):
  return {'duration':2,'cues':[{'t0':0,'t1':2,'text':'A'}],'beats':[{'id':'b','t0':0,'t1':2,'cueIndex':0,'scene':'compose','scriptLine':'A','visualIntent':'A reaches for a letter','shot':{'objects':[{'id':'a','type':'person','x':100,'y':455}]}}]}
 def test_multiline_timecoded_text_kept(self):
  cues,_=parse_script('[00:00–00:02] First line\ncontinued narration\n[00:02–00:04] Next',4)
  self.assertEqual(cues[0]['text'],'First line continued narration')
 def test_bad_timestamp_not_silently_estimated(self):
  with self.assertRaises(ValueError):parse_script('[00:ab–00:04] Invalid',4)
 def test_cue_cannot_run_past_audio(self):
  e=self.fixture();e['cues'][0]['t1']=2.1
  with self.assertRaises(ValueError):validate(e)
 def test_bad_scene_data_rejected(self):
  for bad in [{'x':float('nan')},{'attachTo':'missing'},{'exit':-1},{'keyframes':[{'at':-1,'x':20}]}]:
   e=self.fixture();e['beats'][0]['shot']['objects'][0].update(bad)
   with self.assertRaises(ValueError):validate(e)
 def test_duplicate_object_ids_rejected(self):
  e=self.fixture();e['beats'][0]['shot']['objects']*=2
  with self.assertRaises(ValueError):validate(e)
 def test_beat_owns_its_cue_time(self):
  e=self.fixture();e['beats'][0]['t0']=.5
  with self.assertRaises(ValueError):validate(e)
 def test_valid_plan(self):
  validate(self.fixture())
  e=self.fixture();e['duration']=30;e['beats'][0]['t1']=30
  with self.assertRaises(ValueError):validate(e)
  e['tailHoldReason']='Verified silent end credits';validate(e)

 def test_invalid_seconds_rejected(self):
  with self.assertRaises(ValueError):parse_script('[00:75–01:20] Invalid',90)
 def test_partial_srt_must_not_drop_a_cue(self):
  text='1\n00:00:00,000 --> 00:00:01,000\nGood\n\n2\nwrong --> timestamp\nLost'
  with self.assertRaises(ValueError):parse_script(text,3)

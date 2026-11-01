import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from cast_registry import resolve_cast

class CastTests(unittest.TestCase):
 def episode(self):
  return {'cast':{'host':{'role':'guide','variant':0,'color':'#FF3D17'}},'beats':[{'id':'a','shot':{'objects':[{'id':'p','type':'person','castId':'host','action':'point'}]}}]}
 def test_resolve_without_mutating_source(self):
  ep=self.episode();out=resolve_cast(ep)
  self.assertEqual(out['beats'][0]['shot']['objects'][0]['role'],'guide')
  self.assertNotIn('role',ep['beats'][0]['shot']['objects'][0])
 def test_reject_drift(self):
  ep=self.episode();ep['beats'][0]['shot']['objects'][0]['variant']=3
  with self.assertRaises(ValueError):resolve_cast(ep)
 def test_reject_unknown(self):
  ep=self.episode();ep['beats'][0]['shot']['objects'][0]['castId']='missing'
  with self.assertRaises(ValueError):resolve_cast(ep)
 def test_reject_animated_identity(self):
  ep=self.episode();ep['beats'][0]['shot']['objects'][0]['keyframes']=[{'at':0,'color':'blue'}]
  with self.assertRaises(ValueError):resolve_cast(ep)

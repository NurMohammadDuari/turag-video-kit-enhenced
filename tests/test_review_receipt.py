import json
import tempfile
import unittest
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from review_receipt import digest,verify

class ReviewReceiptTests(unittest.TestCase):
 def test_changes_invalidate_review(self):
  with tempfile.TemporaryDirectory() as d:
   h=Path(d)/'player.html';r=Path(d)/'review.json';h.write_text('reviewed player')
   shot={'id':'a','approved':True,'unresolved':[]}
   shot.update({k:'Concrete inspection of this shot' for k in ['meaning','style','motion','contact','timing']})
   r.write_text(json.dumps({'htmlSha256':digest(h),'shots':[shot]}))
   verify(h,r,['a'])
   with self.assertRaises(ValueError):verify(h,r,['a','b'])
   h.write_text('edited player')
   with self.assertRaises(ValueError):verify(h,r,['a'])

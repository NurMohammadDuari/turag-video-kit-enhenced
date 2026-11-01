import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from export_handoff import timestamp

class HandoffTests(unittest.TestCase):
 def test_millisecond_carry(self):
  self.assertEqual(timestamp(59.9996),'00:01:00,000')
  self.assertEqual(timestamp(3600.125),'01:00:00,125')
  self.assertEqual(timestamp(0),'00:00:00,000')

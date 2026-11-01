"""Meaningful timing/parser regression checks; run python3 -m unittest discover -s tests."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from prepare_episode import parse_script, validate


class TimingTests(unittest.TestCase):
    def test_markdown_bengali_and_milliseconds(self):
        cues, method = parse_script('* **[00:01.5 – 00:04]** বাংলা কর্মী।', 5)
        self.assertEqual(cues, [{'t0': 1.5, 't1': 4, 'text': 'বাংলা কর্মী।'}])
        self.assertFalse(method['verified'])

    def test_srt_multiline(self):
        cues, _ = parse_script('1\n00:00:01,000 --> 00:00:02,500\nবাংলা\nকর্মী', 4)
        self.assertEqual(cues[0], {'t0': 1, 't1': 2.5, 'text': 'বাংলা কর্মী'})

    def test_untimed_never_claims_alignment(self):
        cues, method = parse_script('এক দুই\nতিন চার পাঁচ', 10)
        self.assertEqual(cues[-1]['t1'], 10)
        self.assertEqual(method['method'], 'estimated_word_weight')
        self.assertFalse(method['verified'])

    def test_rejects_gap_overlap_and_nonfinite(self):
        for beats in [[{'t0': 1, 't1': 5}], [{'t0': 0, 't1': 3}, {'t0': 2, 't1': 5}], [{'t0': 0, 't1': float('nan')}]]:
            with self.assertRaises(ValueError):
                validate({'duration': 5, 'cues': [{'t0': 0, 't1': 5}], 'beats': beats})


if __name__ == '__main__':
    unittest.main()

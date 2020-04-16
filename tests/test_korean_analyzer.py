"""
Reference: https://github.com/apache/lucene-solr/blob/master/lucene/analysis/nori/src/test/org/apache/lucene/analysis/ko/TestKoreanAnalyzer.java
"""

import unittest
from pynori.korean_analyzer import KoreanAnalyzer


## Initization
print('Initialize...')
analyzer = KoreanAnalyzer(pos_filter=True, decompound_mode='DISCARD')
analyzer_stoptags = KoreanAnalyzer(pos_filter=True, stop_tags=['NNP', 'NNG'], decompound_mode='DISCARD')

class TestKoreanAnalyzer(unittest.TestCase):

	def setUp(self):
		pass

	def do(self, kor_analyzer, token_attr, in_string):
		return kor_analyzer.do_analysis(in_string)[token_attr]

	def test_stoptags(self):

		self.assertEqual(self.do(analyzer, 'termAtt', "한국은 대단한 나라입니다."), ['한국', '대단', '나라', '이'])
		self.assertEqual(self.do(analyzer, 'offsetAtt', "한국은 대단한 나라입니다."), [(0, 2), (4, 6), (8, 10), (10, 13)])
		self.assertEqual(self.do(analyzer, 'posLengthAtt', "한국은 대단한 나라입니다."), [1, 1, 1, 1])
		self.assertEqual(self.do(analyzer_stoptags, 'termAtt', "한국은 대단한 나라입니다."), ['은', '대단', '하', 'ᆫ', '이', 'ᄇ니다'])
		self.assertEqual(self.do(analyzer_stoptags, 'offsetAtt', "한국은 대단한 나라입니다."), [(2, 3), (4, 6), (6, 7), (6, 7), (10, 13), (10, 13)])
		self.assertEqual(self.do(analyzer_stoptags, 'posLengthAtt', "한국은 대단한 나라입니다."), [1, 1, 1, 1, 1, 1])

	def tearDown(self):
		pass
		
		
if __name__ == '__main__':
	unittest.main()
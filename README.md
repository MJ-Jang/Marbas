# Pynori

Lucene Nori, Korean Mopological Analyzer, in Python

* Nori in Apache Lucene is a korean morpological analyzer based on Mecab.
* Pynori is a python-version of nori (Apache Lucene is written in Java).
* The analysis results are the same (All test cases are passed).
* Pynori maybe a little slower than nori because of python script language and less optimized data structures.
* Pynori includes mecab-ko-dic-2.1.1-20180720 for system dictionary.
* Pynori is compatible with Python 3.7 and is distributed under the Apache License 2.0.

자바로 작성되어 있는 아파치 루씬의 노리 형태소 분석기를 파이썬으로 변환한 프로젝트입니다. 원본과 같은 테스트를 실시하여 동일한 결과를 얻었습니다(ref.Test). 동의어 확장 필터는 제외하고 다른 기능은 모두 정상적으로 동작합니다. 정확도는 동일하지만 파이썬 언어인 점과 더불어 Trie 자료구조의 사용 등으로 속도는 조금 느립니다(ref.Property). 진행하지 못한 일들은 앞으로 보완할 계획입니다(ref.TODO).

노리 형태소 분석기에 대한 내용은 저의 [노리 Deep Dive 블로그](https://gritmind.github.io/2019/05/nori-deep-dive.html)를 참고해주세요.

## Install

```
pip install pynori
```


## Usage

```python

from pynori.korean_analyzer import KoreanAnalyzer
nori = KoreanAnalyzer(decompound_mode='MIXED',
                      discard_punctuation=True,
                      output_unknown_unigrams=True,
                      pos_filter=False,
                      stop_tags=['JKS', 'JKB', 'VV', 'EF'])

input_text = "아빠가 방에 들어가신다."
result = nori.do_analysis(input_text)
print(result)
>>>

{'termAtt': ['아빠', '가', '방', '에', '들어가', '시', 'ᆫ다'],
 'offsetAtt': [(0, 2), (2, 3), (4, 5), (5, 6), (7, 10), (10, 12), (10, 12)],
 'posLengthAtt': [1, 1, 1, 1, 1, 1, 1],
 'posTypeAtt': ['MORP', 'MORP', 'MORP', 'MORP', 'MORP', 'MORP', 'MORP'],
 'posTagAtt': ['NNG', 'JKS', 'NNG', 'JKB', 'VV', 'EP', 'EF'],
 'dictTypeAtt': ['KN', 'KN', 'KN', 'KN', 'KN', 'KN', 'KN']}
```

* argument에 따라 다르게 KoreanAnalyzer를 초기화
* result는 딕셔너리 타입이므로 원하는 key만 따로 출력 가능 (ex. result['termAtt'])

## Resources

* mecab-ko-dic-2.1.1-20180720 를 시스템 사전으로 사용
* 사용자 사전은 ~/pynori/resources/userdict_ko.txt 에서 수정 가능


## Test

```
git clone https://github.com/gritmind/python-nori.git
cd python-nori
python -m unittest -v tests.test_korean_analyzer
python -m unittest -v tests.test_korean_tokenizer
```

## Property

* Use mecab-ko-dic-2.1.1-20180720
* Based on lucene analyzer, nori
* Use Trie data structure, instead of FST
* Modify token & dictionary objects
* Not use circular buffer & wordID

## Improvement 
원본 루씬 노리 대비 개선점 (주의. general하지 않을 수도 있음)

* 특수문자로 시작되는 사용자 단어가 있을 시 동의어 처리가 되지 않는 오류
* Unknown 길이가 무분별하게 길어지는 현상


## TODO
* Synonym Graph Filter
* KoreanTokenizer TODO List (MAX_BACKTRACE_GAP, isLowSurrogate, UnicodeScript ...)
* Optimize algorithms and data structures, to be faster

## License
* Apache License 2.0

## Reference
* [Lucene-solr Nori](https://github.com/apache/lucene-solr/tree/master/lucene/analysis/nori)
* [Mecab-ko-dic](https://bitbucket.org/eunjeon/mecab-ko-dic/src/master/)


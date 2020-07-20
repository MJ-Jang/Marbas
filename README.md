# Marbas

Nori의 python 버전인 pynori를 커스터마이징이 용이하도록 수정


## Install

```
pip install git+https://github.com/MJ-Jang/Marbas
```

## Usage
### 1) User pattern 직접 input
```python
from marbas.marbas_tokenizer import MarbasTokenizer
tok = MarbasTokenizer(userdict_patterns=['바로 로밍|바로_NNG 로밍_NNG',
                                         '바로로밍|바로_NNG 로밍_NNG'])

print(tok.tokenize('바로 로밍 신청하려고요'))
print(tok.tokenize('바로로밍 좋아요'))
print(tok.tokenize('바로 집으로 튀어가라'))
```

### 2) User dictionary
유저가 정의한 pos tagging을 수행합니다.
##### a. dictionary format
```text
일시정지신청|일시정지_NNG 신청_NNG\n
홀리몰리|홀리_VV 몰리_NNG\n
중증급성호흡기증후군|중증_NNG 급성호흡기_NNG 증후군_NNG\n
```
##### b. usage
```python
from marbas.marbas_tokenizer import MarbasTokenizer

tok = MarbasTokenizer(path_userdict='test_userdict.txt')
print(tok.tokenize('홀리몰리~'))
```

### 3) Postprocess
오분석된 결과에 대한 수정을 진행합니다.
##### a. dictionary format
```text
중증급성호흡기증후군|중증_NNG 급성호흡기_NNG 증후군_NNG|중증_NNG 급성_NNG 호흡기_NNG 증후군_NNG
```
##### b. usage
```python
from marbas.marbas_tokenizer import MarbasTokenizer

tok = MarbasTokenizer(path_userdict='test_userdict.txt',
                      path_errorfix_dict='test_postpro_dict.txt')
print(tok.tokenize('중증급성호흡기증후군이 뭐에요?'))
```

### 4) Train, save, and load
Tokenizer를 쉽게 사용하기 위해 token -> index 사전을 구축하는 작업입니다. 
Default token list: UNK, START, END, PAD, CLS, SEP
```python
from marbas.marbas_tokenizer import MarbasTokenizer

tok = MarbasTokenizer(userdict_patterns=['바로 로밍|바로_NNG 로밍_NNG',
                                         '바로로밍|바로_NNG 로밍_NNG'],
                      path_userdict='test_userdict.txt',
                      path_errorfix_dict='test_postpro_dict.txt')
sents = ['일시정지 신청', '바로 로밍 신청하고 싶어요']
tok.train(sents)

print(tok.text_to_id('일시정지 신청'))
print(tok.token_to_id(tok.PAD))
```


## Resources
* 시스템 사전은 `~/pynori/resources/mecab-ko-dic-2.1.1-20180720` 에서 수정
   * 사전 변경사항은 다음 두 항목을 실시하면 곧바로 적용 가능
      * 기존 csv 파일 수정/삭제 or 새로운 csv 파일 추가 (주의. mecab 단어 작성 규칙)
      * 기존 `~/pynori/resources/pkl_mecab_csv/mecab_csv.pkl` 삭제
      * (참고. `mecab_csv.pkl` 파일이 없으면 KoreanAnalyzer 초기화 시에 최신 csv 파일을 기반으로 재생성)
      * (참고. `~/pynori/resources/pkl_mecab_matrix/matrix_def.pkl` 파일은 수정/삭제하지 말 것)
      * (참고. 다른 버전의 mecab-ko-dic 적용을 위해서는 코드 내의 path 수정 필요)

## License

* Apache License 2.0

## Reference
1. (Github) [Lucene-solr - Nori](https://github.com/apache/lucene-solr/tree/master/lucene/analysis/nori)
2. (Github) [Mecab-ko-dic](https://bitbucket.org/eunjeon/mecab-ko-dic/src/master/)
3. (Github) [Pynori](https://github.com/gritmind/python-nori)
3. (Blog) [엘라스틱서치 공식 한국어 분석 플러그인 '노리'](https://www.elastic.co/kr/blog/nori-the-official-elasticsearch-plugin-for-korean-language-analysis)
4. (Blog) [노리(Nori) 형태소 분석기 Deep Dive](https://gritmind.github.io/2019/05/nori-deep-dive.html)

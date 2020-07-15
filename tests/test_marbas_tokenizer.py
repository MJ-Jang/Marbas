from pynori.marbas_tokenizer import MarbasTokenizer

tok = MarbasTokenizer(userdict_patterns=['한글', '로밍', '일시정지 일시 정지'], path_userdict='pynori/resources/userdict_ko.txt')

tok.train(['나는 밥을 먹는다', '일시정지 신청해줘'])
tok.save_model('./', 'tmp')
tok.load_model('tmp.model')

tok.tokenize('일시정지 신청해줘')

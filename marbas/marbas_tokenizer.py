import os
import dill

from configparser import ConfigParser

from .korean_tokenizer import KoreanTokenizer
from .korean_posstop_filter import KoreanPOSStopFilter
from .synonym_graph_filter import SynonymGraphFilter
# from .preprocessing import Preprocessing
#
# from .korean_tokenizer import DcpdMode
# from .synonym_graph_filter import SynMode

from typing import Text, List
from tqdm import tqdm

cfg = ConfigParser()
# PATH_CUR = os.getcwd() + '/pynori'
PATH_CUR = os.path.dirname(__file__)
cfg.read(PATH_CUR + '/config.ini')

# OPTION
DECOMPOUND_MODE = cfg['OPTION']['DECOMPOUND_MODE']
INFL_DECOMPOUND_MODE = cfg['OPTION']['INFL_DECOMPOUND_MODE']
VERBOSE = cfg.getboolean('OPTION', 'VERBOSE')
OUTPUT_UNKNOWN_UNIGRAMS = cfg.getboolean('OPTION', 'OUTPUT_UNKNOWN_UNIGRAMS')
DISCARD_PUNCTUATION = cfg.getboolean('OPTION', 'DISCARD_PUNCTUATION')
# FILTER
USE_SYNONYM_FILTER = cfg.getboolean('FILTER', 'USE_SYNONYM_FILTER')
USE_POS_FILTER = cfg.getboolean('FILTER', 'USE_POS_FILTER')
MODE_SYNONYM_FILTER = cfg['FILTER']['MODE_SYNONYM_FILTER']


class MarbasTokenizer(object):
    """
    Pynori based Tokenizer for easy save, load and transforming to indexs
    """
    UNK = '<unk>'
    START = '<s>'
    END = '</s>'
    PAD = '<pad>'
    CLS = '<cls>'
    SEP = '<sep>'

    def __init__(self,
                 verbose=VERBOSE,
                 path_userdict=None,
                 userdict_patterns=None,
                 decompound_mode=DECOMPOUND_MODE,
                 infl_decompound_mode=INFL_DECOMPOUND_MODE,
                 output_unknown_unigrams=OUTPUT_UNKNOWN_UNIGRAMS,
                 discard_punctuation=DISCARD_PUNCTUATION,
                 pos_filter=USE_POS_FILTER,
                 stop_tags=KoreanPOSStopFilter.DEFAULT_STOP_TAGS,
                 synonym_filter=USE_SYNONYM_FILTER,
                 mode_synonym=MODE_SYNONYM_FILTER):

        self.kor_tokenizer = KoreanTokenizer(verbose,
                                             decompound_mode,
                                             infl_decompound_mode,
                                             output_unknown_unigrams,
                                             discard_punctuation,
                                             path_userdict,
                                             userdict_patterns)
        #
        # self.syn_graph_filter = None
        # if self.synonym_filter:  # SynonymGraphFilter 초기화 처리 지연 시간으로 True일 때만 활성.
        #     self.syn_graph_filter = SynonymGraphFilter(preprocessor=self.preprocessor,
        #                                                kor_tokenizer=self.kor_tokenizer,
        #                                                mode_synonym=self.mode_synonym)

        self.tok_to_id = {}
        self.id_to_tok = {}

        for i, v in enumerate([self.UNK, self.START, self.END, self.PAD, self.CLS, self.SEP]):
            self.tok_to_id[v] = i
            self.id_to_tok[i] = v

    def tokenize(self, in_string):
        """Analyze text input string and return tokens
            Filtering 순서에 유의. (POS -> SYNONYM)
        """
        ##############
        # Tokenizing #
        ##############
        self.kor_tokenizer.set_input(in_string)
        while self.kor_tokenizer.increment_token():
            pass
        tkn_attr_obj = self.kor_tokenizer.tkn_attr_obj

        outp = {
            'tokens': tkn_attr_obj.__dict__.get('termAtt'),
            'tags': tkn_attr_obj.__dict__.get('posTagAtt')
        }
        return outp

    def text_to_id(self, in_string):
        tokens = self.tokenize(in_string)['tokens']
        return [self.tok_to_id[t] for t in tokens]

    def token_to_id(self, token):
        idx = self.tok_to_id.get(token)
        if idx:
            return idx
        else:
            return self.tok_to_id.get(self.UNK)

    def set_option_tokenizer(self,
                             decompound_mode=None,
                             infl_decompound_mode=None,
                             output_unknown_unigrams=None,
                             discard_punctuation=None):
        if decompound_mode is not None:
            self.kor_tokenizer.mode = decompound_mode
        if infl_decompound_mode is not None:
            self.kor_tokenizer.infl_mode = infl_decompound_mode
        if output_unknown_unigrams is not None:
            self.kor_tokenizer.output_unknown_unigrams = output_unknown_unigrams
        if discard_punctuation is not None:
            self.kor_tokenizer.discard_punctuation = discard_punctuation
        pass

    def set_option_filter(self,
                          pos_filter=None,
                          stop_tags=None,
                          synonym_filter=None,
                          mode_synonym=None):
        # if pos_filter is not None:
        #     self.pos_filter = pos_filter
        # if stop_tags is not None:
        #     self.kor_pos_filter.stop_tags = stop_tags
        # if synonym_filter is not None or mode_synonym is not None:
        #     if self.synonym_filter or synonym_filter:
        #         # 주의: 현재 상태 모드의 kor_tokneizer가 입력.
        #         self.syn_graph_filter = SynonymGraphFilter(preprocessor=self.preprocessor,
        #                                                    kor_tokenizer=self.kor_tokenizer,
        #                                                    mode_synonym=mode_synonym)
        # if mode_synonym is not None:
        #     self.mode_synonym = mode_synonym
        # if synonym_filter is not None:
        #     self.synonym_filter = synonym_filter
        pass

    def train(self, sents: List):
        tokens = set()
        for s in tqdm(sents, desc='adding tokens'):
            res = self.tokenize(s)['tokens']
            for t in res:
                tokens.add(t)

        len_dict = len(self.id_to_tok)
        for i, t in enumerate(list(tokens)):
            self.id_to_tok[i+len_dict] = t
            self.tok_to_id[t] = i+len_dict

    def save_model(self, save_prefix: Text, save_path: Text = None):
        obj = {
            "tok_to_id": self.tok_to_id,
            "id_to_tok": self.id_to_tok,
            "entries": self.kor_tokenizer.entries
        }
        if not save_path:
            save_path = './'

        with open(os.path.join(save_path, save_prefix+'.model'), 'wb') as saveFile:
            dill.dump(obj, saveFile)

    def load_model(self, model_path: Text):
        with open(model_path, 'rb') as loadFile:
            res = dill.load(loadFile)

        self.tok_to_id = res['tok_to_id']
        self.id_to_tok = res['id_to_tok']

        self.kor_tokenizer = KoreanTokenizer(verbose=VERBOSE,
                                             decompound_mode=DECOMPOUND_MODE,
                                             infl_decompound_mode=INFL_DECOMPOUND_MODE,
                                             output_unknown_unigrams=OUTPUT_UNKNOWN_UNIGRAMS,
                                             discard_punctuation=DISCARD_PUNCTUATION,
                                             path_userdict = None,
                                             userdict_patterns = res['entries'])

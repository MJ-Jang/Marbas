import re
from .dict.errorfix_dictrionary import ErrorFixDictionary


class KoreanErrorCorrector(object):
    """
    correct wronly tagged POS
    """

    def __init__(self,
                 path_userdict = None,
				 userdict_patterns = None):

        if not path_userdict and not userdict_patterns:
            raise ValueError("At least one of path_userdict or userdict_patterns should be given")

        dictionary, self.entries = ErrorFixDictionary.open(USER_PATH=path_userdict,
                                                           PATTERN_LIST=userdict_patterns)
        self.correct_dict = dictionary.correct_dict
        keys = sorted(list(self.correct_dict.keys()), key=lambda x: len(x), reverse=True)
        self.patterns = '|'.join(keys)

    def correct(self, tkn_attrs):
        tokens = tkn_attrs.termAtt
        tags = tkn_attrs.posTagAtt
        merge_text = ' '.join([t + '_' + p for t, p in zip(tokens, tags)])

        match = re.findall(pattern=self.patterns, string=merge_text)
        if match:
            for m in match:
                merge_text = merge_text.replace(m, self.correct_dict.get(m))

            splits = merge_text.split(' ')
            tokens, tags = [], []
            for s in splits:
                t, p = s.split('_')
                tokens.append(t)
                tags.append(p)

        tkn_attrs.termAtt = tokens
        tkn_attrs.posTagAtt = tags
        return tkn_attrs

from .dictionary import Dictionary
from .character_definition import CharacterDefinition
from .trie import Trie
from ..pos import POS

from typing import Text, List

import pandas as pd


class UserDictionary(Dictionary):
    """Build User Dictionary
    """

    WORD_COST = -100000
    LEFT_ID = 1781  # NNG left
    RIGHT_ID = 3533  # NNG right
    RIGHT_ID_T = 3535  # NNG right with hangul and a coda on the last char
    RIGHT_ID_F = 3534  # NNG right with hangul and no coda on the last char
    USER_POS = 'NNG'

    @staticmethod
    def open(USER_PATH: Text = None, PATTERN_LIST: List = None):
        """
        :param USER_PATH: user dictionary path
        :param PATTERN_LIST: List of POS patterns
        """
        if not USER_PATH and not PATTERN_LIST:
            raise ValueError("At least one of USER_PATH or PATTERN_LIST should be given")

        entries = []

        if USER_PATH:
            if USER_PATH.endswith('.txt'):
                with open(USER_PATH, 'r', encoding='UTF-8') as rf:
                    user_dict = rf.readlines()
                user_dict = [s.strip() for s in user_dict]
                user_dict = list(set(user_dict))

            elif USER_PATH.endswith('.tsv'):
                user_dict = pd.read_csv(USER_PATH, sep='\t', encoding='utf-8')
                user_dict = user_dict[user_dict.keys()[0]].tolist()
                user_dict = [s.strip() for s in user_dict]
                user_dict = list(set(user_dict))

            elif USER_PATH.endswith('.csv'):
                user_dict = pd.read_csv(USER_PATH, sep=',', encoding='utf-8')
                user_dict = user_dict[user_dict.keys()[0]].tolist()
                user_dict = [s.strip() for s in user_dict]
                user_dict = list(set(user_dict))
            else:
                raise TypeError("Specified file format is not supported")

            for line in user_dict:
                line = line.strip()
                if len(line) == 0:
                    continue
                if line[:2] == '# ':
                    continue
                entries.append(line)

            # with open(USER_PATH, 'r', encoding='UTF8') as rf:
            #     for line in rf:
            #         line = line.strip()
            #         if len(line) == 0:
            #             continue
            #         if line[:2] == '# ':  # 주석 line
            #             continue
            #         entries.append(line)

        if PATTERN_LIST:
            entries += list(set(PATTERN_LIST))

        if len(entries) == 0:
            return None
        else:
            return UserDictionary(entries), entries

    def __init__(self, entries):
        charDef = CharacterDefinition()
        # 복합명사 우선 순위 & 중복 단어 제거를 위해 정렬
        # entries = sorted(entries)
        entries = sorted(entries, reverse=True)
        self.userTrie = Trie()
        lastToken = ""
        segmentations = []
        rightIds = []
        ord = 0

        for entry in entries:
            splits = entry.split("|")

            subwords = [s.split() for s in splits[1:]][0]
            subword_tags = [s.split('_')[1].strip() for s in subwords]
            splits = [splits[0].strip()] + [s.split('_')[0].strip() for s in subwords]

            token = splits[0]
            rightId = ""

            if token == lastToken:
                continue

            lastChar = list(entry)[0]
            if charDef.isHangul(lastChar):
                if charDef.hasCoda(lastChar):
                    rightId = self.RIGHT_ID_T
                # rightIds.append(RIGHT_ID_T)
                else:
                    rightId = self.RIGHT_ID_F
                # rightIds.append(RIGHT_ID_F)
            else:
                rightId = self.RIGHT_ID
            # rightIds.append(RIGHT_ID)

            # if len(splits) == 2:
            #     # segmentations.append(None)
            #     pass
            # else:
            #     length = []
            #     offset = 0
            #     for i in range(1, len(splits)):
            #         length.append(len(splits[i]))
            #         offset += len(splits[i])
            #     if offset > len(token):
            #         raise Exception(
            #             "Illegal user dictionary entry '{}' - the segmentation is bigger than the surface form ({})".format(
            #                 entry, token))

            # add mapping to Trie (similar to FST)
            morph_inf = dict()
            morph_inf['surface'] = token
            morph_inf['left_id'] = self.LEFT_ID
            morph_inf['right_id'] = rightId
            morph_inf['word_cost'] = int(self.WORD_COST)
            morph_inf['POS'] = self.USER_POS
            if len(splits) == 2:
                morph_inf['POS_type'] = POS.Type.MORPHEME
                # morph_inf['analysis'] = token
                morph_inf['morphemes'] = None
                morph_inf['POS'] = subword_tags[0]

                self.userTrie.insert(token, morph_inf)
            elif len(splits) > 2:
                morph_inf['POS_type'] = POS.Type.COMPOUND
                # morph_inf['analysis'] = ' '.join(splits[1:]) # decompounded form
                morphemes_list = []
                for i, subword in enumerate(splits[1:]):
                    morphemes_list.append(Dictionary.Morpheme(posTag=subword_tags[i], surfaceForm=subword))
                morph_inf['morphemes'] = morphemes_list
                self.userTrie.insert(token, morph_inf)

            lastToken = token
        # ord += 1

    # self.userTrie = userTrie
    # self.segmentations = segmentations
    # self.rightIds = rightIds

"""
	#@override
	def getMorphemes(self, wordId, surfaceForm, off, len):
		## Get the morphemes of specified word (e.g. 가깝으나: 가깝 + 으나). 
		# return Morpheme[]
		raise NotImplementedError("The method not implemented")

	#@override
	def getLeftId(self, wordId):
		return LEFT_ID

	#@override
	def getRighId(self, wordId):
		return self.rightIds[wordId]

	#@override
	def getWordCost(self, wordId):
		return WORD_COST

	#@override
	def getPOSType(self, wordId):
		if self.segmentations[wordId] == None:
			return POS.Type.MORPHEME
		else:
			return POS.Type.COMPOUND

	#@override
	def getLeftPOS(self, wordId):
		return POS.Tag.NNG

	#@override
	def getRightPOS(self, wordId):
		return POS.Tag.NNG
"""





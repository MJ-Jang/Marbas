from .dictionary import Dictionary

from typing import Text, List


class ErrorFixDictionary(Dictionary):
    """Build Error Fix Dictionary
    """
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
            with open(USER_PATH, 'r', encoding='UTF8') as rf:
                for line in rf:
                    line = line.strip()
                    if len(line) == 0:
                        continue
                    if line[:2] == '# ':  # 주석 line
                        continue
                    entries.append(line)

        if PATTERN_LIST:
            entries += PATTERN_LIST

        if len(entries) == 0:
            return None
        else:
            return ErrorFixDictionary(entries), entries

    def __init__(self, entries):
        self.correct_dict = {}

        for s in entries:
            splits = s.split('|')
            self.correct_dict.update({splits[1].strip(): splits[2].strip()})

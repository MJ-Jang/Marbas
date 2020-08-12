import os
import sys
import shlex
import pickle
import gzip
import argparse

from datetime import datetime
from tqdm import tqdm
from marbas.pos import POS

parser = argparse.ArgumentParser()

parser.add_argument('--custom_path',
                    type=str,
                    default='Custom_dict.csv',
                    )

args = parser.parse_args()

cur_path = __file__
# resource_path = '/'.join(cur_path.split('/')[:-1]) + '/marbas/resources'
resource_path = 'marbas/resources'

mecab_ko_dic_ver = 'mecab-ko-dic-2.1.1-20180720'


# pickle load & save
def write_pkl(data, name):
    """ name: '~.pkl' """
    fp = open(name, 'wb')
    pickle.dump(data, fp)
    fp.close()


def read_pkl(name):
    """ name: '~.pkl' """
    fp = open(name, 'rb')
    return pickle.load(fp)


# ---
start_main = datetime.now()

# load basic mecab data
total_entries = []
dirName = resource_path + '/' + mecab_ko_dic_ver
fileList = os.listdir(dirName)
for fname in fileList:
    if fname.split('.')[-1] == 'csv':
        PATH_EACH = dirName + '/' + fname
        total_entries += open(PATH_EACH, 'r', encoding='UTF8').readlines()

# load custom dict
PATH_CUSTOM = args.custom_path
for line in open(PATH_CUSTOM, 'r', encoding='UTF8').readlines():
    if not line.startswith('#'):
        total_entries += [line]

print("Compressing Data to Mecab Format...")

refined_data = []
for entry in tqdm(total_entries):
    entry = entry.strip()

    # Use shlex.
    # to deal with the case: ",",1792,3558,788,SC,*,*,*,*,*,*,*
    shlex_splitter = shlex.shlex(entry, posix=True)
    shlex_splitter.whitespace = ','
    shlex_splitter.whitespace_split = True
    splits = list(shlex_splitter)
    # splits = entry.split(',')

    token = splits[0]

    morph_inf = dict()
    morph_inf['surface'] = splits[0]
    morph_inf['left_id'] = splits[1]
    morph_inf['right_id'] = splits[2]
    morph_inf['word_cost'] = int(splits[3])
    morph_inf['POS'] = splits[4]

    if splits[8] == '*':  # 단일어
        morph_inf['POS_type'] = POS.Type.MORPHEME
        morph_inf['morphemes'] = None

    else:  # 복합어

        mecab_pos_type_naming = splits[8].upper()
        if mecab_pos_type_naming == 'COMPOUND':
            morph_inf['POS_type'] = POS.Type.COMPOUND
        elif mecab_pos_type_naming == 'INFLECT':
            morph_inf['POS_type'] = POS.Type.INFLECT
        elif mecab_pos_type_naming == 'PREANALYSIS':
            morph_inf['POS_type'] = POS.Type.PREANALYSIS
        else:
            morph_inf['POS_type'] = mecab_pos_type_naming

        if len(splits[11].split('+')) == 1:  # Compound인데 1개면 잘못 명시한 케이스 (확인 필요. 오류?)
            # 예외처리 (ex. 개태,1783,3538,3534,NNP,*,F,개태,Compound,*,*,*)
            morph_inf['POS_type'] = POS.Type.MORPHEME  # Compound인데 토큰이 1개니까 그냥 MORPHEME으로 처리
            morph_inf['morphemes'] = None
        else:  # 2개 이상: 정상적인 COMPOUND
            morphemes_list = []
            for substr in splits[11].split('+'):
                # substr = 목/NNG/*+매기/NNG/*+송아지/NNG/*
                subword = substr.split('/')[0]
                subpos = substr.split('/')[1]
                # morphemes_list.append(Dictionary.Morpheme(posTag=subpos, surfaceForm=subword))
                morphemes_list.append((subpos, subword))
            morph_inf['morphemes'] = morphemes_list

    # morph_inf['analysis'] = splits[11]
    # 짐수레꾼,1781,3535,2835,NNG,*,T,짐수레꾼,Compound,*,*,짐/NNG/*+수레/NNG/*+꾼/NNG/*
    # sysTrie.insert(token, morph_inf)
    refined_data.append([token, morph_inf])

# save and compress.
# with gzip.open('mecab_csv.pkl', 'wb') as wf:
#    pickle.dump(sysTrie, wf)

output_f_nm = 'mecab_custom_csv.pkl'
with gzip.open(output_f_nm, 'wb') as wf:
    pickle.dump(refined_data, wf)

end_main = datetime.now()
print('> {} is successfully generated! - {}'.format(output_f_nm, end_main - start_main))

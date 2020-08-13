# get custom dictionary from blob
wget https://mlpipelinhub.blob.core.windows.net/models/POS_tagger/SystemDic/latest/CustomDic.csv

python custom_systemdict.py --custom_path="CustomDic.csv"
mv mecab_csv.pkl marbas/resources/pkl_mecab_csv
rm -rf CustomDic.csv
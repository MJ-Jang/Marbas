# get custom dictionary from blob
wget https://mlpipelinhub.blob.core.windows.net/models/POS_tagger/SystemDic/latest/CustomDic.csv

python custom_systemdict.py --custom_path="CustomDic.csv"
mv mecab_custom_csv.pkl marbas/resources
rm -rf CustomDic.csv
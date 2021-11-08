import os
import pandas as pd
from genrss import GenRSS

def f_merge_df_to_csv(df, csv_file):
    def cal_hash(x):
            return hash(x)
        
    if os.path.exists(csv_file) == False:
        df.to_csv(csv_file, index=False)
    else:
        df_existed = pd.read_csv(csv_file)        
        df = pd.concat([df, df_existed])
        df['hash'] = df['title'].astype(str) + df['url'].astype(str)
        df['hash'] = df['hash'].apply(cal_hash).astype(str)
        df.drop_duplicates(subset=['hash'], inplace=True, keep='last')
        df.drop(columns=['hash'], inplace=True)
        df.to_csv(csv_file, index=False)
    print('The CSV file has been saved to "', csv_file,'".', sep='')   

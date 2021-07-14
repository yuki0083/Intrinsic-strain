import csv
import pandas as pd
import numpy as np

#csvを読み込む関数
def make_data_from_csv(csv_file_path):

  
    #一行目をheaderとして、csv読み込み
    df = pd.read_csv(csv_file_path, header=1, encoding='shift-jis')   
    df = df.drop(df.columns[0],axis='columns')#0列目を削除

    return df

#dfの数値を丸める関数
def round_df_xyz(df_xyz, num):
    #df_xyz = df_xyz.round({'中心(X)':num, '中心(Y)':num, '中心(Z)':num})
    df_xyz = df_xyz.round({'中心(X)':num})
    return df_xyz
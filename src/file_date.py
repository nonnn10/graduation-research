import glob             #ディレクトリのファイル一覧を取得するためのモジュール
import pandas as pd
import datetime as dt
"""
csvファイルを任意の期間dataframeにまとめるためのスクリプト
"""

def main(route = "hateruma_route" ,dep_port = "isigaki", dates = "2017"):
    """
    ../data/route/*_route/*_dep/*.csvを全てまとめて
    ひとつのdataframe型にする関数

    parameter
    ---------
    route : str
        ../data/route/下の航路ディレクトリ名
        航路ディレクトリは全部で7個
    dep_port : str
        ../data/route/変数route/下の出発港ディレクトリ名
        出発港は全部で14個
    dates : str
        ../data/route/変数route/変数dep_port/下の任意の日付のcsvファイル

    return
    ------
    df : dataframe
        任意の航路、出発港、日付(範囲)を全てまとめたデータフレームを返す


    """
    route = "hateruma_route"        #航路のディレクトリ名
    dep_port = "isigaki"        #出発港のディレクトリ名
    dates = "2017-01-*"             #まとめたいcsvファイルの日付,この場合だと2017年1月の日付csvを全て統一する事になる
    dflist = file_index(route,dep_port,dates)
    print(dflist)
    df = df_array(dflist,0)
    df = df_all(dflist,df)
    print(df)
    print(df.dtypes)
    df.to_csv('../data/route/'+route+'/'+dep_port+'_dep/'+dates+'.csv')   #名前の変更をしてもいいかも

    return df

def file_index(route,dep_port,dates):
    """
    csvファイル名の配列を返す

    parameter
    ---------
    route : str
        ../data/route/下の航路ディレクトリ名
        航路ディレクトリは全部で7個
    dep_port : str
        ../data/route/変数route/下の出発港ディレクトリ名
        出発港は全部で14個
    dates : str
        ../data/route/変数route/変数dep_port/下の任意の日付のcsvファイル

    return
    ------
    dflist : list
        配列の中にdataframeが入っている
    """
    path = '../data/route/'+route+'/'+dep_port+'_dep/'+dates    #まとめたいcsvファイルがあるパス
    files_pass = []

    files_pass = glob.glob(path)
    files = []
    dflist = []
    for i,file_name in enumerate(files_pass):               #enumerateでiにはcoute数、file_nameにはfileのパス
        files.append(file_name.replace("../data/route/"+route+"/"+dep_port+"_dep/",""))    #file名
        #dflist配列にdataframe形式で格納
        dflist.append(pd.read_csv("../data/route/"+route+"/"+dep_port+"_dep/"+files[i],encoding='cp932',sep=',',names=("Time","label","Date")))

    files.sort()
    print(files)
    print(len(dflist))

    return dflist

def df_array(dflist, df_num):
    """
    ひとつのdataframeを整形する

    parameter
    ---------
    dflist : list
        配列の中にdataframeが入っている
    df_num : int
        dflistの何番目の配列をなのかを指定するナンバー

    return
    ------
    df : dataframe
        dflistの配列のひとつを整形して、戻り値とする
    """
    print(dflist)
    df = dflist[df_num]          #dataframe結合の元になるdf
    df["Time"] = pd.to_datetime(df['Date'].astype(str)+' '+ df['Time'])     #列Timeに日付と時間を結合させdatetime型に変換
    df = df.drop("Date", axis=1).rename(columns={'Time': 'Date'})       #列Dateを削除、列Timeの名前をDateに変更

    return df

def df_all(dflist,df):
    """
    df_array関数をループさせdflist配列の全てをまとめ整形する

    parameter
    ー-------
    dflist : list
        配列の中にdataframeが入っている
    df : dataframe
        まとめるための元になるdf
    
    return
    ------
    df : dataframe
        全てをまとめたdf

    """
    for i in range(1,len(dflist)):      #1~30までループ
        df2 = df_array(dflist,df_num=i)
        df = pd.concat([df,df2],axis=0)     #行方向に後ろからへ結合
    #全てをまとめたdfを日付順にソート、index番号をリセット、元のindex列を削除
    df = df.sort_values('Date').reset_index().drop("index",axis=1)

    return df

def dfarray(route = "hateruma_route" ,dep_port = "isigaki", dates = "2017"):
    """
    df_comb.pyで使用するための関数
    日付をまとめたcsvfileを列[Date,label]に整形する
    """
    df = pd.read_csv("../data/route/"+route+"/"+dep_port+"_dep/"+dates+".csv",encoding='utf-8',sep=',',names=("Time","label","Date"))
    df["Time"] = df["Time"].str.replace(r'(\d{1,2}):(\d{1,2})\n(.*)', r'\1:\2',regex=True)
    print(df)
    df["Time"] = pd.to_datetime(df['Date'].astype(str)+' '+ df['Time'])     #列Timeに日付と時間を結合させdatetime型に変換
    df = df.drop("Date", axis=1).rename(columns={'Time': 'Date'})       #列Dateを削除、列Timeの名前をDateに変更
    df.to_csv('../data/route/'+route+'/'+dep_port+'_dep/'+dates+'.csv')   #名前の変更をしてもいいかも

    return df

if __name__ == '__main__':
    main()

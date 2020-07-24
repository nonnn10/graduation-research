"""
欠損値処理 : https://qiita.com/0NE_shoT_/items/8db6d909e8b48adcb203
dateframeの正規表現 : https://qiita.com/hiroyuki_mrp/items/29e87bf5fe46de62983c
                    https://www.sejuku.net/blog/23421
colum名変更 : https://shirabeta.net/How-to-rename-columns-of-pandas-DataFrame.html#.XxSTLS2KWAM

次やること
最終出力をどうするか？
"""
import csv
import pandas as pd
import datetime as dt
import dateutil         #日付の計算に必要
from dateutil.relativedelta import relativedelta
import glob             #ディレクトリのファイル一覧を取得するためのモジュール
import re
import wind_speed

def main(dep_port = "isigaki", route = "hateruma_route", dates = "2017-01-*" ):
    #df = pd.read_table("../data/wave_height/nowphas_2017_2018/h705e.017.txt",encoding='cp932',sep='   ',)
    my_cols = [str(i) for i in range(9)] # create some row names
    df = pd.read_csv("../data/wave_height/nowphas_2017_2018/h705e.017.txt",
                                   sep="   ",
                                   names=my_cols, 
                                   header=None,
                                   skiprows=1,
                                   engine="python")
    #print(df.isnull().sum())    #NaN,Noneの数がわかる
    #print(df.info())            #欠損していない行数がわかる
    df = df.drop(["8"],axis=1)  #全ての要素が欠損している行を削除
    #df_date = df["0"]           #日付データのみを抽出
    df = date_regex_trans(df)   #日付データをdatatime型に変換できるようにする処理
    df = df.dropna().reset_index()      #NaNのある行を削除してindex番号をリセット
    #df['0'] = pd.to_datetime(df['0'],format='%Y-%m-%d %H:%M')     #datatime型に変換
    df['0'] = pd.to_datetime(df['0'])     #datatime型に変換
    df = df.drop(["index"],axis=1)  #全ての要素が欠損している行を削除
    #列名の辞書
    column_name_dic = {
        "0": "Date",
        "1": "flag",
        "2": "WaveNum-AveWaveHight",            #波数,平均波の波高
        "3": "AveWaveCyc-MeWaveHight",          #平均波の周期,有義波の波高
        "4": "MeWaveCyc-0p1WaveHight",          #有義波の周期,1/10波の波高
        "5": "0p1WaveCyc-HighestWaveHight",     #1/10波の周期,最高波の波高
        "6": "HighestWaveCyc",                  #最高波の周期
        "7": "dire_wave"                        #波の向き
    }
    df = df.rename(columns=column_name_dic, inplace=False)      #inplaceをTrueにするとdataframeが直接書き換えられる
    for i in range(2,6):                                        #1列に2つのデータがある時
        df = column_division(df,column_name_dic[str(i)])
    #print(df.info())
    #正しいならびに列を入れ替え
    #列[年月日時分,フラグ,波数,
    # 平均波の波高,平均波の周期,
    # 有義波の波高,有義波の周期,
    # 1/10波の波高,1/10波の周期,
    # 最高波の波高,最高波の周期,
    # 波の向き]
    df = df[['Date', 'flag', 'WaveNum',
       'AveWaveHight', 'AveWaveCyc',
        'MeWaveHight', 'MeWaveCyc',             #Meaningful 意味のある
       '0p1WaveHight', '0p1WaveCyc', 
       'HighestWaveHight', 'HighestWaveCyc',    
        'dire_wave']]                           #direction 方向,方角
    #print(df)

    #dflavelの読み込み(labelデータのあるcsv)
    dflabel = pd.read_csv('../data/route/'+route+'/'+dep_port+'_dep/'+dates+'.csv',encoding='cp932',sep=',',index_col=0)
    #dflabelに列MeWaveHight,MeWaveCyc,dire_waveを追加して全ての要素は0で追加
    dflabel= dflabel.assign(MeWaveHight = 0)
    dflabel= dflabel.assign(MeWaveCyc = 0)
    dflabel= dflabel.assign(dire_wave = 0)
    #print(dflabel)
    #dfのwaveデータをdflavelに追加
    dflabel = df_wave_hight_append(df,dflabel)
    #print(dflabel)

    return dflabel

def df_wave_hight_append(df,dflabel):
    """
    欠航情報のあるdateframeに有義波の波高と周期、波の向きをMeWaveHight,MeWaveCyc,dire_wave列として追加

    parameters
    ----------
    df : dateframe
        波のデータのあるdateframe
    dflabel : dateframe
        欠航情報のあるdateframe
    
    return
    ------
    dflabel : dateframe
        欠航情報と波データの結合をしたdateframe
    """
    me_wave_hight = []
    me_wave_cyc = []
    dire_wave = []
    for i, row in enumerate(dflabel.itertuples(name=None)):   #dateframeの行ごとのループ
        #print(row[1])                           #dflabelの2列目がstr型の日付データ
        date_time = wind_speed.datetime_list_trans(row[1])    #str型の日付データをintの配列に変換
        #print(date_time)
        # if date_time[4] <= 29:      #分が29分以下なら
        #     date_time[3] -= 1       #時間をマイナス1時間する
        #     date_time[4] = 59       #分を59分にする(7:20 -> 6:59に変換)   
        
        year,month,date,hour,minute = wind_speed.datelist_in_vari(date_time)            #前の日付を変数に格納
        df_wave_data = df[(df['Date'] >= dt.datetime(year,month,date,hour,minute))]     #日付に一番近いデータを抽出
        # if i == 0:
        #     print(str(year)+"/"+str(month)+"/"+str(date)+" "+str(hour)+":"+str(minute))
        #     print(df_wave_data.head(1))  
        me_wave_hight.append(df_wave_data.head(1).iloc[0,5])    #有義波の波高を配列に追加
        me_wave_cyc.append(df_wave_data.head(1).iloc[0,6])      #有義波の周期を配列に追加
        dire_wave.append(df_wave_data.head(1).iloc[0,11])       #波の向きを配列に追加
    dflabel["MeWaveHight"] = me_wave_hight      #dflabelのMewaveHight列に値を追加
    dflabel["MeWaveCyc"] = me_wave_cyc
    dflabel["dire_wave"] = dire_wave

    return dflabel

def column_division(df,column_name):
    """
    列にデータが2つあるため分割して別の列にする

    parameters
    ----------
    df : dateframe
        元のデータフレーム
    column_name : str
        列の名前
    
    return
    ------
    df2 : dataframe
        正しい列名のデータフレーム
    """
    df_div = df[column_name].str.split('  ', expand=True)   #データを空白で分割
    column_div = column_name.split('-')                     #列名をハイフンで分割
    df_div.columns = [column_div[0],column_div[1]]          #分割した列名を分割したデータに適用
    df2 = pd.concat([df, df_div], axis=1).drop(column_name,axis=1)  #元のdfに結合
    #print(df2)

    return df2



def date_regex_trans(df_date):
    """
    日付データ(2017 1 1 1 0)を(2017-1-1 1: 0)に変換
    日付データをdatatime型に変換できるようにする処理

    parameters
    ----------
    df_date : dataframe
        日付データのあるデータフレーム
    
    return
    ------
    df_date : dataframe
        日付型に直せるようにしたデータフレーム
    """
    #日付部分の置換処理
    #2017 1 1 1 0, 2017 1 1 020 -> 2017-1-1 1 0, 2017-1-1 020
    df_date = df_date.replace(r'^(\d{4}) (\d) (\d)', r'\1-\2-\3',regex=True)    #regexは正規表現をす使うか使わないか
    #201710 1 420, 201710 12220 -> 2017-10-1 420, 2017-10-12220
    df_date = df_date.replace(r'^(\d{4})(\d{2}) (\d)', r'\1-\2-\3', regex=True)   
    #2017 110 0 0 -> 2017-1-10
    df_date = df_date.replace(r'^(\d{4}) (\d)(\d{2})', r'\1-\2-\3', regex=True)   
    #201710 1 420, 201710 12220 -> 2017-10-1 420, 2017-10-12220    
    df_date = df_date.replace(r'^(\d{4})(\d{2})(\d{2})', r'\1-\2-\3', regex=True)

    #時間部分の置換処理
    #2017-1-1 1 0 -> 2017-1-1 1: 0 
    #2017-1-1 020 -> 2017-1-1 1:20
    #2017-1-11020 -> 2017-1-1 10:20
    #2017-1-110 0 -> 2017-1-1 10:0
    #2017-10-1 420 -> 2017-10-1 4:20
    #2017-10-12 5 0 -> 2017-10-12  5: 0
    #2017-10-1220 0 -> 2017-10-12 20: 0 
    #2017-10-12 120 -> 2017-10-12  1:20 
    #2017-10-121020 -> 2017-10-12 10:20
    df_date = df_date.replace(r'^(\d{4}-\d{1,2}-\d{1,2})( \d|\d{2})( \d|\d{2})', r'\1 \2:\3',regex=True)
    df_date = df_date.replace(r' (\d$)', r'\1',regex=True)
    df_date = df_date.replace(r' (\d):(\d{1,2})$', r'\1:\2',regex=True)

    
    return df_date
   
    
if __name__ == '__main__':
    main()
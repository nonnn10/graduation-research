"""
wind_speed.pyとwave_hight.py戻り値であるdataframeを結合し、新しいdataframeとして出力
"""
import csv
import pandas as pd
import datetime as dt
import dateutil         #日付の計算に必要
from dateutil.relativedelta import relativedelta
import glob             #ディレクトリのファイル一覧を取得するためのモジュール
import re
import wind_speed
import wave_hight
import file_date        #csvfileのデータを整形するため

def main(dep_port = "isigaki", route = "hateruma_route", dates = "2017"):
    """
    wind_speed.pyとwave_hight.py戻り値であるdataframeを結合し、新しいdataframeとして出力
    csvとして任意のディレクトリに保存

    parameters
    ----------
    dep_port : str
        出発港の文字列
    route : str
        航路の文字列
    dates : str
        読み込むcsvのファイル名(日付になっているはず)
    
    return
    ------
    df : dataframe
        波,風情報をラベルデータに追加したdataframe
    """
    # df = file_date.dfarray(dep_port = dep_port, route = route, dates = dates)
    df_wind = wind_speed.main(dep_port = dep_port, route = route, dates = dates)
    df_wave = wave_hight.main(dep_port = dep_port, route = route, dates = dates)
    #print(df_wind)
    #print(df_wave)
    df = pd.merge(df_wind, df_wave)
    #print(df)
    #dfをcsvとして出力
    df.to_csv("../data/data_2017/"+route+"_"+dep_port+"_"+dates+".csv")
    return df

if __name__ == '__main__':
    #航路の辞書でvalueが出発港の配列
    route = {
        "taketomi_route": ["isigaki","taketomi"],
        "hateruma_route": ["isigaki","hateruma"],
        "kurosima_route": ["isigaki","kurosima"],
        "iriomote_ohara_route": ["isigaki","ohara"],
        "iriomote_uehara_route": ["isigaki","uehara"],
        "hatoma_route": ["isigaki","hatoma"],
        "kohama_route": ["isigaki","kohama"]
        }
    #main関数が航路数×出発港の数だけ実行しcsvfile出力
    for key, value in route.items():
        for i in range(len(value)):
            print(value[i]+"--"+key+"2017")
            #file_date.dfarrayでまとめたcsvに波と風データを追加する
            main(dep_port = value[i], route = key, dates = "2017")  
            try:
                df = file_date.dfarray(dep_port = value[i], route = key, dates = "2017")
                
            except TypeError:
                continue
            except AttributeError:
                continue
            
            #main(dep_port = value[i], route = key, dates = "2017")
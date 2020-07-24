"""
datetimeに関するサイト : https://qiita.com/xza/items/9618e25a8cb08c44cdb0#python-標準時刻関連ライブラリ
datetimeの比較 : https://qiita.com/mSpring/items/6ec1ab28dcb261db2c73


やり残してるところ
日付比較のところ何々以上入るけど何々未満はいらないのでは？
最後の処理csvに書き出すか？それとも実行ファイルを別で作成してreturnでdataframeを返すか？
現状、dataframeで出力
"""
import csv
import pandas as pd
import datetime as dt
import dateutil         #日付の計算に必要
from dateutil.relativedelta import relativedelta
import re

def main(dep_port = "isigaki", route = "hateruma_route", dates = "2017"):

    #dfは風速データの入っているdateframe,   from_windで対応したwindデータを選択
    df = pd.read_csv("../data/wind_speed/2017_"+from_wind(dep_port)+"_data.csv",encoding='cp932',sep=',')#,usecols=[0])
    #print(df)
    #正規表現によりYYYY/MM/DDからYYYY-MM-DDに変更
    df = df.replace('(.*)/(.*)/(.*)', r'\1-\2-\3', regex=True)
    df = df.rename(columns=str)
    #dataframeの列名を変更
    df = df.rename(index=str, columns={'年月日時':'Date', '風速(m/s)':'wind_speed','風向':'wind_direction'})
    df['Date'] = pd.to_datetime(df['Date'])     #datatime型に変換
    #ラベルの入っているdf
    dflabel = pd.read_csv('../data/route/'+route+'/'+dep_port+'_dep/'+dates+'.csv',encoding='cp932',sep=',',index_col=0)
    #dflabelに列wind_speedを追加して全ての要素は0で追加
    dflabel= dflabel.assign(wind_speed = 0)
    #print(dflabel)
    #dflabelにwind_speedの値を追加する
    dflabel = df_wind_speed_append(df,dflabel)
    #print(dflabel)
    return dflabel

def from_wind(dep_port):
    """
    風は石垣,西表,大原のデータがあるためそれぞれ対応したデータを選択しなければいけない
    そのための辞書
    """
    wind_dic = {
        "isigaki" : "isigaki",
        "taketomi" : "isigaki",
        "kurosima" : "ohara",
        "kohama" : "iriomote",
        "uehara" : "iriomote",
        "hatoma" : "iriomote",
        "ohara" : "ohara",
        "hateruma" : "ohara"
        }

    return wind_dic[dep_port]

def datelist_in_vari(date_list, str_on = False):#日付の入ったlistを変数に入れ直す,variableは変数
    """
    日付の入った配列を変数に入れ直す、わかりやすくするため

    parameters
    ----------
    date_list : list
        年,月,日,時間,分で区切られた配列
    str_on : bool
        この変数をTrueにすると戻り値をstr型に変換する
    return
    ------
    year : int
    month : int
    date : int
    hour : int
    minute : int
    """
    if str_on == True:
        date_list = str(date_list)
    year = date_list[0]     #西暦,年
    month = date_list[1]    #月
    date = date_list[2]     #日付
    hour = date_list[3]     #時間
    minute = date_list[4]   #分

    return year, month, date, hour, minute

def datetime_list_trans(datetime):
    """
    datetime型をlist型に変換

    parameters
    ----------
    datetime : datetime
        日付
    
    return
    ------
    date_time : list[int]
        list型で数値がint型の日付が出力
    """
    print(datetime)
    date_time = re.split('[- :]', datetime)   #正規表現で文字列をsplit [2017, 1, 29, 11, 50, 0]
    #map()
    date_time = [int(s) for s in date_time] #配列の要素strをintに変換
    return date_time

def df_wind_speed_append(df,dflabel):
    wind_speed = []
    for i, row in enumerate(dflabel.itertuples(name=None)):   #dateframeの行ごとのループ
        print(row[1])                           #dflabelの2列目がstr型の日付データ
        date_time = datetime_list_trans(row[1])    #str型の日付データをintの配列に変換
        #print(date_time)

        # if date_time[4] <= 29:      #分が29分以下なら
        #     date_time[3] -= 1       #時間をマイナス1時間する
        #     date_time[4] = 59       #分を59分にする(7:20 -> 6:59に変換)   
        # if i != 0:
        year,month,date,hour,minute = datelist_in_vari(date_time)               #前の日付を変数に格納
            # year_la,month_la,date_la,hour_la,minute_la = datelist_in_vari(date_time)    #後の日付を変数に格納
            #print(str(date_time_pri)+"new------old"+str(date_time))
            #print("-------------")
            #print(df[(df['Date'] >= dt.datetime(year,month,date,hour,minute)) & (df['Date'] < dt.datetime( year_la,month_la,date_la,hour_la,minute_la))])
            # if hour == hour_la and minute == minute_la:         #時間と分が等しい時の処理
        df_wind_data = df[(df['Date'] >= dt.datetime(year,month,date,hour,minute))]
            # else:
            #    df_wind_data = df[(df['Date'] >= dt.datetime(year,month,date,hour,minute)) & (df['Date'] < dt.datetime( year_la,month_la,date_la,hour_la,minute_la))]
            #print(df_wind_data.head(1)["wind_speed"])
        wind_speed.append(df_wind_data.head(1).iloc[0,1])           #比較して一番時間の近い風速データを配列に追加,iloc[0,1]->1行2列(その場所が風速データ)
        # date_time_pri = date_time   #前回ループのdate 

    #一番最後の行はfor文では処理されないのでここで処理
    #print(wind_speed)
    dflabel["wind_speed"] = wind_speed
    #print(dflabel)

    return dflabel

if __name__ == '__main__':
    main()

#http://taustation.com/python3-for-loop-first-and-last-execution/
# def generator(df):
    
#     # 先頭に表示させる文字
#     prefix = "<"
 
#     # 与えられたコレクションをイテレーターとする
#     it = iter(lst)
 
#     # まず最初の要素を取得しておく
#     next_element = next(it)
 
#     # 最初の要素は既に取得されているので、current_elementは2つ目の要素から
#     # 取得される
#     for current_element in it:
#         # ジェネレーターはprefix、本体要素、suffixを返す
#         yield prefix, next_element, ", "
#         # 以下、取得した要素をnext_elementに順次移していく
#         next_element = current_element
#         # 2つ目の要素以降はprefixなし
#         prefix = ""
#     # 最後の要素のみsuffixを">"にする
#     yield prefix, next_element, ">"

# for prefix, e, suffix in generator(lst):
#     print("{}{}{}".format(prefix, e, suffix), end="")
# print()


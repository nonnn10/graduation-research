"""
コマンドライン引数 : https://qiita.com/taashi/items/07bf75201a074e208ae5
webのリロード : https://www.seleniumqref.com/api/python/window_set/Python_refresh.html
htmlの属性のスクレイピング : https://www.seleniumqref.com/api/python/element_infoget/Python_get_attribute.html

コマンドラインから時間の引数を受け取り,波と風の数値をとる
ディレクトリは「../data/now_value_scrape」の中のwave_height,wind_speedのそれぞれの時間9:00,11:00...17:00それぞれのディレクトリに
value_top_wind_max_speed_dir.csv　というファイル名などで保存
"""
from time import sleep
from selenium import webdriver
import csv
import time
from selenium.webdriver.chrome.options import Options
import exe
import os
from selenium.webdriver.common.action_chains import ActionChains    #wendyの時間帯のバーをクリックするの必要
#wait処理に必要
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#日付取得
import datetime as dt
#日付の年,月,週の計算を可能にする
from dateutil.relativedelta import relativedelta
#正規表現置換
import re
#関数を使うため,create_date_dir()...
import windy_image_scrap as wis
#コマンドライン引数
import sys
#2次元配列を1次元にするために
import itertools

def main(driver,atribute,args,abspath):
    #コマンドラインから取得した引数をscrap_timeに代入
    scrap_time = args[1]
    #時間によって配列の取得する部分が異なるため
    list_num = time_select(scrap_time)

    #画像保存先のディレクトリパス
    dir_pass = abspath+"/graduation-research/data/now_value_scrape"
    #atribute = "wind_speed"
    print(atribute)
    now_date = wis.now_date_cre()       #プログラム実行時の日付
    
    #画像ファイル名の作成に必要
    month = re.sub(r'(\d*)-(\d*)-(\d*)', r'\2',now_date)
    yaer = re.sub(r'(\d*)-(\d*)-(\d*)', r'\1',now_date)

    time.sleep(3)
    # ウィンドウサイズを設定
    driver.set_window_size(2000, 850)

    buttun = driver.find_element_by_css_selector("#detail > div.table-wrapper.show.noselect.notap > div.data-table.noselect.flex-container > div.forecast-table.progress-bar > div.fg-red.size-xs.inlined.clickable")
    buttun.click()
    #ボタンを押すまで待機
    time.sleep(10)

    #要素が出現するまで待機
    wait = WebDriverWait(driver, 10)

    #値の種類
    val_dic = {
        "date" : "#detail-data-table > tbody > tr.td-days.height-days",
        "time_hour" : "#detail-data-table > tbody > tr.td-hour.height-hour.d-display-waves",
        "wind_speed": "#detail-data-table > tbody > tr.td-windCombined.height-windCombined.d-display-waves",
        "wave_height": "#detail-data-table > tbody > tr.td-waves.height-waves.d-display-waves",
        "swell": "#detail-data-table > tbody > tr.td-swell1.height-swell1.d-display-waves",
        "swell_spacing": "#detail-data-table > tbody > tr.td-swell1Period.height-swell1Period.d-display-waves" 
    }
    #for文に直す予定
    for i, (key,value) in enumerate(val_dic.items()):
        #dic_list = list(val_dic.items())

        #引数のatributeにval_dicのkey
        wis.create_date_dir(dir_pass,atribute=key,date=False)    #ディレクトリ作成

        val_row,dir_row = val_roup(wait,key,value)
        #csvfileに記述
        file_name = atribute+"_val_"+key     #fileの名前をwindy_val_date,windy_val_time_hourなどにする
        write_mode = "a"
        print(dir_pass+key)
        #引数のatributeにval_dicのkey

        if key == "wind_speed":
            #if文でwind_apeedなら
            wind_speed,max_wind_speed = wind_speed_dedi(val_row)
            wind_name = ["wind_speed","max_wind_speed"]             #fileの名前のための配列
            for i, wind_lists in enumerate([wind_speed,max_wind_speed]):
                file_name = atribute+"_val_"+wind_name[i]
                wis.create_date_dir(dir_pass,atribute=wind_name[i]+"/"+scrap_time,date=False)    #ディレクトリ作成
                csv_write(dir_pass+"/"+wind_name[i]+"/"+scrap_time+"/"+file_name+".csv",write_mode,wind_lists)
            #角度が取得した行に存在するなら
            if not dir_row:
                print(dir_row)
            else :
                file_name = atribute+"_val_"+wind_name[i]+"_dir"
                wis.create_date_dir(dir_pass,atribute=wind_name[i]+"/"+scrap_time,date=False)    #ディレクトリ作成
                csv_write(dir_pass+"/"+wind_name[i]+"/"+scrap_time+"/"+file_name+".csv",write_mode,dir_row)
                print(dir_row)
        else:
            wis.create_date_dir(dir_pass,atribute=key+"/"+scrap_time,date=False)                  #ディレクトリ作成
            val_row = list(itertools.chain.from_iterable(val_row))
            csv_write(dir_pass+"/"+key+"/"+scrap_time+"/"+file_name+".csv",write_mode,val_row)
            #角度が取得した行に存在するなら
            if not dir_row:
                print(bool(dir_row))
            else :
                file_name = atribute+"_val_"+key+"_dir"
                wis.create_date_dir(dir_pass,atribute=key+"/"+scrap_time,date=False)    #ディレクトリ作成
                csv_write(dir_pass+"/"+key+"/"+scrap_time+"/"+file_name+".csv",write_mode,dir_row)
                print(dir_row)
        print(val_row)

    #print(aa[1].find_element_by_tag_name("div").text)
    #for i in range(0,len(wave_val)):
        #wind_col = wind_table[i].find_element_by_tag_name('td')
        #print("せいこう"+"  "+str(i))
        #print(wave_val[i].text)
    # ドライバーを終了
    driver.close()
    driver.quit()

def val_roup(wait, value, css_selector):
    """
    trの中のtdを標準出力
    任意の地点の時間、風、波、うねりなどを指定して1行分出力
    paramerter
    ----------
    wait : WebDriverWait
        待機時間
    value : str
        なんのデータなのか(date,wind_speed,...)
    css_selector : str
        出力する行のCSSセレクタ
    
    return
    ------
    val_list : list
        角度以外の値の配列
    dir_list : list
        角度の配列
    """
    #cssセレクタでWebElementの取得,取得したい情報が読み込まれるまで待機して読み込む処理
    val_table = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
    #csvに書き込む配列
    val_list = []
    #角度のための配列
    dir_list = []
    if value == "date":
        val = val_table.find_elements_by_tag_name('td')
        
        print("td of num"+str(len(val)))
        for i in range(0,len(val)):
            #wind_col = wind_table[i].find_element_by_tag_name('td')
            #print("せいこう"+" 　"+str(i))
            #print(val[i].get_attribute("data-day"))
            der_val = newline_spl(val[i].get_attribute("data-day"))
            val_list.append(der_val)
    else:
        val = val_table.find_elements_by_tag_name('td')
        print("td of num"+str(len(val)))
        for i in range(0,len(val)):
            der_val = newline_spl(val[i].text)
            val_list.append(der_val)
        dir_list = direction_scr(val_table) #角度
            #print(dir_list)

    return val_list,dir_list

def direction_scr(val_table):
    """
    波の向き,風の向きなどを取得する関数
    parameters
    ----------
    val_table : WebElement
        任意の行のtdタグをfindしたwebslement

    return
    ------
    wind_dir_list : list[str]
        向きの値,0~360までの値をとる
    """
    dir_list = []
    wind_direction_row = val_table.find_elements_by_tag_name('div') #val_tableからdivタグを取得
    for i in range(0,len(wind_direction_row)):                      #divタグの数分のループ
        wind_dir_raw = wind_direction_row[i].get_attribute("style") #style属性をstrで取得
        wind_dir = re.sub(r'(.*)\((\d*)deg\).*', r'\2',wind_dir_raw)#正規表現で角度のみを抽出
        dir_list.append(wind_dir)       #角度をdir_list配列に追加

    return dir_list

def newline_spl(value):
    """
    改行文字\nで区切るための関数

    paramerter
    ----------
    value : str
        改行文字の入った文字列
    
    return
    ------
    value : list
        改行と#を削除した配列
    """
    value = value.splitlines()
    try:
        value.remove("#")
    except ValueError as e:
        #print(e)
        pass

    return value

def time_select(scrap_time):
    if scrap_time == "9:00":
        list_choice = 3
    elif scrap_time == "11:00":
        list_choice = 4
    elif scrap_time == "13:00":
        list_choice = 4
    elif scrap_time == "15:00":
        list_choice = 5
    else :                          #scrap_time == "17:00"
        list_choice = 2
    
    return list_choice

def wind_speed_dedi(val_row):
    """
    val_roup()で取得した風速の部分は値が風速と最大風速の二つあるため処理が必要

    parameters
    ----------
    val_row : list
        取得した値の入った配列,予定では64個ある

    return
    ------
    wind_speed : list
        風速の配列
    max_wind_speed : list
        最大風速の配列
    """
    wind_speed = []
    max_wind_speed = []
    for i in range(0,len(val_row)):
        wind_speed.append(val_row[i][0])
        max_wind_speed.append(val_row[i][1])
    print("wind_speed")
    print("td of num"+str(len(wind_speed)))
    print(wind_speed)
    print("max_wind_speed")
    print("td of num"+str(len(max_wind_speed)))
    print(max_wind_speed)

    return wind_speed, max_wind_speed

def csv_write(save_name,write_mode,write_value):
    """
    csvfileを記述するための関数

    parameters
    ----------
    save_name : str
        保存するディレクトリとファイル名
    write_mode : str
        上書き"a",書き出し"w"
    write_value : list
        書き出す値
    """
    with open(save_name, write_mode, encoding='UTF-8', errors='ignore') as f:
                writer = csv.writer(f, lineterminator='\n')            
                writer.writerow(write_value)

if __name__ == "__main__":
    abspath = wis.abspath_top()   #絶対path (/Users/name)
    print(abspath)
    atri = {"value_top":"https://www.windy.com/24.435/124.004/waves?waves,24.344,123.967,10",
            "value_bottom":"https://www.windy.com/24.282/124.041/waves?waves,24.162,124.040,10,i:pressure"}
    args = sys.argv
    for i, (key,value) in enumerate(atri.items()):
        for _ in range(0,3):#最大3回tryする
            try :
                driver = exe.start_up(headless_active=True, web_url=value,abspath=abspath)
                main(driver,key,args,abspath)
            except Exception as e :     #全てのエラーで
                time.sleep(20)
                driver = exe.start_up(headless_active=True, web_url=value,abspath=abspath)
                main(driver,key,args,abspath)
                error_dir = abspath+"/graduation-research/data"
                wis.create_date_dir(error_dir,"Error",date=False)
                save_name = error_dir+"/Error"+"/windy_"+key+".csv"
                write_value = [wis.now_date_cre(),"Error Location "+key,e]
                csv_write(save_name,"a",write_value)
            else:    #正常終了した時
                break
        else:
            error_dir = abspath+"/graduation-research/data/Error"
            save_name = error_dir+"/Errorlog"+"/windy_"+key+".csv"
            write_value = [wis.now_date_cre(),"Error Location "+key,"failed 3 times "]
            csv_write(save_name,"a",write_value)

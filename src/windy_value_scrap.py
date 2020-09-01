"""
スクレイピングで属性の値を取得 : https://www.seleniumqref.com/api/python/element_infoget/Python_get_attribute.html
スクレイピングでのtry処理 : https://tanuhack.com/stable-selenium/

windy.comから数値をスクレイピングする
"""
from selenium import webdriver
import csv
import time
from selenium.webdriver.chrome.options import Options
import exe
import os
import windy_image_scrap as wis
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
#2次元配列を1次元にするために
import itertools

def main(driver,atribute,abspath):
    #画像保存先のディレクトリパス
    dir_pass = abspath+"/graduation-research/data/windy_value"
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
    #wind_table = driver.find_element_by_css_selector("#detail-data-table > tbody > tr.td-windCombined.height-windCombined.d-display-waves")
    #print(wind_table.text())
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

        val_row = val_roup(wait,key,value)
        print(val_row)
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
                wis.create_date_dir(dir_pass,atribute=wind_name[i],date=False)    #ディレクトリ作成
                csv_write(dir_pass+"/"+wind_name[i]+"/"+file_name+".csv",write_mode,wind_lists)
        else:
            wis.create_date_dir(dir_pass,atribute=key,date=False)                  #ディレクトリ作成
            val_row = list(itertools.chain.from_iterable(val_row))
            csv_write(dir_pass+"/"+key+"/"+file_name+".csv",write_mode,val_row)


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

    """
    #cssセレクタでWebElementの取得,取得したい情報が読み込まれるまで待機して読み込む処理
    val_table = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
    #csvに書き込む配列
    val_list = []

    if value == "date":
        val = val_table.find_elements_by_tag_name('td')
        
        print("tdの数"+str(len(val)))
        for i in range(0,len(val)):
            #wind_col = wind_table[i].find_element_by_tag_name('td')
            #print("せいこう"+" 　"+str(i))
            #print(val[i].get_attribute("data-day"))
            der_val = newline_spl(val[i].get_attribute("data-day"))
            val_list.append(der_val)
    else:
        val = val_table.find_elements_by_tag_name('td')
        print("tdの数"+str(len(val)))
        for i in range(0,len(val)):
            #wind_col = wind_table[i].find_element_by_tag_name('td')
            #print("せいこう"+" 　"+str(i))
            #print(val[i].text)
            der_val = newline_spl(val[i].text)
            val_list.append(der_val)
        #val_list = list(itertools.chain.from_iterable(val_list))
    return val_list

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
    print("tdの数"+str(len(wind_speed)))
    print(wind_speed)
    print("max_wind_speed")
    print("tdの数"+str(len(max_wind_speed)))
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
    
    for i, (key,value) in enumerate(atri.items()):
        for _ in range(0,3):#最大3回tryする
            try :
                driver = exe.start_up(headless_active=True, web_url=value,abspath=abspath)
                main(driver,key,abspath)
            except Exception as e :     #全てのエラーで
                time.sleep(20)
                driver = exe.start_up(headless_active=True, web_url=value,abspath=abspath)
                main(driver,key,abspath)
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
            write_value = [wis.now_date_cre(),"Error Location "+key,"3回失敗"]
            csv_write(save_name,"a",write_value)

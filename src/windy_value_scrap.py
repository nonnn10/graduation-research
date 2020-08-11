"""

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

def main(driver,atribute):
    #画像保存先のディレクトリパス
    dir_pass = "../data/windy_value/"
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
        wis.create_date_dir(dir_pass,key,date=False)    #ディレクトリ作成

        val_row = val_roup(wait,key,value)
        print(val_row)
        if key == "wind_speed":
            #if文でwind_apeedなら
            wind_speed = []
            max_wind_speed = []
            for i in range(0,len(val_row)):
                wind_speed.append(val_row[i][0])
                max_wind_speed.append(val_row[i][1])
            print("wind_speed")
            print(wind_speed)
            print("max_wind_speed")
            print(max_wind_speed)

    wind_table = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#detail-data-table > tbody > tr.td-windCombined.height-windCombined.d-display-waves')))

    wave_table = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#detail-data-table > tbody > tr.td-waves.height-waves.d-display-waves')))
    #wait = WebDriverWait(wind_table, 20)
    #wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, 'td')))
    #aa = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "td-windCombined")))
    wind_val = wind_table.find_elements_by_tag_name('td')

    wave_val = wave_table.find_elements_by_tag_name('td')
    print("tdの数"+str(len(wave_val)))
    #wait = WebDriverWait(driver, 10)
    
    print(wave_val[0].text)
    #print(aa[1].find_element_by_tag_name("div").text)
    #for i in range(0,len(wave_val)):
        #wind_col = wind_table[i].find_element_by_tag_name('td')
        #print("せいこう"+"  "+str(i))
        #print(wave_val[i].text)
    # ドライバーを終了
    driver.close()
    #driver.quit()

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
            print("せいこう"+" 　"+str(i))
            print(val[i].get_attribute("data-day"))
            der_val = newline_spl(val[i].get_attribute("data-day"))
            val_list.append(der_val)
    else:
        val = val_table.find_elements_by_tag_name('td')
        print("tdの数"+str(len(val)))
        for i in range(0,len(val)):
            #wind_col = wind_table[i].find_element_by_tag_name('td')
            print("せいこう"+" 　"+str(i))
            print(val[i].text)
            der_val = newline_spl(val[i].text)
            val_list.append(der_val)
    
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
    #a="#\n24\n30"
    value = value.splitlines()
    try:
        value.remove("#")
    except ValueError as e:
        #print(e)
        pass

    return value

if __name__ == "__main__":
    atri = {"value":"https://www.windy.com/24.435/124.004/waves?waves,24.344,123.967,10"}
            #"wave_height":"https://www.windy.com/24.435/124.004/waves?waves,24.344,123.967,10"}
    for i, (key,value) in enumerate(atri.items()):
        driver = exe.start_up(headless_active=True, web_url=value)
        main(driver,key)
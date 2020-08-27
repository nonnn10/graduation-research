"""
コマンドライン引数 : https://qiita.com/taashi/items/07bf75201a074e208ae5
webのリロード : https://www.seleniumqref.com/api/python/window_set/Python_refresh.html

コマンドラインから時間の引数を受け取り,波と風の時間のスクリーンショットをとる
ディレクトリは「../data/windy_img/now_scrape」の中のwave_height,wind_speedのそれぞれの時間9:00,11:00...17:00それぞれのディレクトリに
2020-08-31 17:00:00.png　というファイル名で保存
"""
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

def main(driver,atribute,args):
    #コマンドラインから取得した引数をscrap_timeに代入
    scrap_time = args[1]

    #画像保存先のディレクトリパス
    dir_pass = "../data/now_img_scrape"+"/"+atribute

    wis.create_date_dir(dir_pass,scrap_time,date=False)    #ディレクトリ作成

    now_date = wis.now_date_cre()

    #画像ファイル名の作成に必要
    month = re.sub(r'(\d*)-(\d*)-(\d*)', r'\2',now_date)
    yaer = re.sub(r'(\d*)-(\d*)-(\d*)', r'\1',now_date)

    time.sleep(10)
    # ウィンドウサイズを設定
    driver.set_window_size(1200, 850)
    #ウィンドウサイズの確認
    time.sleep(3)
    size = driver.get_window_size()
    print("Window size: width = {}px, height = {}px.".format(size["width"], size["height"]))
    
    #ここでwebのリロード
    driver.refresh()
    time.sleep(3)
    #何かをクリック
    #search-weather-bg
    elements = driver.find_elements_by_id("search-weather-bg")
    loc = elements[0].location
    x, y = loc['x'], loc['y']
    #x = 55
    #y = 820                      #追加
    #print("座標xの値"+str(x))
    #print("座標yの値"+str(y))
    #x += time_num[i]
    print("座標xの値"+str(x))
    actions = ActionChains(driver)
    actions.move_by_offset(x, y)
    actions.click()
    actions.perform()

    time.sleep(3)
    #時間の取得
    img_name = driver.find_element_by_css_selector("#progress-bar > div.timecode.main-timecode").text
    img_date = 0
    next_month = False
    #ファイル名を作成
    img_name_date,img_date,next_month= wis.file_name_date(img_name,img_date,next_month,yaer,month)
    print(img_name_date)
    #スクリーンショットを作成,保存
    time.sleep(3)
    sfile = driver.get_screenshot_as_file(dir_pass+'/'+scrap_time+'/'+str(img_name_date)+'.png')
    print(sfile)

    driver.close()
    driver.quit()


if __name__ == '__main__':
    
    atri = {"wind_speed":"https://www.windy.com/?24.343,123.967,10",
            "wave_height":"https://www.windy.com/ja/-%E6%B3%A2-waves?waves,24.343,123.967,10"}
    args = sys.argv
    for i, (key,value) in enumerate(atri.items()):
        driver = exe.start_up(headless_active=True, web_url=value)
        try:
            main(driver,key,args)
        except Exception as e : 
            print(e)
            driver.get_screenshot_as_file('../data/windy_img'+'/Error.png')
            driver.close()
            driver.quit()
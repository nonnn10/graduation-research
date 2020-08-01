"""
スクリーンショット : #https://m4usta13ng.hatenablog.com/entry/20181118_py_selenium_screenshot
for文によるerror,ActionChains解決 : https://kurozumi.github.io/selenium-python/api.html#selenium.webdriver.common.action_chains.ActionChains.reset_actions

windy.comから画像をスクレイピングする
"""
from selenium import webdriver
import csv
import time
from selenium.webdriver.chrome.options import Options
import exe
import os
from selenium.webdriver.common.action_chains import ActionChains    #wendyの時間帯のバーをクリックするの必要
#wait処理に必要
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#日付取得
import datetime as dt
#日付の年,月,週の計算を可能にする
from dateutil.relativedelta import relativedelta
#正規表現置換
import re



def main(driver):
    #画像保存先のディレクトリパス
    dir_pass = "../data/windy_img/"
    now_date = create_date_dir(dir_pass)    #ディレクトリ作成
    #画像ファイル名の作成に必要
    month = re.sub(r'(\d*)-(\d*)-(\d*)', r'\2',now_date)
    yaer = re.sub(r'(\d*)-(\d*)-(\d*)', r'\1',now_date)

    time.sleep(3)
    # ウィンドウサイズを設定
    driver.set_window_size(1200, 850)
    #picker-close-buttonが表示されるまで待つ処理
    #WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, "picker-close-button")))

    #参考
    #https://qiita.com/motoki1990/items/a59a09c5966ce52128be
    day1_time_num = {
        0 : 23,#7:00
        1 : 30,#9:00
        2 : 38,#11:00
        3 : 43,#13:00
        4 : 50,#15:00
        5 : 60,#17:00
    }
    day2_time_num = {
        0 : 105,
        1 : 112,
        2 : 120,
        3 : 127,
        4 : 135,
        5 : 142,
    }
    day3_time_num = {
        0 : 189,
        1 : 197,
        2 : 204,
        3 : 211,
        4 : 217,
        5 : 222
    }
    day4_time_num = {
        0 : 271,
        1 : 278,
        2 : 285,
        3 : 292,
        4 : 298,
        5 : 305
    }
    day5_time_num = {
        0 : 354,
        1 : 328,
        2 : 335,
        3 : 342,
        4 : 349,
        5 : 356
    }



    # driver.close()
    #img_dateの初期化
    img_date = 0

    time_num = day5_time_num

    for i in range(0,len(time_num)):
        try:
            error=False
            mouse_move(time_num,i,driver,error)
        except Exception:
            error = True
            mouse_move(time_num,i,driver,error)
        time.sleep(3)
        
        #WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, "leaflet-canvas")))
        #png = driver.find_element_by_class_name("leaflet-canvas").screenshot_as_png
        
        #img_nameの
        img_name = driver.find_element_by_css_selector("#progress-bar > div.timecode.main-timecode").text
        #print(img_name)
        
        #ここに関数
        img_name_date = file_name_date(img_name,img_date,yaer,month)

        # img_date = re.sub(r'(.*) (\d{1,2}) - (\d{1,2}:\d{2})', r'\2',img_name)
        # print(img_name)
        print(img_name_date)
        sfile = driver.get_screenshot_as_file(dir_pass+now_date+'/'+str(img_name_date)+'.png')
        print(sfile)
        #with open('../data/windy_img/'+img_name+'.png', 'wb') as f:
        #    f.write(png)

    # ドライバーを終了
    driver.close()
    # driver.quit()

def mouse_move(time_num,i,driver,error=False):
    """
    任意の時間にマウスを移動させる
    
    parameters
    ----------
    time_num : dictionary
        スクリーンショットを取得したい時間帯の辞書
    i : int
        time_numの時間帯を指定する
    error : bool
        try構文での判定により動きを変更する
    """
    if error == False:
        print("No error")
        time.sleep(2)
        driver.set_window_size(1200, 850)
        time.sleep(2)
        elements = driver.find_elements_by_class_name("played")
        loc = elements[0].location
        x, y = loc['x'], loc['y']
        x += time_num[i]
        print("座標xの値"+str(x))
        actions = ActionChains(driver)
        actions.move_by_offset(x, y)
        actions.click()
        actions.perform()
    elif error == True:
        print("エラー")
        time.sleep(2)
        driver.set_window_size(1200, 850)
        time.sleep(2)
        elements = driver.find_elements_by_class_name("played")
        loc = elements[0].location
        x, y = loc['x'], loc['y']
        x += time_num[i]
        print("座標xの値"+str(x))
        actions = ActionChains(driver)
        actions.reset_actions()
        actions.move_by_offset(x, y)
        actions.click()
        actions.perform()

def create_date_dir(dir_pass):
    """
    画像を取得した日付のディレクトリを作成
    そのディレクトリに取得した画像を保存

    parameters
    ----------
    dir_pass : str
        固定のディレクトリ、日付ディレクトリの上層

    return
    ------
    now_date : str
        今日の日付
    """
    now_date = dt.datetime.now().strftime('%Y-%m-%d')   #日付の取得(2020-07-26)
    #ディレクトリ作成
    if not os.path.exists(dir_pass+now_date): #../data/windy_img/の階層に日付のディレクトリがないなら
        os.makedirs(dir_pass+now_date, exist_ok=True)

    return now_date

def file_name_date(img_name,img_date,yaer,month):
    """
    画像のファイル名を日付と時間帯にする関数

    parameters
    ----------
    img_name : str
        画像の取得日付と時間の文字列
    img_date : int
        画像の日付
    yaer : str
        画像を取得した日の年
    month : str
        画像を取得した日の月

    return
    ------
    img_name_date : str
        画像のファイル名
    """
    #file名の変更
    img_name = re.sub(r'(.*)(\d{1,2}:\d{2})\n(.*)', r'\1\2',img_name)       #正規表現で変換(水曜日 29 - 17:00)
    img_date_now = int(re.sub(r'(.*) (\d{1,2}) - (\d{1,2}:\d{2})', r'\2',img_name))      #正規表現で変換,日付の部分のみ(29)
    img_date_time= re.sub(r'(.*) (\d{1,2}) - (\d{1,2}:\d{2})', r'\3',img_name)      #正規表現で変換,日付の部分のみ(29)


    if img_date <= img_date_now:        #30 <= 31
        img_date = img_date_now         #1日前の日付を今の日付に上書き
        img_name_date = yaer+"-"+month+"-"+str(img_date)+" "+img_date_time    #年-月-日 時間
        img_name_date = dt.datetime.strptime(img_name_date,"%Y-%m-%d %H:%M")      #datetime型に変換

    elif img_date >= img_date_now:      #31 >= 1
        img_date = img_date_now         #1日前の日付を今の日付に上書き
        img_name_date = yaer+"-"+month+"-"+str(img_date)+" "+img_date_time     #年-月-日 時間
        img_name_date = dt.datetime.strptime(img_name_date,"%Y-%m-%d %H:%M")      #datetime型に変換
        img_name_date = img_name_date + relativedelta(months=1)         #次の月にするための計算

    return img_name_date

if __name__ == '__main__':
    driver = exe.start_up(headless_active=True, web_url='https://www.windy.com/ja/-%E6%B3%A2-waves?waves,24.343,123.967,10')
    main(driver)
    
    #https://www.windy.com/ja/-%E6%B3%A2-waves?waves,24.343,123.967,10,i:pressure,m:elVajBL
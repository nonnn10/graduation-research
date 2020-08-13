"""
スクリーンショット : #https://m4usta13ng.hatnablog.com/entry/20181118_py_selenium_screenshot
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
    dir_pass = "../data/windy_img/"
    #atribute = "wind_speed"
    print(atribute)
    now_date = now_date_cre()
    create_date_dir(dir_pass,atribute)    #ディレクトリ作成
    #画像ファイル名の作成に必要
    month = re.sub(r'(\d*)-(\d*)-(\d*)', r'\2',now_date)
    yaer = re.sub(r'(\d*)-(\d*)-(\d*)', r'\1',now_date)

    time.sleep(20)
    # ウィンドウサイズを設定
    driver.set_window_size(1200, 850)
    #ウィンドウサイズの確認
    size = driver.get_window_size()
    print("Window size: width = {}px, height = {}px.".format(size["width"], size["height"]))
    #picker-close-buttonが表示されるまで待つ処理
    #WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, "picker-close-button")))

    #参考
    #https://qiita.com/motoki1990/items/a59a09c5966ce52128be
    
    # driver.close()
    #img_dateの初期化
    img_date = 0
    date_all = date_list()
    
    #待機処理のための設定(30秒)
    wait = WebDriverWait(driver, 30)

    for i in range(0,len(date_all)):
        for j in range(0,len(date_all[i])):
            try:
                error=False
                time.sleep(10)
                mouse_move(date_all[i],j,driver,error)
            except Exception:
                error = True
                time.sleep(10)
                mouse_move(date_all[i],j,driver,error)
            #time.sleep(3)
            
            #WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, "leaflet-canvas")))
            #png = driver.find_element_by_class_name("leaflet-canvas").screenshot_as_png
            
            #img_nameの待機処理を追加(学科の方でエラーが出る)
            #img_name = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#progress-bar > div.timecode.main-timecode"))).text
            time.sleep(20)
            img_name = driver.find_element_by_css_selector("#progress-bar > div.timecode.main-timecode").text
            #print(img_name)
            
            #ここに関数
            img_name_date = file_name_date(img_name,img_date,yaer,month)

            # img_date = re.sub(r'(.*) (\d{1,2}) - (\d{1,2}:\d{2})', r'\2',img_name)
            # print(img_name)
            print(img_name_date)
            sfile = driver.get_screenshot_as_file(dir_pass+now_date+'/'+atribute+'/'+str(img_name_date)+'.png')
            print(sfile)
            #with open('../data/windy_img/'+img_name+'.png', 'wb') as f:
            #    f.write(png)

    # ドライバーを終了
    driver.close()
    driver.quit()

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
        #driver.set_window_size(1200, 850)
        time.sleep(10)
        elements = driver.find_elements_by_class_name("played")
        loc = elements[0].location
        x, y = loc['x'], loc['y']
        x = 55
        y = 820                      #追加
        print("座標xの値"+str(x))
        print("座標yの値"+str(y))
        x += time_num[i]
        print("座標xの値"+str(x))
        actions = ActionChains(driver)
        actions.move_by_offset(x, y)
        actions.click()
        actions.perform()
    elif error == True:
        print("エラー")
        time.sleep(2)
        #driver.set_window_size(1200, 850)
        time.sleep(10)
        elements = driver.find_elements_by_class_name("played")
        loc = elements[0].location
        x, y = loc['x'], loc['y']
        print("座標xの値"+str(x))
        x += time_num[i]
        print("座標xの値"+str(x))
        actions = ActionChains(driver)
        actions.reset_actions()
        actions.move_by_offset(x, y)
        actions.click()
        actions.perform()

def now_date_cre():
    """
    プログラム実行時の日付を返す関数

    return
    ------
    now_date : datetime
        プログラム実行時の日付を取得
    """
    now_date = dt.datetime.now().strftime('%Y-%m-%d')   #日付の取得(2020-07-26)
    return now_date

def create_date_dir(dir_pass,atribute,date=True):
    """
    画像を取得した日付のディレクトリを作成
    日付ディレクトリの下に風速、波高ディレクトリ
    そのディレクトリに取得した画像を保存

    parameters
    ----------
    dir_pass : str
        固定のディレクトリ、日付ディレクトリの上層
    atribute : str
        風、波のいずれか
    date : bool
        日付をディレクトリに含めない時
    """

    atribute = "/"+atribute
    #ディレクトリ作成
    if date == True:
        now_date = dt.datetime.now().strftime('%Y-%m-%d')   #日付の取得(2020-07-26)   
        if not os.path.exists(dir_pass+now_date): #../data/windy_img/の階層に日付のディレクトリがないなら
            os.makedirs(dir_pass+now_date, exist_ok=True)
        if not os.path.exists(dir_pass+now_date+atribute): #../data/windy_img/日付/の階層にatiributeのディレクトリがないなら
            os.makedirs(dir_pass+now_date+atribute, exist_ok=True)
        print(dir_pass+now_date+atribute)
    else:
        dir_pass = dir_pass+atribute    #ディレクトリパス最後にatributeを追加
        dir_list = dir_pass.split("/")  #ディレクトリパスを"/"で分割
        for i in range(0,len(dir_list)):#ディレクトリ階層の数だけループ,最初に../がある想定
            i += 1
            if not os.path.exists("/".join(dir_list[0:i])):             #ディレクトリ階層が存在するかチェック
                os.makedirs("/".join(dir_list[0:i]), exist_ok=True)     #存在しないなら作成

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
    img_name_date : datetime
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

def date_list():
    """
    日付、時間のx軸の値
    """
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
        1 : 361,
        2 : 368,
        3 : 375,
        4 : 382,
        5 : 389
    }
    day6_time_num = {
        0 : 438,
        1 : 445,
        2 : 452,
        3 : 457,
        4 : 464,
        5 : 471
    }
    day7_time_num = {
        0 : 520,
        1 : 527,
        2 : 534,
        3 : 541,
        4 : 548,
        5 : 555
    }
    day8_time_num = {
        0 : 600,
        1 : 607,
        2 : 614,
        3 : 621,
        4 : 628,
        5 : 635
    }
    day9_time_num = {
        0 : 684,
        1 : 691,
        2 : 698,
        3 : 705,
        4 : 712,
        5 : 719
    }
    day10_time_num = {
        0 : 765,
        1 : 772,
        2 : 779,
    }
    date_all = [day1_time_num,day2_time_num,
                day3_time_num,day4_time_num,
                day5_time_num,day6_time_num,
                day7_time_num,day8_time_num,
                day9_time_num,day10_time_num]
    return date_all


if __name__ == '__main__':
    
    atri = {"wind_speed":"https://www.windy.com/?24.343,123.967,10",
            "wave_height":"https://www.windy.com/ja/-%E6%B3%A2-waves?waves,24.343,123.967,10"}
    
    for i, (key,value) in enumerate(atri.items()):
        driver = exe.start_up(headless_active=True, web_url=value)
        try:
            main(driver,key)
        except Exception as e : 
            print(e)
            driver.close()
            driver.quit()
    #https://www.windy.com/?24.343,123.967,10  風
    #https://www.windy.com/ja/-%E6%B3%A2-waves?waves,24.343,123.967,10  波

    #https://www.windy.com/ja/-%E6%B3%A2-waves?waves,24.343,123.967,10,i:pressure,m:elVajBL
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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
    now_date = wis.create_date_dir(dir_pass,atribute)    #ディレクトリ作成
    #画像ファイル名の作成に必要
    month = re.sub(r'(\d*)-(\d*)-(\d*)', r'\2',now_date)
    yaer = re.sub(r'(\d*)-(\d*)-(\d*)', r'\1',now_date)

    time.sleep(3)
    # ウィンドウサイズを設定
    driver.set_window_size(1200, 850)

    # ドライバーを終了
    #driver.close()
    #driver.quit()


if __name__ == "__main__":
    atri = {"wind_speed":"https://www.windy.com/?24.343,123.967,10",
            "wave_height":"https://www.windy.com/ja/-%E6%B3%A2-waves?waves,24.343,123.967,10"}
    for i, (key,value) in enumerate(atri.items()):
        driver = exe.start_up(headless_active=False, web_url=value)
        main(driver,key)
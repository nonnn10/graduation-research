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
    now_date = wis.create_date_dir(dir_pass,atribute)    #ディレクトリ作成
    #画像ファイル名の作成に必要
    month = re.sub(r'(\d*)-(\d*)-(\d*)', r'\2',now_date)
    yaer = re.sub(r'(\d*)-(\d*)-(\d*)', r'\1',now_date)

    time.sleep(3)
    # ウィンドウサイズを設定
    driver.set_window_size(2000, 850)

    buttun = driver.find_element_by_css_selector("#detail > div.table-wrapper.show.noselect.notap > div.data-table.noselect.flex-container > div.forecast-table.progress-bar > div.fg-red.size-xs.inlined.clickable")
    buttun.click()
    time.sleep(10)
    #wind_table = driver.find_element_by_css_selector("#detail-data-table > tbody > tr.td-windCombined.height-windCombined.d-display-waves")
    #print(wind_table.text())
    wait = WebDriverWait(driver, 10)
    wind_table = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#detail-data-table > tbody > tr.td-windCombined.height-windCombined.d-display-waves')))
    #wait = WebDriverWait(wind_table, 20)
    #wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, 'td')))
    #aa = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "td-windCombined")))
    wind_val = wind_table.find_elements_by_tag_name('td')
    print("tdの数"+str(len(wind_val)))
    #wait = WebDriverWait(driver, 10)
    
    print(wind_val[0].text)
    #print(aa[1].find_element_by_tag_name("div").text)
    for i in range(0,len(wind_val)):
        #wind_col = wind_table[i].find_element_by_tag_name('td')
        print("せいこう"+"  "+str(i))
        print(wind_val[i].text)
    # ドライバーを終了
    #driver.close()
    #driver.quit()


if __name__ == "__main__":
    atri = {"value":"https://www.windy.com/24.435/124.004/waves?waves,24.344,123.967,10"}
            #"wave_height":"https://www.windy.com/24.435/124.004/waves?waves,24.344,123.967,10"}
    for i, (key,value) in enumerate(atri.items()):
        driver = exe.start_up(headless_active=False, web_url=value)
        main(driver,key)
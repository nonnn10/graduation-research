"""
windy.comから画像をスクレイピングする
"""
from selenium import webdriver
import csv
import time
from selenium.webdriver.chrome.options import Options
import exe
import os
from selenium.webdriver.common.action_chains import ActionChains


def main(driver):
    #sfile = driver.get_screenshot_as_file("../data/windy_img/File01.png")  #webサイトの表示サイズでスクリーン取得
    #print(sfile)
    time.sleep(3)
        # ウィンドウサイズとズームを設定
    #driver.set_window_size(870, 650)
    #driver.execute_script("document.body.style.zoom='90%'")
    #参考
    #https://qiita.com/motoki1990/items/a59a09c5966ce52128be
    
    elements = driver.find_elements_by_class_name("played")
    loc = elements[0].location
    x, y = loc['x'], loc['y']
    x +=200
    actions = ActionChains(driver)
    actions.move_by_offset(x, y)
    actions.click()
    actions.perform()
    #driver.execute_script("('.played').width(400);") # いらん要素を消す(jquery)
    #mm-hide zoom10 product-ecmwfWaves overlay-waves onrhpane onpatch sea onisolines platform-desktop selectedpois-favs onpicker
    #leaflet-pane leaflet-tooltip-pane
    #https://m4usta13ng.hatenablog.com/entry/20181118_py_selenium_screenshot
    png = driver.find_element_by_class_name("leaflet-canvas").screenshot_as_png

    with open('../data/windy_img/img.png', 'wb') as f:
        f.write(png)
    # ドライバーを終了
    driver.close()
    # driver.quit()
if __name__ == '__main__':
    driver = exe.start_up(headless_active=False, web_url='https://www.windy.com/ja/-%E6%B3%A2-waves?waves,24.343,123.967,10,i:pressure,m:elVajBL')
    main(driver)
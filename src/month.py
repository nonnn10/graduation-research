from selenium import webdriver
import csv
import time
from selenium.webdriver.chrome.options import Options
import exe      #ファイルのコードをname==mainにしていないとimport時に実行されてしまう

def main():
    driver = exe.start_up(headless_active=True,web_url='http://www.aneikankou.co.jp/timetables?date=2017-01-01')
    for i in range(365):          #rangeで取得する日付データ数を指定
        # csv_file_name = exe.date_result(driver)

        # take_route,name,data = exe.name_data_append(driver)     #航路、データを変数に格納

        # #書き込み
        # f = open(csv_file_name, 'w', encoding='cp932', errors='ignore')
        # writer = csv.writer(f, lineterminator='\n')

        # route_start,result_data = exe.sep(take_route,writer)
        # exe.datewrite(route_start,result_data,writer)

        # # name,data = name_data_append(driver)

        # exe.sima_roup(name,data,writer)
        exe.main(driver)
                
        # f.close()

        past_operation_status(driver)
        day, current_day, next_month_day, = date_list(driver)
        date_transition(day, current_day, next_month_day)
        
    driver.close()
    driver.quit()

def past_operation_status (driver):
    """
    過去の運行状況ボタンをクリックする関数

    Parameters
    ----------
    driver : WebDriver
        Chromeのドライバー
    """
    past_state_buttun =  driver.find_element_by_class_name('btn-success')
    past_state_buttun.click()

def date_list (driver):
    """
    日付の表から次の日のWebElementを配列に入れる関数

    parameters
    ----------
    draiver : WebDriver
        Chromeのドライバー

    Returns
    -------
    day : list
        現在の月の日付が配列として入る
    current_day : WebElement
        現在のページの日付情報が入っている
    next_month_day : WebElement
        次の月の一日の情報が入っている
    """
    date = driver.find_element_by_css_selector('body > div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-right.datepicker-orient-bottom > div.datepicker-days > table > tbody')
    #print(date.text)
    day_list = date.find_elements_by_tag_name("td")         #表全ての日付け
    current_day = date.find_element_by_class_name("active") #現在のページの日付け
    next_month_day = date.find_elements_by_class_name("new") #次の月の1日め
    day = []        #現在の月の日付全て
    count = 0
    for i in day_list:
        if i.text == "1":
            if count == 1:
                count += 1
                continue
            count+=1
            day.append(i)
            #print(i.text)
        elif count == 1 :
            day.append(i)
            #print(i.text)
        else :
            continue

    return day, current_day, next_month_day

def date_transition (day, current_day, next_month_day):
    """
    次の日付をクリックする関数

    parameters
    ----------
    day : list
        現在の月の日付が配列として入る
    current_day : WebElement
        現在のページの日付情報が入っている
    next_month_day : WebElement
        次の月の一日の情報が入っている

    """
    try:
        time.sleep(1)
        day[int(current_day.text)].click()
        print("NO Error")
    except IndexError:
        time.sleep(1)
        next_month_day[0].click()
        print("next month move")
    #exe.date_result(driver)

if __name__ == '__main__':
    main()
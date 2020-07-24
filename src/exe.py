from selenium import webdriver
import csv
import time
from selenium.webdriver.chrome.options import Options

"""
安永観光から欠航情報データを取得するスクリプト
csvファイルの書き込みの仕方
    datewritte()の引数で指定,sima_roup()の中にもあるから気をつける

class化したほうがいいかもdatewritte()の引数が多すぎる
"""

def main(driver):
    # driver = start_up(headless_active=True, web_url='http://www.aneikankou.co.jp/timetables')

    csv_file_name = date_result(driver)     #取得した情報の日付

    take_route,name,data = name_data_append(driver)     #航路、データを変数に格納

    file_name = csv_file_name
    writte_mode = "w"

    #竹富島の航路情報書き出し
    route_start,result_data,route_name = sep(take_route)
    datewrite(route_start,result_data,route_name,csv_file_name,file_name,writte_mode)

    #竹富島以外の航路情報書き出し
    sima_roup(name,data,csv_file_name)
            
    # f.close()
    # driver.close()   #この行と下の1行はheadlessモード出ない時には必要
    # driver.quit()

def start_up (headless_active,web_url):
    """
    Chromeのドライバーを指定する
    ヘッドレスモードにするか指定する
    
    parameters
    ----------
    options_active : bool
        ヘッドレスにする場合True
    Returns
    -------
    draiver : WebDriver
        Chromeのドライバー
    
    """
    options = Options()
    if headless_active == True:    
        options.add_argument('--headless')          #ヘッドレスモードのオプション
    #絶対パスでドライバーの場所を指定
    driver = webdriver.Chrome('/Users/nallab/Desktop/卒業研究/ChromeDriver/chromedriver',options=options)
    driver.get(web_url)
    #driver.get('http://www.aneikankou.co.jp/timetables?date=2016-04-01')
    # time.sleep(3)
    return driver

def sep (route):
    """
    航路の表から航路の名前の書き出し、出発港、時間と運行結果の変数格納
    竹富島の表専用
    parameters
    ----------
    route : WebElement
        竹富島の航路表の情報
    writer : csv.writer
        csvの情報

    return
    ------
    route_start : list
        出発港の配列
    result_data : list
        時間と運行結果の配列
    eng_transform(route_name.text) : str
        スペルに直した航路の名前
    """
    route_name = route.find_element_by_tag_name('h2')       #航路名の名前
    route_start = route.find_elements_by_tag_name('th')     #出発港の名前
    result_data = route.find_elements_by_tag_name('td')     #時間と運行結果

    #配列でないとcsvに書き出す際にカンマが一文字ごとに入ってしまうため
    #writer.writerow([eng_transform(route_name.text)])       #航路名の書き出し


    return route_start,result_data,eng_transform(route_name.text)

def eng_transform(route_name):
    """
    日本語の名前を英語のスペルに変換
    航路と出発港を英語に変換
    
    parameters
    ----------
    route_name : str
        航路名、出発港
        hoge.textの形で引数を入れる
    
    return
    ------
    eng_route_name : str
        航路、出発港の英語スペルを配列で格納
    """
    eng_name_dic = {
        "竹富島航路" : "taketomi_route",
        "黒島航路" : "kurosima_route",
        "小浜島航路" : "kohama_route",
        "西表島上原航路" : "iriomote_uehara_route",
        "鳩間島航路" : "hatoma_route",
        "西表島大原航路" : "iriomote_ohara_route",
        "波照間島航路" : "hateruma_route",
        "石垣発" : "isigaki_dep",
        "竹富発" : "taketomi_dep",
        "黒島発" : "kurosima_dep",
        "小浜発" : "kohama_dep",
        "上原発" : "uehara_dep",
        "鳩間発" : "hatoma_dep",
        "大原発" : "ohara_dep",
        "波照間発" : "hateruma_dep"
    } 
    eng_route_name = eng_name_dic[route_name]
    return eng_route_name

def op_status_transe(datalist):     #運行状況の通常運行と欠航の情報を0,1に変換
    """
    運行状況の通常運行と欠航の情報を0,1に変換する関数

    parameters
    ----------
    datalist : list
        時間と運行状況の結果の入っている配列

    return
    ------
    datalist : list
        時間と0か1の運航状況の情報が格納
    """
    datalist = [0 if "通常運航" == i else i for i in datalist]  #通常運航を0に変換
    datalist = [1 if "欠航" == i else i for i in datalist]     #欠航を1に変換

    return datalist

def sep_2 (route_name, route_data):
    """
    関数sima_roupで使用
    航路の表から航路の名前の書き出し、出発港、時間と運行結果の変数格納

    parameters
    ----------
    route_name : WebElement
        航路の名前
    route_data : WebElement
        竹富島以外の航路表の情報
    
    return
    ------
    route_start : list
        出発港の配列
    result_data : list
        時間と運行結果の配列
    eng_transform(route_name.text) : str
        スペルに直した航路の名前
    """
    #writer.writerow([eng_transform(route_name.text)])
    route_start = route_data.find_elements_by_tag_name('th')     #出発港の名前
    result_data = route_data.find_elements_by_tag_name('td')     #時間と運行結果
    return route_start,result_data,eng_transform(route_name.text)

def datewrite (route_start,result_data,route_name,csv_file_name,file_name,writte_mode):
    """
    航路表から時間、運行結果の書き出し

    parameters
    ----------
    route_start : WebElement
        出発港の情報
    result_data : list
        時間と運行結果の配列
    route_name : str
        出発港の名前
    csv_file_name : str
        取得した情報の日付 (2020-7-15,2020-12-6)
    file_name : str
        ファイルの名前
    writte_mode : str
        書き込みモードを選択 a,追記　w,新しく上書き
    """
    #----------------------#
    file_name = "2017"          #2017年で一纏めにしてみたい
    writte_mode = "w"           #追記
    #----------------------#
    start_cul = 0
    for i in route_start:   #出発のループ
        #ファイルへの書き出しのためのfile open
        with open("../data/route/"+route_name+"/"+eng_transform(i.text)+"/"+file_name+".csv", writte_mode, encoding='UTF-8', errors='ignore') as f:
            writer = csv.writer(f, lineterminator='\n')            
            csvlist = []
            cnt = 0
            for j in result_data:   #時間と運行結果のループ
                cul_num = cnt % 4
                # print("カウント "+str(cnt))
                # print("start_cul "+str(start_cul))
                
                if start_cul == 0:
                    if cul_num == 0:
                        csvlist.append(coron_trans(j.text))     #時間を追加
                        cnt=cnt+1
                    elif cul_num == 1:
                        csvlist.append(j.text)          #運航状況の通常運航、欠航の追加
                        cnt=cnt+1
                        if True == ("-" in csvlist):    #「-」などの船が運航しなかった場合の対処
                            #print("-----" in csvlist)
                            csvlist = []
                            continue
                        else:
                            #print(csvlist)
                            #print("-----" in csvlist)
                            csvlist.append(csv_file_name)       #日付の追加   
                            writer.writerow(op_status_transe(csvlist))
                        csvlist = []
                    else:
                        cnt=cnt+1
                elif start_cul == 1:
                    if cul_num == 2:
                        csvlist.append(coron_trans(j.text))     #時間を追加
                        cnt=cnt+1
                    elif cul_num == 3:
                        csvlist.append(j.text)          #運航状況の通常運航、欠航の追加
                        cnt=cnt+1
                        if True == ("-" in csvlist):    #「-」などの船が運航しなかった場合の対処
                            #print("-----" in csvlist)
                            csvlist = []
                            continue
                        else :
                            #print(csvlist)
                            #print("-----" in csvlist)
                            csvlist.append(csv_file_name)   #日付の追加
                            writer.writerow(op_status_transe(csvlist))
                        csvlist = []
                    else:
                        cnt=cnt+1
            start_cul = start_cul+1

def coron_trans(data):
    """
    全角のコロン「：」を半角のコロン「:」に変換する関数

    parameter
    ---------
    data : str
        7:30や７：50などの文字が入っている
    
    return
    ------
    data : str
        全角のコロンを半角のコロンに置き換えた文字列を返す
    """
    data = data.replace('：', ':')

    return data


def sima_roup(name,data,csv_file_name):
    """
    竹富島以外の航路のループでデータのcsvへの書き出し

    prameter
    --------
    name : list
        出発港の配列
    data : list
        時間と運行結果の配列
    """
    file_name = csv_file_name
    writte_mode = "w"
    for i in range(6):      #6 = 航路の数
        route_start,result_data,route_name = sep_2(name[i],data[i])
        datewrite(route_start,result_data,route_name,csv_file_name,file_name,writte_mode)

def date_result(driver):
    """
    ファイルネームの格納

    parameter
    ---------
    driver : WebDriver
        ウェブページの情報
    
    return
    ------
    csv_file_name : str
        csvのファイルネーム
    """
    element = driver.find_element_by_class_name("today")        #YY年MM月DD日の運行状況のclass
    s = element.text
    print(s)
    print(s[0:4]+"-"+s[5:7]+"-"+s[8:10])
    print(s[8:10])
    #MMとDD先頭の0を削除する正規表現
    date = s[0:4]+"-"+s[5:7]+"-"+s[8:10]
    #csv_file_name = date + ".csv"      #ファイルネーム,YYYY-MM-DD.csv

    return date

def name_data_append(driver):
    """
    竹富島以外の航路情報の配列への格納
    css selecterでの指定

    parameter
    ---------
    driver : WebDriver
        ウェブページの情報
    
    return
    ------
    take_route : WebElement
        竹富島の航路表情報
    name : list
        竹富島以外の航路の名前を配列に格納
    data : list
        竹富島以外の航路の表情報を配列に格納
    """
    #element = driver.find_element_by_css_selector('#route-list')
    take_route = driver.find_element_by_css_selector('#route-list > div:nth-child(1)')

    name = []
    data = []

    kuro_route_name = driver.find_element_by_css_selector("#route-list > div:nth-child(2) > h2:nth-child(1)")
    name.append(kuro_route_name)
    kuro_route_data = driver.find_element_by_css_selector("#route-list > div:nth-child(2) > table:nth-child(2)")
    data.append(kuro_route_data)
    koha_route_name = driver.find_element_by_css_selector("#route-list > div:nth-child(2) > h2:nth-child(3)")
    name.append(koha_route_name)
    koha_route_data = driver.find_element_by_css_selector("#route-list > div:nth-child(2) > table:nth-child(4)")
    data.append(koha_route_data)
    iriue_route_name = driver.find_element_by_css_selector("#route-list > div:nth-child(3) > h2:nth-child(1)")
    name.append(iriue_route_name)
    iriue_route_data = driver.find_element_by_css_selector("#route-list > div:nth-child(3) > table:nth-child(2)")
    data.append(iriue_route_data)
    hato_route_name = driver.find_element_by_css_selector("#route-list > div:nth-child(3) > h2:nth-child(3)")
    name.append(hato_route_name)
    hato_route_data = driver.find_element_by_css_selector("#route-list > div:nth-child(3) > table:nth-child(4)")
    data.append(hato_route_data)
    irio_route_name = driver.find_element_by_css_selector("#route-list > div:nth-child(4) > h2:nth-child(1)")
    name.append(irio_route_name)
    irio_route_data = driver.find_element_by_css_selector("#route-list > div:nth-child(4) > table:nth-child(2)")
    data.append(irio_route_data)
    hate_route_name = driver.find_element_by_css_selector("#route-list > div:nth-child(4) > h2:nth-child(3)")
    name.append(hate_route_name)
    hate_route_data = driver.find_element_by_css_selector("#route-list > div:nth-child(4) > table:nth-child(4)")
    data.append(hate_route_data)
    
    return take_route,name,data
# def name_data_append(driver):
#     name = []
#     data = []
#     text="#route-list > div:nth-child({num}) > h2:nth-child({num2})"
#     for i in range(2,5):
#         for j in range(1,5):
#             if j % 2 == 0:
                
#                 result = text.format(num=i,num2=j)
#                 print(result)
#                 data.append(driver.find_element_by_css_selector(result))
#             else:
#                 result = text.format(num=i,num2=j)
#                 print(result)
#                 name.append(driver.find_element_by_css_selector(result))
#     return name,data

if __name__ == '__main__':
    driver = start_up(headless_active=True, web_url='http://www.aneikankou.co.jp/timetables')
    main(driver)



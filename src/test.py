import csv
import pandas as pd
import datetime as dt
import dateutil         #日付の計算に必要
from dateutil.relativedelta import relativedelta
import glob             #ディレクトリのファイル一覧を取得するためのモジュール
import re
import numpy as np
import file_date
import os
import hour_windy_img as hwi
import windy_image_scrap as wis
import exe
"""
dir_pass = "../data/windy_img/test.txt"#"/Users/e175755/graduation-research/data/windy_img/test.txt"
print('getcwd:      ', os.getcwd())
print('__file__:    ', __file__)
apath=os.getcwd()
#print()
dl = apath.split("/")  #ディレクトリパスを"/"で分割
print(dl)
dl.remove("")             #dir_listの中に""がある場合は削除
print(dl)


#print(dl.index('x'))

x = dl.index('graduation-research')
x = dl.index('Users')
x =+ 2
#x -= 1
print(x)
print("/"+"/".join(dl[0:x]))

def abspath_top():
    """
"""
    絶対パスを取得しその中のgraduation-researchより上の階層のpathを出力

    parameters
    ----------

    return
    ------
    top_path : str
        graduation-researchより上のpath
    """
"""
    apath=os.getcwd()       #スクリプトを実行した場所の絶対path
    dl = apath.split("/")   #ディレクトリパスを"/"で分割
    dl.remove("")           #dlの中に""がある場合は削除
    try:
        x = dl.index('graduation-research') #'graduation-research'のindex番号
    except ValueError:
        x = dl.index('Users')               #'Users'のindex番号
        x =+ 2
    top_path = "/"+"/".join(dl[0:x])
    
    return top_path

abspath = abspath_top()
print(abspath)
"""
x = "12:20大原経由"
y = exe.japan_lan_del(x)
print(y)
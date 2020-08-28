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
import windy_image_scrap as wis

dir_pass = "../data/windy_img/test.txt"#"/Users/e175755/graduation-research/data/windy_img/test.txt"
key = "date"
#wis.create_date_dir(dir_pass,atribute=key,date=False)
now_date = "\n"+str(dt.datetime.now())

print(now_date)
with open(dir_pass,mode = "a") as f:
    f.write(now_date)
    f.write("hello")
#print()
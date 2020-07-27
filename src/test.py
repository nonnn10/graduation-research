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

date = dt.datetime.now().strftime('%Y-%m-%d')
print(date)
if not os.path.exists("../data/windy_img/"+date):
            os.makedirs("../data/windy_img/"+date, exist_ok=True)
#df = file_date.dfarray()
#print(df)
print("../data/windy_img/"+date)
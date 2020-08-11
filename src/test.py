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

a=["#\n24\n30"]
#a=["23"]
a=a[0].splitlines()
print(a)
try:
    a.remove("#")
    print(type(a))
except ValueError as e:
    print(e)



print(a)
import csv
import pandas as pd
import datetime as dt
import dateutil         #日付の計算に必要
from dateutil.relativedelta import relativedelta
import glob             #ディレクトリのファイル一覧を取得するためのモジュール
import re
import numpy as np
import file_date

s = "14:20\nｼ励ｻｼ倥ｻｼ呎怦縺ｮ縺ｿ驕玖穐"

print(re.sub('(\d{1,2}):(\d{1,2})\n(.*)', r'\1:\2', s))
#df = file_date.dfarray()
#print(df)
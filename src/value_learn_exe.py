"""
"""
import numpy as np
from value_learn import Value_learn
from value_metrics import Value_metrics

route_name = "hatoma_route"
dep = "isigaki_dep"
days_ago = 0

#数値学習のインスタンス
vl = Value_learn(route_name,dep,days_ago)

vl.df_load(route_name,dep,days_ago)
print(vl.X)
vl.data_split(vl.X,vl.y,vl.df)
print('Labels counts in y[0 1]:', np.bincount(vl.y))
print('Labels counts in y_train[0 1]:', np.bincount(vl.y_train))
print('Labels counts in y_test[0 1]:', np.bincount(vl.y_test))

#標準化
vl.make_std(vl.X_train,vl.X_test)

#学習データセット作成
vl.make_train_data(vl.X_train, vl.y_train)
vl.make_test_data(vl.X_train, vl.y_train, vl.train_data)

vl.par()

vl.fit(vl.train_data, vl.test_data, vl.parameters, batch=100)

conf_path = '../data/images_conf/'
path_metrics = "../data/result_value/2_23_value.txt"
#学習評価のインスタンス
vm = Value_metrics(vl.model,vl.y_test,vl.X_test,vl.y_train,vl.X_train,path_metrics,conf_path)

vm.predict(vm.model,vm.X_test)

vm.auc_result(vm.y_test,vm.y_pred)
print("AUC {}".format(vm.auc))

vm.confm(route_name,dep,days_ago)
vm.metrics_score()


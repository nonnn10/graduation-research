"""
数値データを学習するためのクラス
"""
from sklearn import datasets
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import lightgbm as lgb


class Value_learn:
    def __init__(self, route_name, dep, days_ago):
        self.route_name = route_name
        self.dep = dep
        self.days_ago = days_ago
        self.read_data = '../data/df_com_all_4/'
    
    def df_load(self,route_name,dep,days_ago):
        """
        学習するためのdfを作成する。
        前処理が終わった後のdf
        parameters
        ----------
        route_name :str
            航路の名前(taketomi_route)
        dep : str
            出発港の名前(isigaki_dep)
        days_ago:str
            教師ラベルと説明変数を何日ずらしているか
            
        return
        ------
        X:dataframe
            説明変数のdf
        y:dataframe
            目的変数(教師ラベル)のdf 
        df : dataframe
            モデル評価、分析のために使用
        """

        df = pd.read_csv(self.read_data + route_name+'_'+dep+'_'+str(days_ago)+'.csv', header=None)
        #時間の列にNanがあるものを削除
        df = df.dropna(subset=[1])

        #データのロード
        self.X = df.iloc[:,3:12].values
        #print(X)
        self.y = df.loc[:, 1]#.values
        #print(y)
        self.df = df.iloc[:,3:12]
        return self.X,self.y,self.df
    
    #データの分割（テスト用とトレーニング用）


    def data_split(self,X,y,df):
        """
        訓練データと教師データ、dfを教師データ2割りの割合で分割
        parameters
        ----------
        X : nparray
            特徴量(風速、最大風速、最大風速の風向、波高、時間、波の向き、うねり、うねりの向き、うねりの間隔)
        y : nparray
            教師ラベル(0:運航、1:欠航)

        return
        ------
        X_train,X_test : nparray
            特徴量のトレーニングとテスト
        y_train,y_test : nparray
            教師ラベルのトレーニングとテスト
        df_train,df_test : dataframe
            X,yの日付や時間を確認するため
        """
        self.X_train, self.X_test, self.y_train, self.y_test, self.df_train, self.df_test = train_test_split(
            X, y, df, test_size=0.2, random_state=1, stratify=y)

        return self.X_train, self.X_test, self.y_train, self.y_test, self.df_train, self.df_test


    #標準化
    def make_std(self,X_train,X_test):
        """
        特徴量に標準化処理を行う
        parameters
        ----------
        X_train,X_test : nparray
            特徴量のトレーニングとテストデータ

        return
        ------
        X_train_std,X_test_std : nparray
            標準化を施した特徴量のトレーニングとテストデータ
        """
        self.sc = StandardScaler()
        self.sc.fit(self.X_train)
        self.X_train_std = self.sc.transform(self.X_train)
        self.X_test_std = self.sc.transform(self.X_test)
        return self.X_train_std, self.X_test_std
    
    #トレーニングデータ作成
    def make_train_data(self,X_train, y_train):
        """
        学習用データの作成
        parameters
        ----------
        X_train : nparray
            学習用のトレーニングデータ
        y_train : nparray
            学習用のラベルデータ

        returns
        -------
        train_data : 
            学習用データの作成
        """
        self.train_data = lgb.Dataset(self.X_train, label=self.y_train)
        return self.train_data

    # テストデータの作成    
    def make_test_data(self,X_test, y_test, train_data):
        """
        テストデータの作成
        parameters
        ----------
        X_test : nparray
            学習用のtestデータ
        y_test : nparray
            学習用のtestデータ

        returns
        -------
        test_data : 
            学習用データの作成
        """
        self.test_data = lgb.Dataset(self.X_test, label=self.y_test, reference=self.train_data)
        return self.test_data

    def par(self):
        """
        パラメータの辞書を定義
        oputnaで改善したい
        return
        ------
        parameter : dict
            LightGBMのパラメーター
        """
        self.boostring='dart'
        self.learning_rate=0.05
        self.min_data_in_leaf=20
        #applications='binary'
        self.feature_fraction=0.7
        self.num_leaves=41
        self.metric='auc'#'binary_logloss'#'auc'
        self.drop_date=0.15
        self.objective = "binary"
        #application = applications
        self.parameters = {
                    'boosting': self.boostring,          # dart (drop out trees) often performs better
                    'objective': self.objective,
                    #'application': applications,     # Binary classification
                    'learning_rate': self.learning_rate,       # Learning rate, controls size of a gradient descent step
                    'min_data_in_leaf': self.min_data_in_leaf,      # Data set is quite small so reduce this a bit
                    'feature_fraction': self.feature_fraction,     # Proportion of features in each boost, controls overfitting
                    'num_leaves': self.num_leaves,            # Controls size of tree since LGBM uses leaf wise splits
                    'metric': self.metric,  # Area under ROC curve as the evaulation metric
                    'drop_rate': self.drop_date   
                }
        return self.parameters

    def fit(self,train_data, test_data, parameters, batch=100):
        """
        学習を行う
        parameters
        ----------
        train_data:
            学習用trainデータ
        test_data:
            学習用testデータ
        batch : int
            学習回数
            初期値は100
        """
        self.evaluation_results = {}
        self.model=lgb.train(self.parameters,
                        self.train_data,
                        valid_sets=[self.train_data, self.test_data], 
                        valid_names=['Train', 'Test'],
                        evals_result = self.evaluation_results,
                        num_boost_round=batch,
                        early_stopping_rounds=50,
                        verbose_eval=20)
        return self.model,self.evaluation_results

    
    


    





#train_data=train_data(X_train, y_train,lgb)
        

# route_name = "taketomi_route"
# dep = "isigaki_dep"
# days_ago = 0
# test = Value_learn(route_name,dep,days_ago)
# X,y,df = test.df_load(route_name,dep,days_ago)
# print(X)
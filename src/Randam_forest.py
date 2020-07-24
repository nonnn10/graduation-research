from sklearn import datasets
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler        #標準化
from sklearn.metrics import precision_score, recall_score, f1_score     #混同行列


def main(dep_port = "isigaki", route = "hateruma_route", dates = "2017-01-*"):
    df = pd.read_csv('../data/data_2017/'+route+'_'+dep_port+"_"+dates+".csv", header=0,index_col=0)
    #print(df)
    #データのロード
    X = df.loc[:, ["wind_speed","MeWaveHight","MeWaveCyc","dire_wave"]].values
    #print(X)
    y = df.loc[:, "label"].values



    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=1, stratify=y)
    print('Labels counts in y[0 1]:', np.bincount(y))
    print('Labels counts in y_train[0 1]:', np.bincount(y_train))
    print('Labels counts in y_test[0 1]:', np.bincount(y_test))
    #print(type(X_train))
    #print(y)

    X_train_std,X_test_std = sta_sca(X_train, X_test)

    forest = random_exe(X_train,X_test,y_train,y_test)
    forest_std = random_exe(X_train_std,X_test_std,y_train,y_test)

    pred(forest,X_test,y_test)
    print("標準化処理をした正解率")
    y_pred = pred(forest_std,X_test_std,y_test)
    conf_proces(y_test,y_pred)

def route_classifier_roup(dates="2017"):
    """
    航路×出発港の数だけ分類器を学習テストデータで予測

    parameters
    ー--------
    dates : str
        データの入っているファイルの名前(日付)
    """
    route = {
        "taketomi_route": ["isigaki","taketomi"],
        "hateruma_route": ["isigaki","hateruma"],
        "kurosima_route": ["isigaki","kurosima"],
        "iriomote_ohara_route": ["isigaki","ohara"],
        "iriomote_uehara_route": ["isigaki","uehara"],
        "hatoma_route": ["isigaki","hatoma"],
        "kohama_route": ["isigaki","kohama"]
        }
    #main関数が航路数×出発港の数だけ実行し予測正解率出力
    for key, value in route.items():
        for i in range(len(value)):
            print(key+"/"+value[i]+"_dep")
            main(dep_port = value[i], route = key, dates = dates)

def sta_sca(X_train, X_test):      #標準化
    """
    標準化処理

    parameters
    ----------
    X_train : numpy.ndarray
        学習用の説明変数
    X_test : numpy.ndarray
        テスト用の説明変数

    return
    ------
    X_train_std : numpy.ndarray
        学習用の説明変数に標準化処理を行ったもの
    X_test_std : numpy.ndarray
        テスト用の説明変数に標準化処理を行ったもの
    """
    sc = StandardScaler()
    sc.fit(X_train)
    X_train_std = sc.transform(X_train)
    X_test_std = sc.transform(X_test)
    #print(X_train_std)

    return X_train_std,X_test_std
    
def random_exe(X_train,X_test,y_train,y_test):
    """
    ランダムフォレスを実行する関数

    parameters
    ----------
    X_train : numpy.ndarray
        学習用の説明変数
    X_test : numpy.ndarray
        テスト用の説明変数
    y_train : numpy.ndarray
        学習用の目的変数
    y_test : numpy.ndarray
        テスト用の目的変数

    return
    forest : sklearn.ensemble._forest.RandomForestClassifier
        ランダムフォレストの分類機インスタンス
    """
    #ランダムフォレスト実行

    forest = RandomForestClassifier(criterion='gini',
                                    n_estimators=25, 
                                    random_state=1,
                                    n_jobs=2)
    forest.fit(X_train, y_train)

    return forest
    # X_combined = np.vstack((X_train, X_test))#結合しているのはテストデータをランダムに取得したため
    # y_combined = np.hstack((y_train, y_test))

    # plot_decision_regions(X_combined, y_combined, 
    #                     classifier=forest, test_idx=range(3798, 4748))

    # plt.xlabel('wind speed [standardized]')
    # plt.ylabel('Wave height [standardized]')
    # plt.legend(loc='upper left')
    # plt.tight_layout()
    # #plt.savefig('images/03_22.png', dpi=300)
    # plt.show()

def pred(forest,X_test,y_test):
    """
    テストデータを使用して予測した正解率を出力
    
    parameters
    forst : sklearn.ensemble._forest.RandomForestClassifier
        分類機
    X_test : numpy.ndarray
        テスト用の説明変数
    y_test : numpy.ndarray
        テスト用の目的変数
    
    return
    ------
    y_pred : numpy.ndarray
        予測したlabel
    """
    y_pred = forest.predict(X_test)
    print('Test Accuracy: %.3f' % forest.score(X_test, y_test))

    return y_pred

def conf_proces(y_test,y_pred):
    """
    混同行列の出力

    parameters
    ----------
    y_test : numpy.ndarray
        テスト用の目的変数
    y_pred : numpy.ndarray
        テストデータの予測label
    """
    print('Precision: %.3f' % precision_score(y_true=y_test, y_pred=y_pred))
    print('Recall: %.3f' % recall_score(y_true=y_test, y_pred=y_pred))
    print('F1: %.3f' % f1_score(y_true=y_test, y_pred=y_pred))


if __name__ == "__main__":
    route_classifier_roup(dates="2017")
    #main()
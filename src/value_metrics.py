import os
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
import sklearn.metrics as metrics
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
#日付取得
import datetime as dt

from windy_image_scrap import create_date_dir

class Value_metrics:
    def __init__(self,model,y_test,X_test,y_train,X_train,path_metrics,conf_path):
        self.model = model
        self.y_test = y_test
        self.X_test = X_test
        self.y_train = y_train
        self.X_train = X_train
        self.path_w = path_metrics
        self.conf_path = conf_path

    @staticmethod
    def create_date_dir(dir_pass,atribute="",date=True):
        """
        画像を取得した日付のディレクトリを作成
        日付ディレクトリの下に風速、波高ディレクトリ
        そのディレクトリに取得した画像を保存

        parameters
        ----------
        dir_pass : str
            固定のディレクトリ、日付ディレクトリの上層
        atribute : str
            風、波のいずれか
        date : bool
            日付をディレクトリに含めない時
        """

        atribute = "/"+atribute
        now_date = dt.datetime.now().strftime('%Y-%m-%d')   #日付の取得(2020-07-26)  
        #ディレクトリ作成
        dir_pass = dir_pass+"/"+now_date    #ディレクトリパス最後にatributeを追加
        dir_list = dir_pass.split("/")  #ディレクトリパスを"/"で分割
        dir_list.remove("")             #dir_listの中に""がある場合は削除
        for i in range(0,len(dir_list)):#ディレクトリ階層の数だけループ,最初に../がある想定
            i += 1
            #print("/".join(dir_list[0:i]))
            if not os.path.exists("/"+"/".join(dir_list[0:i])):             #ディレクトリ階層が存在するかチェック
                #print("not exist")
                os.makedirs("/"+"/".join(dir_list[0:i]), exist_ok=True)     #存在しないなら作成
    
        return now_date


    #予測を行う
    def predict(self,model,X_test):
        """
        予測を行う
        parameters
        ----------
        X_test : array
            予測をしたいデータ
        
        return
        ------
        y_pred : list
            テストデータの予測結果(0:運航,1:欠航)
        y_pred_train : list
            トレーニングデータの予測結果(0:運航,1:欠航)
        """
        #model.predict(X_test)
        self.y_pred_proba = self.model.predict(self.X_test)
        #print(y_pred_proba)
        self.y_pred = [0 if i < 0.5 else 1 for i in self.y_pred_proba]
        #print(self.y_pred)
        self.y_train_proba = self.model.predict(self.X_train)
        self.y_pred_train = [0 if i < 0.5 else 1 for i in self.y_train_proba]
        return self.y_pred,self.y_pred_train
    
    def auc_result(self,y_test,y_pred):
        """
        Area Under the Curve
        parameters
        ----------
        y_test : list
            予測に使用したデータのラベル(目的変数)
        y_pred : list
            予測結果
        """
        fpr, tpr, thresholds = metrics.roc_curve(self.y_test, self.y_pred_proba)
        self.auc = metrics.auc(fpr, tpr)
        #print("AUC",self.auc)
        return self.auc

    def confm(self,route_name,dep,days_ago):
        """
        混同行列を作成する
        parameters
        ----------
        route_name : str
            航路の名前
        dep : str
            出発港の名前
        days_ago : int
            何日前のデータセットにするか

        return
        ------
        confmat : list
            混同行列のリスト
        """
        self.confmat = confusion_matrix(y_true=self.y_test, y_pred=self.y_pred)
        

        fig, ax = plt.subplots(figsize=(2.5, 2.5))
        ax.matshow(self.confmat, cmap=plt.cm.Blues, alpha=0.3)
        for i in range(self.confmat.shape[0]):
            for j in range(self.confmat.shape[1]):
                ax.text(x=j, y=i, s=self.confmat[i, j], va='center', ha='center')

        plt.xlabel('Predicted label')
        plt.ylabel('True label')

        plt.tight_layout()

        create_date_dir(self.conf_path,atribute="",date=True)
        plt.savefig(self.conf_path+route_name+'_'+dep+'_'+str(days_ago)+'.png', dpi=300)
        #plt.show()
        #print(confmat)
        
        return self.confmat
    #confmat = confm(route_name,dep,days_ago,y_pred,y_test)
    #print(confmat)

    #適合率、再現率、F1スコア
    def metrics_score(self):
        """
        評価指標をテキストに書き出し
        parameters
        ----------

        return
        ------

        """
        self.now_data = create_date_dir(self.path_w,"")
        with open(self.path_w, mode='a') as f:
            f.writelines('Accuracy : %.3f\n' % accuracy_score(self.y_test, self.y_pred))
            f.writelines('Precision: %.3f\n' % precision_score(y_true=self.y_test, y_pred=self.y_pred))
            f.writelines('Recall: %.3f\n' % recall_score(y_true=self.y_test, y_pred=self.y_pred))
            f.writelines('F1: %.3f\n' % f1_score(y_true=self.y_test, y_pred=self.y_pred))
            f.writelines(str(self.confmat)+"\n")
            
        print(accuracy_score(self.y_test, self.y_pred))
        print('Precision: %.3f' % precision_score(y_true=self.y_test, y_pred=self.y_pred))
        print('Recall: %.3f' % recall_score(y_true=self.y_test, y_pred=self.y_pred))
        print('F1: %.3f' % f1_score(y_true=self.y_test, y_pred=self.y_pred))
        print(self.confmat)
    
    def make_pair_plot(self):
        self.X_false = pd.DataFrame(None)
        self.X_true = pd.DataFrame(None)
        for index,true,pred,setumei in zip(self.y_test.index,self.y_test,self.y_pred,self.X_test):
            #print("{}  {} {} {}".format(index,int(true),pred,setumei))
            if int(true) ^ int(pred) == True:
                setumei = np.append(setumei,true)
                setumei = np.append(setumei,pred)
                self.X_false = pd.concat([self.X_false, pd.DataFrame(setumei)],axis=1)
                #print(X_false)
                #X_false.append(setumei)
                #print("間違っているよ",int(true) ^ int(pred))
            else:
                setumei = np.append(setumei,true)
                setumei = np.append(setumei,pred)
                self.X_true = pd.concat([self.X_true, pd.DataFrame(setumei)],axis=1)
                #print("あたり",int(true) ^ int(pred))

        self.X_false = self.X_false.T
        self.X_ture = self.X_true.T

        self.X_false["pred"] = 0
        self.X_ture["pred"] = 1
        self.X_test_pred_re = pd.concat([self.X_ture,self.X_false])
        self.X_test_pred_re.reset_index(drop=True)
        self.X_test_pred_re.columns = ['max_wind', 'max_wind_dir', 'swell','swell_dir','swell_sp','time','wave_height','wave_he_dir','wind_speed','ture_label','pred_label','pred_True']
        sep_label="pred_label"
        plt.figure(figsize=(10,5))
        sns.pairplot(self.X_test_pred_re,hue=sep_label)
        plt.grid()
        plt.show()
            

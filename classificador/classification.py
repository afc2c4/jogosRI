import pandas as pd
import glob
from time import time
import operator
import re
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import recall_score, precision_score
from sklearn.feature_selection import mutual_info_classif

def info_gain(X, y, size):
    info_dict = dict(zip(X.columns, mutual_info_classif(X, y)))
    best_info_gain = sorted(info_dict.items(), key = operator.itemgetter(1), reverse = True)

    return best_info_gain[:size]



def takeDataFrames():
    files = glob.glob("data/*.csv")
    dataFrames = []
    for i in range(len(files)):
        data = pd.read_csv(files[i])
        dataFrames.append(data)
        files[i] = re.search("\w+/(\w+)\.\w+", files[i]).group(1)

    return [dataFrames, files]

def trainClassifiers():
    bayes = GaussianNB()
    dTree = DecisionTreeClassifier()
    svm = SVC()
    regression = LogisticRegression()
    mlp = MLPClassifier()

    skf = StratifiedKFold(n_splits = 10)
    classifierList = [bayes, dTree, svm, regression, mlp]
    dataFrames, data_name = takeDataFrames()

    accuracy = []
    row_name = []
    precision = []
    recall = []
    trainTime = []

    for i in range(len(dataFrames)):
        X = dataFrames[i].drop("class", axis = 1)
        y = dataFrames[i]["class"]

        for train_idx, test_idx in skf.split(X, y):
            X_train, y_train = X.iloc[train_idx], y.iloc[train_idx]
            X_test, y_test = X.iloc[test_idx], y.iloc[test_idx]
            accuracy_fold = []
            precision_fold = []
            recall_fold = []
            trainTime_fold = []
            for classifier in classifierList:
                ini = time()
                classifier.fit(X_train, y_train)
                fim = time()

                y_pred = classifier.predict(X_test)

                acc = classifier.score(X_test, y_test)
                prec = precision_score(y_test, y_pred)
                rec = recall_score(y_test, y_pred)

                accuracy_fold.append(acc)
                precision_fold.append(prec)
                recall_fold.append(rec)
                trainTime_fold.append(fim - ini)

            row_name.append(data_name[i])
            accuracy.append(accuracy_fold)
            precision.append(precision_fold)
            recall.append(recall_fold)
            trainTime.append(trainTime_fold)

    name = ["Naive_bayes", "Decision_tree", "svm", "logistic_reg", "mlp"]

    for i in range(len(classifierList)):
        data_acc = []
        data_rec = []
        data_prec = []
        data_time = []
        for accuracies in accuracy:
            data_acc.append(accuracies[i])
        for precisions in precision:
            data_prec.append(precisions[i])
        for recalls in recall:
            data_rec.append(recalls[i])
        for t in trainTime:
            data_time.append(t[i])

        dataFrame = pd.DataFrame(list(zip(data_acc, data_rec, data_prec, data_time)),
                                index = row_name,
                                columns = ["Accuracy", "Recall", "Precision", "Train time"])

        dataFrame.to_csv("classifiers_results/" + name[i] + ".csv")

def main():
    print("main")
    token = pd.read_csv("data/token.csv")
    X = token.drop("class", axis = 1)
    y = token["class"]
    #print("oi")
    #dataFrame = pd.DataFrame(columns=info_gain(X, y, 2000), )
    info_list = info_gain(X, y, 2000)
    indexes = []
    for i in range(len(info_list)):
        indexes.append(info_list[i][0])

    infogain_data = token.loc[:, indexes]
    infogain_data["class"] = y
    infogain_data.to_csv("data/info_gain.csv", index = False)
    #print(len(indexes))
    trainClassifiers()

main()

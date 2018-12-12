import pandas as pd
from sklearn import svm
from sklearn import tree
from sklearn import linear_model
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import model_selection
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import ExtraTreesClassifier

def chooseBaggingMethod(number):
    if number == 0:
        return DecisionTreeClassifier()
    elif number == 1:
        return MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
    elif number == 2:
        return svm.SVC(probability=True,kernel='linear')
    elif number == 3:
        return KNeighborsClassifier()
    elif number == 4:
        return RandomForestClassifier(n_estimators=25)

def chooseBoostingMethod(number):
    if number == 0:
        return DecisionTreeClassifier()
    elif number == 1:
        return svm.SVC(probability=True,kernel='linear')
    elif number == 2:
        return SGDClassifier(loss='hinge')
    elif number == 3:
        return ExtraTreesClassifier(n_estimators=10, n_jobs=7)
    elif number == 4:
        return RandomForestClassifier(n_estimators=35)

def generateXYLists(df, x_attributes, y_attributes):
    length = len(df[x_attributes[0]])
    x_list = []
    y_list = []
    for x in range(length):
        temp_list = []
        for attributes in x_attributes:
            temp_list.append(df[attributes].iloc[x])
        x_list.append(temp_list)

    for y in range(length):
        for attributes in y_attributes:
            y_list.append(df[attributes].iloc[y])

    return x_list, y_list

def SVMClassification(df, x_attributes, y_attributes):
    x_list, y_list = generateXYLists(df, x_attributes, y_attributes)
    clf = svm.SVC()
    clf.fit(x_list, y_list)
    return clf

#classification
def MultiLayerClassification(df, x_attributes, y_attributes):
    x_list, y_list = generateXYLists(df, x_attributes, y_attributes)
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
    clf.fit(x_list, y_list)
    return clf

#Decision tree
def DecisionTreeClassification(df, x_attributes, y_attributes):
    x_list, y_list = generateXYLists(df, x_attributes, y_attributes)
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x_list, y_list)
    return clf

#Bayes-Algorithm
def BayesianClassification(df, x_attributes, y_attributes):
    x_list, y_list = generateXYLists(df, x_attributes, y_attributes)
    reg = linear_model.BayesianRidge()
    reg.fit(x_list, y_list)
    return reg

#Bagging-Algorithm
def BaggingClassification(df, x_attributes, y_attributes, classifier):
    x_list, y_list = generateXYLists(df, x_attributes, y_attributes)
    #Change classification algorithm in here
    cart = chooseBaggingMethod(classifier)
    bagging = BaggingClassifier(base_estimator=cart, max_samples=0.6, max_features=0.5).fit(x_list, y_list)
    #bagging = BaggingClassifier(KNeighborsClassifier(),max_samples=0.5, max_features=0.5).fit(x_list, y_list)
    return bagging

#Boosting-Algorithm
def BoostingClassification(df, x_attributes, y_attributes, classifier):
    x_list, y_list = generateXYLists(df, x_attributes, y_attributes)
    cart = chooseBoostingMethod(classifier)
    if classifier == 2:
        clf = AdaBoostClassifier(base_estimator=cart, n_estimators=15, algorithm='SAMME').fit(x_list, y_list)
    else:
        clf = AdaBoostClassifier(base_estimator=cart, n_estimators=15).fit(x_list, y_list)
    return clf

#RandomForest-Algorithm
def RandomforestClassification(df, x_attributes, y_attributes):
    x_list, y_list = generateXYLists(df, x_attributes, y_attributes)
    clf = RandomForestClassifier(n_estimators=25).fit(x_list, y_list)
    return clf

#Draw a picture
def plotting(test, revenue):
    plt.plot(test, 'r-')
    plt.plot(revenue, 'b-')
    plt.show()

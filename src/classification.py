import pandas as pd
from sklearn import svm
from sklearn import tree
from sklearn import linear_model
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt

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

#Draw a picture
def plotting(test, revenue):
    plt.plot(test, 'r-')
    plt.plot(revenue, 'b-')
    plt.show()

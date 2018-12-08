import pandas as pd
from sklearn import svm

def SVMClassification(df, x_attributes, y_attributes):
    length = len(df[x_attributes[0]])
    print(length)
    x_list = []
    y_list = []
    for x in range(length):
        temp_list = []
        for attributes in x_attributes:
            temp_list.append(df[attributes][x])
        x_list.append(temp_list)
    for x in x_list:
        print(x)

    for y in range(length):
        for attributes in y_attributes:
            y_list.append(df[attributes][y])
    for y in y_list:
        print(y)

    clf = svm.SVC(gamma='scale')
    clf.fit(x_list, y_list)
    return clf

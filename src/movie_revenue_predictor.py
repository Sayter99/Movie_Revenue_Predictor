import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import preprocessing
import clustering
import classification
import sys
import math
from sklearn.model_selection import train_test_split
from utilities.instagram_data import AcquireJson
from pathlib import Path

X_Attributes = ['budget', 'actor1_hashtags', 'actor2_hashtags',
                'actor3_hashtags', 'director_hashtags', 'genre_point',
                'director_point', 'actor_point']
Y_Attributes = ['revenue']

def preprocess():
    a = AcquireJson()
    integratedCSV = Path('datasets/integrated.csv')
    integratedRefilledCSV = Path('datasets/integratedRefilled.csv')
    gpCSV = Path('datasets/gp.csv')
    preprocessed = Path('datasets/preprocessed.csv')
    if not integratedCSV.exists():
        creditsData = pd.read_csv('datasets/tmdb_5000_credits.csv')
        moviesData = pd.read_csv('datasets/tmdb_5000_movies.csv')
        mergedData = preprocessing.mergeDataFrames(creditsData, moviesData)
        # cast -> main actor/actress
        mergedData['cast'] = mergedData['cast'].apply(lambda x: preprocessing.cast2main(x))
        # crew -> director
        mergedData['crew'] = mergedData['crew'].apply(lambda x: preprocessing.crew2director(x))
        # get # of hashtags
        mergedData['actor1_hashtags'] = mergedData['cast'].apply(lambda x: a.getHashtagCounts(x.split(',')[0]))
        a.clearCache()
        mergedData['actor2_hashtags'] = mergedData['cast'].apply(lambda x: a.getHashtagCounts(x.split(',')[1]))
        a.clearCache()
        mergedData['actor3_hashtags'] = mergedData['cast'].apply(lambda x: a.getHashtagCounts(x.split(',')[2]))
        a.clearCache()
        mergedData['director_hashtags'] = mergedData['crew'].apply(lambda x: a.getHashtagCounts(x))
        a.clearCache()
        mergedData['movie_hashtags'] = mergedData['title_x'].apply(lambda x: a.getHashtagCounts(x))
        mergedData.to_csv('datasets/integrated.csv')
    if not integratedRefilledCSV.exists():
        mergedData = pd.read_csv('datasets/integrated.csv')
        mergedData['crew'] = mergedData['crew'].replace(np.nan, 'N/A')
        mergedData.to_csv('datasets/test.csv')
        mergedData.apply(lambda x: a.refillMissingTags(x), axis = 1)
        mergedData.to_csv('datasets/integratedRefilled.csv')
    if not gpCSV.exists():
        mergedData = pd.read_csv('datasets/integratedRefilled.csv')
        mergedData['genres'] = mergedData['genres'].apply(lambda x: preprocessing.genre2str(x))
        mergedData['production_companies'] = mergedData['production_companies'].apply(lambda x: preprocessing.pc2main(x))
        mergedData.to_csv('datasets/gp.csv')
    if not preprocessed.exists():
        df = pd.read_csv('datasets/gp.csv')
        df = preprocessing.dropMissingValues(df)
        genres = set(df['genres'].tolist())
        dic = {}
        for genre in genres:
            tmp = df[df['genres'] == genre]
            if tmp['budget'].sum() != 0:
                dic[genre] = tmp['revenue'].sum()/tmp['budget'].sum()
            else:
                dic[genre] = 0
        df['genre_point'] = df['genres'].apply(lambda x: dic[x])
        dic.clear()
        directors = set(df['crew'].tolist())
        for director in directors:
            tmp = df[df['crew'] == director]
            if tmp['budget'].sum() != 0:
                dic[director] = tmp['revenue'].sum()/tmp['budget'].sum()
            else:
                dic[director] = 0
        df['director_point'] = df['crew'].apply(lambda x: dic[x])
        dic.clear()
        actors = set()
        df['cast'].apply(lambda x: preprocessing.splitActors(x, actors))
        for actor in actors:
            tmp = df[df['cast'].apply(lambda x: preprocessing.containActor(x, actor)) == True]
            if tmp['budget'].sum() != 0:
                dic[actor] = tmp['revenue'].sum()/tmp['budget'].sum()
            else:
                dic[actor] = 0
        dic['N/A'] = 0
        df['actor_point'] = df['cast'].apply(lambda x: dic[x.split(',')[0]] + dic[x.split(',')[1][1:]] + dic[x.split(',')[2][1:]])
        df.iloc[:, 1:].to_csv('datasets/preprocessed.csv')

def findOutliers(df):
    # Based on the different column in array(a1, a2, genre_point......)
    X = df['director_hashtags'].values.reshape(-1, 1).tolist()
    labelList = clustering.DBSCANClustering(X, 94000, 200)
    for i in range(len(labelList)):
        if labelList[i] == -1:
            print(i)
            print(df['crew'].iloc[i])
            # print(df['cast'].iloc[i].split(',')[0]) # switch from 0, 1, 2

def generateClusteredCSV():
    preprocessed = Path('datasets/preprocessed.csv')
    clustered = Path('datasets/clustered.csv')
    if not preprocessed.exists():
        return None
    if not clustered.exists():
        # clustering all columns by kmeans clustering
        df = pd.read_csv("datasets/preprocessed.csv")
        # findOutliers(df)
        df = df[(df['id'] != 22832) & (df['id'] != 692) & (df['id'] != 14736) & (df['id'] != 238603) &
                (df['id'] != 10117) & (df['id'] != 198184) & (df['id'] != 65759) & (df['id'] != 4327) &
                (df['id'] != 59962) & (df['id'] != 11170)]
        kmeans_labels = []
        for attribute in X_Attributes:
            X = df[attribute].values.reshape(-1, 1).tolist()
            kmeans_labels.append(clustering.KMeansClustering(X, 30))
        X = df['revenue'].values.reshape(-1, 1).tolist()
        kmeans_labels.append(clustering.KMeansClustering(X, 5))
        final_df = pd.DataFrame()
        for i in range(len(X_Attributes)):
            final_df[X_Attributes[i]] = df[X_Attributes[i]]
            #final_df[X_Attributes[i]] = pd.Series(kmeans_labels[i]).values
            #final_df[X_Attributes[i]] = (df[X_Attributes[i]] - df[X_Attributes[i]].min())/(df[X_Attributes[i]].max() - df[X_Attributes[i]].min())
        final_df['revenue'] = pd.Series(kmeans_labels[-1]).values
        #final_df['revenue'] = df['revenue']
        final_df.to_csv('datasets/clustered.csv')

def classificationError(test_result, real_revenue):
    error = 0
    diff = 0
    for i in range(len(test_result)):
        if test_result[i] != real_revenue[i]:
            error = error + 1
            diff = diff + abs(test_result[i] - real_revenue[i])
    print("errors: " + str(error))
    print("total: " + str(len(test_result)))
    print("diff: " + str(diff))
    return error, len(test_result), diff

def rmseError(test_result, real_revenue):
    diff = 0
    for i in range(len(test_result)):
        if test_result[i] != real_revenue[i]:
            diff = diff + (test_result[i] - real_revenue[i])*(test_result[i] - real_revenue[i])
    return math.sqrt(diff/len(test_result))/(max(real_revenue) - min(real_revenue))

def trainAndTest(df, method, plotting, eval):
    train, test = train_test_split(df, test_size=0.08)
    if method == 0: # single classifier
        classifier = classification.RandomforestClassification(train, X_Attributes, Y_Attributes)
        test_list, real_revenue = classification.generateXYLists(test, X_Attributes, Y_Attributes)
        test_result = classifier.predict(test_list)
        if plotting == True:
            classification.plotting(test_result, real_revenue)
        if eval == 0:
            return classificationError(test_result, real_revenue)
        else:
            return rmseError(test_result, real_revenue)
    elif method == 1: # boosting or bagging
        classifier = classification.BoostingClassification(train, X_Attributes, Y_Attributes, 4)
        test_list, real_revenue = classification.generateXYLists(test, X_Attributes, Y_Attributes)
        test_result = classifier.predict(test_list)
        if plotting == True:
            classification.plotting(test_result, real_revenue)
        if eval == 0:
            return classificationError(test_result, real_revenue)
        else:
            return rmseError(test_result, real_revenue)
    
def classificationTest(test_times, classification_method, plotting, evaluation_method):
    # err, total, diff = trainAndTest(df, 1, True)
    df = pd.read_csv('datasets/clustered.csv')
    err_t = 0
    diff_t = 0
    total = 0
    for i in range(test_times):
        err, total, diff = trainAndTest(df, classification_method, plotting, evaluation_method)
        err_t = err_t + err
        diff_t = diff_t + diff
    print('avg correctness: ' + str(((total - (err_t/test_times))/total)))
    print('avg diff: ' + str((diff_t/test_times/total)))

def RMSETest(test_times, classification_method, plotting, evaluation_method):
    df = pd.read_csv('datasets/noclustered.csv')
    err_t = 0
    for i in range(test_times):
        rmse = trainAndTest(df, classification_method, plotting, evaluation_method)
        err_t = err_t + rmse
    print('RMSE: ' + str(err_t/test_times))

classification_method = 1 # boosting
plotting = False # don't plot results
evaluation_method = 0 # class
test_times = 1

preprocess()
generateClusteredCSV()
classificationTest(test_times, classification_method, plotting, evaluation_method)

evaluation_method = 1 # RMSE
RMSETest(test_times, classification_method, plotting, evaluation_method)
import json
import numpy as np
import pandas as pd

def mergeDataFrames(credits, movies):
    # merge two csv files
    mergedData = movies.merge(credits, left_on='id', right_on='movie_id', how='inner')
    return mergedData

def dropMissingValues(mergedData):
    # drop missing values
    mergedData = mergedData[(mergedData['budget'] != 0) & (mergedData['revenue'] != 0)]
    return mergedData

def dropMissingValues2(mergedData):
    # drop missing values
    mergedData.fillna('0')
    mergedData = mergedData[(mergedData['budgets'] != 'No Budget') &
                            (mergedData['budgets'] != 'No Budget Information') &
                            (mergedData['budgets'] != '0') &
                            (mergedData['gross_usa'] != 'Not Found in OMDB') &
                            (mergedData['gross_usa'] != 'No Gross Revenue') &
                            (mergedData['gross_usa'] != '0') &
                            (pd.notna(mergedData['gross_usa']))]
    mergedData['budgets'] = mergedData['budgets'].apply(lambda x: int(x))
    mergedData['gross_usa'] = mergedData['gross_usa'].apply(lambda x: int(x))
    return mergedData

def splitActors(x, actors):
    tmp = x.split(',')
    for i in range(len(tmp)):
        if 'N/A' not in tmp[i]:
            if tmp[i][0] == ' ':
                actors.add(tmp[i][1:])
            else:
                actors.add(tmp[i])

def containActor(x, actor):
    return actor in x

def autofill(mergedData, method):
    pass

def cast2main(s):
    cast = json.loads(s)
    if len(cast) >= 3:
        first = cast[0]['name']
        second = cast[1]['name']
        third = cast[2]['name']
        res = first + ', ' + second + ', ' + third
    elif len(cast) >= 2:
        first = cast[0]['name']
        second = cast[1]['name']
        res = first + ', ' + second + ', ' + 'N/A'
    elif len(cast) >= 1:
        first = cast[0]['name']
        res = first + ', N/A, N/A'
    else:
        res = 'N/A, N/A, N/A'
    return res

def crew2director(s):
    cast = json.loads(s)
    res = 'N/A'
    for i in cast:
        if i['job'] == 'Director':
            res = i['name']
            break
    return res

def genre2str(s):
    genre = json.loads(s)
    min = 999999
    res = 'N/A'
    for i in genre:
        if int(i['id']) < min:
            res = i['name']
    if res == 'N/A':
        print('WARNING: Failed to find out the primary genre')
    return res

def pc2main(s):
    pc = json.loads(s)
    res = 'N/A'
    if len(pc) >= 3:
        first = pc[0]['name']
        second = pc[1]['name']
        third = pc[2]['name']
        res = first + ', ' + second + ', ' + third
    elif len(pc) >= 2:
        first = pc[0]['name']
        second = pc[1]['name']
        res = first + ', ' + second
    elif len(pc) >= 1:
        first = pc[0]['name']
        res = first
    else:
        res = 'N/A'
    return res
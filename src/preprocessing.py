import json

def mergeDataFrames(credits, movies):
    # merge two csv files
    mergedData = movies.merge(credits, left_on='id', right_on='movie_id', how='inner')
    return mergedData

def dropMissingValues(mergedData):
    # drop missing values
    mergedData = mergedData[(mergedData['budget'] != 0) & (mergedData['revenue'] != 0)]
    return mergedData

def autofill(mergedData, method):
    pass

def cast2main(s):
    cast = json.loads(s)
    if len(cast) >= 2:
        first = cast[0]['name']
        second = cast[1]['name']
        res = first + ', ' + second
    elif len(cast) >= 1:
        first = cast[0]['name']
        res = first
    else:
        res = 'N/A'
    return res

def crew2director(s):
    cast = json.loads(s)
    res = 'N/A'
    for i in cast:
        if i['job'] == 'Director':
            res = i['name']
            break
    return res
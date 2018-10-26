import json

def mergeAndTrim(credits, movies):
    # merge two csv files
    mergedData = movies.merge(credits, left_on='id', right_on='movie_id', how='inner')
    # deal with missing values
    mergedData = mergedData[(mergedData['budget'] != 0) & (mergedData['revenue'] != 0)]
    return mergedData

def cast2main(mergedData):
    main = []
    for i in mergedData.index.values:
        cast = json.loads(mergedData.ix[i]['cast'])
        if len(cast) >= 2:
            first = cast[0]['name']
            second = cast[1]['name']
            main.append(first + ', ' + second)
        elif len(cast) >= 1:
            main.append(first)
        else:
            main.append('N/A')
    mergedData['main'] = main
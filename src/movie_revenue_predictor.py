import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import preprocessing
import sys
from utilities.instagram_data import AcquireJson
from pathlib import Path

a = AcquireJson()
integratedCSV = Path('datasets/integrated.csv')
integratedRefilledCSV = Path('datasets/integratedRefilled.csv')
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
elif not integratedRefilledCSV.exists():
    mergedData = pd.read_csv('datasets/integrated.csv')
    mergedData['crew'] = mergedData['crew'].replace(np.nan, 'N/A')
    mergedData.to_csv('datasets/test.csv')
    mergedData.apply(lambda x: a.refillMissingTags(x), axis = 1)
    mergedData.to_csv('datasets/integratedRefilled.csv')
else:
    pass
# deal with missing values
#####mergedData = preprocessing.dropMissingValues(mergedData)
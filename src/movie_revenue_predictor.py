import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import preprocessing
import sys
from utilities.instagram_data import AcquireJson
#import utilities.instagram_data as instagram

creditsData = pd.read_csv('datasets/tmdb_5000_credits.csv')
moviesData = pd.read_csv('datasets/tmdb_5000_movies.csv')
mergedData = preprocessing.mergeDataFrames(creditsData, moviesData)
# cast -> main actor/actress
mergedData['cast'] = mergedData['cast'].apply(lambda x: preprocessing.cast2main(x))
# crew -> director
mergedData['crew'] = mergedData['crew'].apply(lambda x: preprocessing.crew2director(x))
# get # of hashtags
a = AcquireJson()
mergedData['actor1_hashtags'] = mergedData['cast'].apply(lambda x: a.getHashtagCounts(x.split(',')[0]))
a.clearCache()
mergedData['actor2_hashtags'] = mergedData['cast'].apply(lambda x: a.getHashtagCounts(x.split(',')[1]))
a.clearCache()
mergedData['actor3_hashtags'] = mergedData['cast'].apply(lambda x: a.getHashtagCounts(x.split(',')[2]))
a.clearCache()
mergedData['director_hashtags'] = mergedData['crew'].apply(lambda x: a.getHashtagCounts(x))
a.clearCache()
mergedData['movie_hashtags'] = mergedData['title_x'].apply(lambda x: a.getHashtagCounts(x))
mergedData.to_csv('datasets/merged.csv')
# deal with missing values
#####mergedData = preprocessing.dropMissingValues(mergedData)
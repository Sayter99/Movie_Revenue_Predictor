import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import preprocessing
import sys
import utilities.instagram_data as instagram

creditsData = pd.read_csv('datasets/tmdb_5000_credits.csv')
moviesData = pd.read_csv('datasets/tmdb_5000_movies.csv')
mergedData = preprocessing.mergeDataFrames(creditsData, moviesData)
# deal with missing values
mergedData = preprocessing.dropMissingValues(mergedData)
# cast -> main actor/actress
mergedData['cast'] = mergedData['cast'].apply(lambda x: preprocessing.cast2main(x))
# crew -> director
mergedData['crew'] = mergedData['crew'].apply(lambda x: preprocessing.crew2director(x))
# get # of hashtags
mergedData['actor_hashtags'] = mergedData['cast'].apply(lambda x: instagram.getHashtagCounts(x.split(',')[0]))
mergedData['actress_hashtags'] = mergedData['cast'].apply(lambda x: instagram.getHashtagCounts(x.split(',')[1]))
mergedData['director_hashtags'] = mergedData['crew'].apply(lambda x: instagram.getHashtagCounts(x))
mergedData.to_csv('test.csv')
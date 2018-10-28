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
# mergedData.to_csv('test.csv')
preprocessing.cast2main(mergedData)
test = str(mergedData['main'][0]).split(',')
for a in test:
    instagram.getHashtagCounts(a)
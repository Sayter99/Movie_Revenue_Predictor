import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import preprocessing

creditsData = pd.read_csv('datasets/tmdb_5000_credits.csv')
moviesData = pd.read_csv('datasets/tmdb_5000_movies.csv')
mergedData = preprocessing.mergeAndTrim(creditsData, moviesData)
# mergedData.to_csv('test.csv')
preprocessing.cast2main(mergedData)
print(mergedData['main'].head())
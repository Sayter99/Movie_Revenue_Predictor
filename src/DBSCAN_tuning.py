import matplotlib
matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import preprocessing
import clustering
import sys
from utilities.instagram_data import AcquireJson
from pathlib import Path
import csv 

df = pd.read_csv("datasets/preprocessed.csv")
# Based on the different column in array(a1, a2, genre_point......)

# all_columns = ['genre_point', 'director_point', 'actor_point']

### old test
# all_columns = ['actor_point', 'actor1_hashtags', 'actor2_hashtags', 'actor3_hashtags', 'director_hashtags', 'movie_hashtags IMDB_ID']
# number_of_lalala = 8
# number_of_radius = 48

# all_radius = [round(x * 0.01 + 0.05, 2) for x in range(0, number_of_radius + 1)]
# all_lalala = [x * 50 + 200 for x in range(0, number_of_lalala + 1)]

### New test - 1
# all_columns = ['actor1_hashtags', 'actor2_hashtags', 'actor3_hashtags', 'director_hashtags']
# number_of_lalala = 8
# number_of_radius = 45

# all_radius = [round(x * 2000 + 10000, 2) for x in range(0, number_of_radius + 1)]
# all_lalala = [x * 50 + 200 for x in range(0, number_of_lalala + 1)]

### New test - 2
# all_columns = ['actor1_hashtags', 'actor2_hashtags', 'actor3_hashtags']
# number_of_lalala = 8
# number_of_radius = 10

# all_radius = [round(x * 10000 + 200000, 2) for x in range(0, number_of_radius + 1)]
# all_lalala = [x * 50 + 200 for x in range(0, number_of_lalala + 1)]

### New test - 3
# all_columns = ['actor1_hashtags']
# number_of_lalala = 8
# number_of_radius = 10

# all_radius = [round(x * 10000 + 500000, 2) for x in range(0, number_of_radius + 1)]
# all_lalala = [x * 50 + 200 for x in range(0, number_of_lalala + 1)]

### New test - 4
# all_columns = ['actor1_hashtags']
# number_of_lalala = 8
# number_of_radius = 20

# all_radius = [round(x * 10000 + 600000, 2) for x in range(0, number_of_radius + 1)]
# all_lalala = [x * 50 + 200 for x in range(0, number_of_lalala + 1)]

### New test - 5
# all_columns = ['actor2_hashtags', 'actor3_hashtags']
# number_of_lalala = 8
# number_of_radius = 8

# all_radius = [round(x * 50000 + 300000, 2) for x in range(0, number_of_radius + 1)]
# all_lalala = [x * 50 + 200 for x in range(0, number_of_lalala + 1)]


###### New test - 5.1
# all_columns = ['actor_point']
# number_of_lalala = 8
# number_of_radius = 9

# all_radius = [round(x * 0.1 + 0.6, 2) for x in range(0, number_of_radius + 1)]
# all_lalala = [x * 50 + 200 for x in range(0, number_of_lalala + 1)]

###### New test - 5.2
# all_columns = ['director_point']
# number_of_lalala = 8
# number_of_radius = 5

# all_radius = [round(x * 0.05 + 0.55, 2) for x in range(0, number_of_radius + 1)]
# all_lalala = [x * 50 + 200 for x in range(0, number_of_lalala + 1)]


###### New test - 6.1
# all_columns = ['actor_point']
# number_of_lalala = 8
# number_of_radius = 13

# all_radius = [round(x * 0.2 + 1.5, 2) for x in range(0, number_of_radius + 1)]
# all_lalala = [x * 50 + 200 for x in range(0, number_of_lalala + 1)]

###### New test - 6.2
# all_columns = ['director_point']
# number_of_lalala = 8
# number_of_radius = 7

# all_radius = [round(x * 0.1 + 0.8, 2) for x in range(0, number_of_radius + 1)]
# all_lalala = [x * 50 + 200 for x in range(0, number_of_lalala + 1)]


###### New test - 7.1
# all_columns = ['actor_point']
# number_of_lalala = 8
# number_of_radius = 20

# all_radius = [round(x * 0.1 + 4, 2) for x in range(0, number_of_radius + 1)]
# all_lalala = [x * 50 + 200 for x in range(0, number_of_lalala + 1)]

###### New test - 7.2
# all_columns = ['director_point']
# number_of_lalala = 8
# number_of_radius = 15

# all_radius = [round(x * 0.1 + 1.5, 2) for x in range(0, number_of_radius + 1)]
# all_lalala = [x * 50 + 200 for x in range(0, number_of_lalala + 1)]

###### New test - 7.1
all_columns = ['actor_point']
number_of_lalala = 8
number_of_radius = 10

all_radius = [round(x * 1 + 20, 2) for x in range(0, number_of_radius + 1)]
all_lalala = [x * 50 + 200 for x in range(0, number_of_lalala + 1)]

for each_column in all_columns:
    X = df[each_column].values.reshape(-1, 1).tolist()
    output = []
    output.append(['number of clusters', 'number of noise points', 'radius', 'lalala'])
    for each_radius in all_radius:
        for each_lalala in all_lalala:
            n_clusters_, n_noise_ = clustering.DBSCANClustering(X, each_radius, each_lalala, each_column)
            output.append([n_clusters_, n_noise_, each_radius, each_lalala])
    
    with open(str(each_column) + '.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(output)

    csvFile.close()

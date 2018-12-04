import pandas as pd
from sklearn.cluster import DBSCAN

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


df = pd.read_csv("./preprocessed.csv")

# Based on the different column in array(a1, a2, genre_point......)
X = df['genre_point'].values.reshape(-1, 1).tolist()

clustering = DBSCAN(eps=0.05, min_samples=200).fit(X)
labels = clustering.labels_

# Based on the size of clusters to set the labels[x] value, if cluster = 4, labels = -1 ~ 3, if cluster = 4,
# labels = -1 ~ 4......

for x in range(len(X)):
    if labels[x] == 0:
        plt.plot(X[x], 0, 'go')
    elif labels[x] == 1:
        plt.plot(X[x], 0, 'bo')
    elif labels[x] == -1:
        plt.plot(X[x], 0, 'ro')
    elif labels[x] == 2:
        plt.plot(X[x], 0, 'mo')
    else:
        plt.plot(X[x], 0, 'ko')

plt.interactive(False)
plt.savefig('foo.png')
plt.close()
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)

# Black removed and is used for noise instead.



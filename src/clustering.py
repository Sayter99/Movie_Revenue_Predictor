import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt

def DBSCANClustering(X, peps, pmin_sample):
    clustering = DBSCAN(eps=peps, min_samples=pmin_sample).fit(X)
    labels = clustering.labels_

    # Based on the size of clusters to set the labels[x] value, if cluster = 4, labels = -1 ~ 3, if cluster = 4,
    # labels = -1 ~ 4......

    for x in range(len(X)):
        color = 'C' + str(8-labels[x])
        plt.plot(X[x], 0, color=color, marker='o')
        #if labels[x] == 0:
        #    plt.plot(X[x], 0, 'go')
        #elif labels[x] == 1:
        #    plt.plot(X[x], 0, 'bo')
        #elif labels[x] == -1:
        #    plt.plot(X[x], 0, 'ro')
        #elif labels[x] == 2:
        #    plt.plot(X[x], 0, 'mo')
        #else:
        #    plt.plot(X[x], 0, 'ko')

    #plt.interactive(False)
    #plt.savefig('foo.png')
    #plt.close()
    plt.show()
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    print('Estimated number of clusters: %d' % n_clusters_)
    print('Estimated number of noise points: %d' % n_noise_)

def KMeansClustering(X, clusters):
    kmeans = KMeans(n_clusters=clusters)
    kmeans = kmeans.fit(X)
    labels = kmeans.predict(X)
    #centroids = kmeans.cluster_centers_
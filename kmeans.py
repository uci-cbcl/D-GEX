#!/usr/bin/env python
    
import sys
    
import numpy as np
from sklearn.cluster import MiniBatchKMeans

BGEDV2_DATA = 'bgedv2_float64.npy'

def main():
    data = np.load(BGEDV2_DATA)
    X = data.transpose()
    X_rand = X[np.random.permutation(129158), :]
    
    km = MiniBatchKMeans(n_clusters=100, max_iter=10, batch_size=1000, verbose=1, compute_labels=False)
    km.fit(X_rand)
    label = km.predict(X)
    
    outfile = open('bgedv2_kmeans_100_label.txt', 'w')
    
    for l in label:
        outfile.write(str(l) + '\n')
    
    outfile.close()
    

    
        
if __name__ == '__main__':
    main()
    
    
    
    
    
    

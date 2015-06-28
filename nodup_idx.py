#!/usr/bin/env python
    
import sys
    
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances

BGEDV2_DATA = 'bgedv2_float64.npy'
LABEL = 'bgedv2_kmeans_100_label.txt'
K = 100
D_THRED = 1.0

def keep(pd_k, idx_k):
    n_k = pd_k.shape[0]
    I, J = np.where(pd_k < D_THRED)
    set_k = set(range(0, n_k))
    
    for i in range(0, I.size):
        idx_i = I[i]
        idx_j = J[i]
        if idx_i >= idx_j:
            continue
        
        if idx_j in set_k:
            set_k.remove(idx_j)
        
    return idx_k[list(set_k)]
    

def main():
    data = np.load(BGEDV2_DATA)
    X = data.transpose()
    
    inlabel = open(LABEL)
    label = []
    for line in inlabel:
        label.append(int(line.strip('\n')))
    
    label = np.array(label)
    inlabel.close()
    
    idx_keep = []
    for k in range(0, K):
        print k
        sys.stdout.flush()
        idx_k = np.where(label == k)[0]
        X_k = X[idx_k, :]
        pd_k = pairwise_distances(X_k, metric='euclidean', n_jobs=10)
        idx_k_keep = keep(pd_k, idx_k)
        idx_keep.extend(idx_k_keep.tolist())
        
    idx_keep = np.sort(np.array(idx_keep)).astype('int')
    
    outfile = open('bgedv2_idx_nodup_K100_D1.0.txt', 'w')
    for idx in idx_keep:
        outfile.write(str(idx) + '\n')
    
    outfile.close()

    

    
        
if __name__ == '__main__':
    main()
    
    
    
    
    
    

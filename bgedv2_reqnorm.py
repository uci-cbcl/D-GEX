#!/usr/bin/env python

import sys

import numpy as np
from scipy import stats

def main():
    data = np.load('bgedv2_GTEx_1000G_float64.npy')
    
    data_sorted = np.zeros(data.shape)
    data_reqnorm = np.zeros(data.shape)
    idx_rank = np.zeros(data.shape, dtype='int')

    
    for i in range(0, data.shape[1]):
        data_sorted[:, i] = np.sort(data[:, i])
        idx_rank[:, i] = (stats.rankdata(data[:, i]) - 1).astype('int')
    
    quantile = data_sorted.mean(axis=1)
    
    for i in range(0, data.shape[1]):
        data_reqnorm[:, i] = quantile[idx_rank[:, i]]
    
    np.save('bgedv2_GTEx_1000G_reqnorm_float64.npy', data_reqnorm)
    np.save('bgedv2_GTEx_1000G_quantile_float64.npy', quantile)
    


   
        
if __name__ == '__main__':
    main()
    
    
    
    
    
    

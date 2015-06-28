#!/usr/bin/env python

import sys

import numpy as np

def main():
    data = np.load('1000G_float64.npy')
    quantile = np.load('bgedv2_GTEx_1000G_quantile_float64.npy')
    
    data_reqnorm = np.zeros(data.shape)
    
    for i in range(0, data.shape[1]):
        print '%s/%s' % (i, data.shape[1])
        sys.stdout.flush()
        data_uniq_i = np.unique(data[:, i]).tolist()
        idx_rank_RNASeq = np.array(map(data_uniq_i.index, data[:, i]))
        idx_pos_RNASeq = (idx_rank_RNASeq+1.0)/len(data_uniq_i)
        idx_rank_bgedv2 = (idx_pos_RNASeq*data.shape[0]).astype('int')-1
        data_reqnorm[:, i] = quantile[idx_rank_bgedv2]
        
    
    
    np.save('1000G_reqnorm_float64.npy', data_reqnorm)
    


   
        
if __name__ == '__main__':
    main()
    
    
    
    
    
    

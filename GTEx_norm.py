#!/usr/bin/env python

import numpy as np

def main():
    data = np.load('GTEx_reqnorm_float64.npy')
    data_means = data.mean(axis=1)
    data_stds = data.std(axis=1) + 1e-3
    data = (data - data_means.reshape((10463, 1)))/data_stds.reshape((10463, 1))
    
    X, Y = data[:943, :].transpose(), data[943:, :].transpose()

    np.save('GTEx_X_float64.npy', X)
    np.save('GTEx_Y_float64.npy', Y)

    np.save('GTEx_Y_0-4760_float64.npy', Y[:, 0:4760])
    np.save('GTEx_Y_4760-9520_float64.npy', Y[:, 4760:9520])
    
        
if __name__ == '__main__':
    main()


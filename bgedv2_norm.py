#!/usr/bin/env python

import numpy as np

def main():
    data = np.load('bgedv2_GTEx_1000G_reqnorm_float64.npy')
    data_means = data.mean(axis=1)
    data_stds = data.std(axis=1) + 1e-3
    data = (data - data_means.reshape((10463, 1)))/data_stds.reshape((10463, 1))
    
    data_tr = data[:, :88807]
    data_va = data[:, 88807:99908]
    data_te = data[:, 99908:]
    
    X_tr, Y_tr = data_tr[:943, :].transpose(), data_tr[943:, :].transpose()
    X_va, Y_va = data_va[:943, :].transpose(), data_va[943:, :].transpose()
    X_te, Y_te = data_te[:943, :].transpose(), data_te[943:, :].transpose()
    
    np.save('bgedv2_X_tr_float64.npy', X_tr)
    np.save('bgedv2_X_va_float64.npy', X_va)
    np.save('bgedv2_X_te_float64.npy', X_te)
    np.save('bgedv2_Y_tr_float64.npy', Y_tr)
    np.save('bgedv2_Y_va_float64.npy', Y_va)
    np.save('bgedv2_Y_te_float64.npy', Y_te)

    np.save('bgedv2_Y_tr_0-4760_float64.npy', Y_tr[:, 0:4760])
    np.save('bgedv2_Y_tr_4760-9520_float64.npy', Y_tr[:, 4760:9520])

    np.save('bgedv2_Y_va_0-4760_float64.npy', Y_va[:, 0:4760])
    np.save('bgedv2_Y_va_4760-9520_float64.npy', Y_va[:, 4760:9520])

    np.save('bgedv2_Y_te_0-4760_float64.npy', Y_te[:, 0:4760])
    np.save('bgedv2_Y_te_4760-9520_float64.npy', Y_te[:, 4760:9520])
    
        
if __name__ == '__main__':
    main()


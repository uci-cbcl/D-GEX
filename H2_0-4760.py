#!/usr/bin/env python

import sys
import os
import pickle as pkl
import time
import random

import numpy as np
import theano.tensor as T
import theano
import pylearn2.train
import pylearn2.models.mlp as p2_md_mlp
import pylearn2.datasets.dense_design_matrix as p2_dt_dd
import pylearn2.training_algorithms.sgd as p2_alg_sgd
import pylearn2.training_algorithms.learning_rule as p2_alg_lr
import pylearn2.costs.mlp.dropout as p2_ct_mlp_dropout
import pylearn2.termination_criteria as p2_termcri
from numpy import dtype


def main():
    base_name = sys.argv[1]
    n_epoch = int(sys.argv[2])
    n_hidden = int(sys.argv[3])
    include_rate = float(sys.argv[4])

    in_size = 943
    out_size = 4760
    b_size = 200
    l_rate = 3e-4
    l_rate_min = 1e-5
    decay_factor = 0.9
    lr_scale = 3.0
    momentum = 0.5
    init_vals = np.sqrt(6.0/(np.array([in_size, n_hidden, n_hidden])+np.array([n_hidden, n_hidden, out_size])))
    
    print 'loading data...'
    
    X_tr = np.load('bgedv2_X_tr_float64.npy')
    Y_tr = np.load('bgedv2_Y_tr_0-4760_float64.npy')
    Y_tr_target = np.array(Y_tr)
    X_va = np.load('bgedv2_X_va_float64.npy')
    Y_va = np.load('bgedv2_Y_va_0-4760_float64.npy')
    Y_va_target = np.array(Y_va)
    X_te = np.load('bgedv2_X_te_float64.npy')
    Y_te = np.load('bgedv2_Y_te_0-4760_float64.npy')
    Y_te_target = np.array(Y_te)

    X_1000G = np.load('1000G_X_float64.npy')
    Y_1000G = np.load('1000G_Y_0-4760_float64.npy')
    Y_1000G_target = np.array(Y_1000G)
    X_GTEx = np.load('GTEx_X_float64.npy')
    Y_GTEx = np.load('GTEx_Y_0-4760_float64.npy')
    Y_GTEx_target = np.array(Y_GTEx)

    
    random.seed(0)
    monitor_idx_tr = random.sample(range(88807), 5000)
    
    data_tr = p2_dt_dd.DenseDesignMatrix(X=X_tr.astype('float32'), y=Y_tr.astype('float32'))
    X_tr_monitor, Y_tr_monitor_target = X_tr[monitor_idx_tr, :], Y_tr_target[monitor_idx_tr, :]
    h1_layer = p2_md_mlp.Tanh(layer_name='h1', dim=n_hidden, irange=init_vals[0], W_lr_scale=1.0, b_lr_scale=1.0)
    h2_layer = p2_md_mlp.Tanh(layer_name='h2', dim=n_hidden, irange=init_vals[1], W_lr_scale=lr_scale, b_lr_scale=1.0)
    o_layer = p2_md_mlp.Linear(layer_name='y', dim=out_size, irange=0.0001, W_lr_scale=lr_scale, b_lr_scale=1.0)
    model = p2_md_mlp.MLP(nvis=in_size, layers=[h1_layer, h2_layer, o_layer], seed=1)
    dropout_cost = p2_ct_mlp_dropout.Dropout(input_include_probs={'h1':1.0, 'h2':include_rate, 'y':include_rate}, 
                                             input_scales={'h1':1.0, 'h2':np.float32(1.0/include_rate),
                                                           'y':np.float32(1.0/include_rate)})
    
    algorithm = p2_alg_sgd.SGD(batch_size=b_size, learning_rate=l_rate, 
                               learning_rule = p2_alg_lr.Momentum(momentum),
                               termination_criterion=p2_termcri.EpochCounter(max_epochs=1000),
                               cost=dropout_cost)

    train = pylearn2.train.Train(dataset=data_tr, model=model, algorithm=algorithm)
    train.setup()

    x = T.matrix()
    y = model.fprop(x)
    f = theano.function([x], y)

    MAE_va_old = 10.0
    MAE_va_best = 10.0
    MAE_tr_old = 10.0
    MAE_te_old = 10.0
    MAE_1000G_old = 10.0
    MAE_1000G_best = 10.0
    MAE_GTEx_old = 10.0

    outlog = open(base_name + '.log', 'w')
    log_str = '\t'.join(map(str, ['epoch', 'MAE_va', 'MAE_va_change', 'MAE_te', 'MAE_te_change', 
                              'MAE_1000G', 'MAE_1000G_change', 'MAE_GTEx', 'MAE_GTEx_change',
                              'MAE_tr', 'MAE_tr_change', 'learing_rate', 'time(sec)']))
    print log_str
    outlog.write(log_str + '\n')
    sys.stdout.flush()

    for epoch in range(0, n_epoch):
        t_old = time.time()
        train.algorithm.train(train.dataset)
        
        Y_va_hat = f(X_va.astype('float32')).astype('float64')
        Y_te_hat = f(X_te.astype('float32')).astype('float64')
        Y_tr_hat_monitor = f(X_tr_monitor.astype('float32')).astype('float64')
        Y_1000G_hat = f(X_1000G.astype('float32')).astype('float64')
        Y_GTEx_hat = f(X_GTEx.astype('float32')).astype('float64')

        MAE_va = np.abs(Y_va_target - Y_va_hat).mean()
        MAE_te = np.abs(Y_te_target - Y_te_hat).mean()
        MAE_tr = np.abs(Y_tr_monitor_target - Y_tr_hat_monitor).mean()
        MAE_1000G = np.abs(Y_1000G_target - Y_1000G_hat).mean()
        MAE_GTEx = np.abs(Y_GTEx_target - Y_GTEx_hat).mean()
        
        MAE_va_change = (MAE_va - MAE_va_old)/MAE_va_old
        MAE_te_change = (MAE_te - MAE_te_old)/MAE_te_old
        MAE_tr_change = (MAE_tr - MAE_tr_old)/MAE_tr_old
        MAE_1000G_change = (MAE_1000G - MAE_1000G_old)/MAE_1000G_old
        MAE_GTEx_change = (MAE_GTEx - MAE_GTEx_old)/MAE_GTEx_old

        
        MAE_va_old = MAE_va
        MAE_te_old = MAE_te
        MAE_tr_old = MAE_tr
        MAE_1000G_old = MAE_1000G
        MAE_GTEx_old = MAE_GTEx

        
        t_new = time.time()
        l_rate = train.algorithm.learning_rate.get_value()
        log_str = '\t'.join(map(str, [epoch+1, '%.6f'%MAE_va, '%.6f'%MAE_va_change, '%.6f'%MAE_te, '%.6f'%MAE_te_change,
                                  '%.6f'%MAE_1000G, '%.6f'%MAE_1000G_change, '%.6f'%MAE_GTEx, '%.6f'%MAE_GTEx_change,
                                  '%.6f'%MAE_tr, '%.6f'%MAE_tr_change, '%.5f'%l_rate, int(t_new-t_old)]))
        print log_str
        outlog.write(log_str + '\n')
        sys.stdout.flush()
        
        if MAE_tr_change > 0:
            l_rate = l_rate*decay_factor
        if l_rate < l_rate_min:
            l_rate = l_rate_min

        train.algorithm.learning_rate.set_value(np.float32(l_rate))

        if MAE_va < MAE_va_best:
            MAE_va_best = MAE_va
            outmodel = open(base_name + '_bestva_model.pkl', 'wb')
            pkl.dump(model, outmodel)
            outmodel.close()    
            np.save(base_name + '_bestva_Y_te_hat.npy', Y_te_hat)
            np.save(base_name + '_bestva_Y_va_hat.npy', Y_va_hat)
        
        if MAE_1000G < MAE_1000G_best:
            MAE_1000G_best = MAE_1000G
            outmodel = open(base_name + '_best1000G_model.pkl', 'wb')
            pkl.dump(model, outmodel)
            outmodel.close()    
            np.save(base_name + '_best1000G_Y_1000G_hat.npy', Y_1000G_hat)
            np.save(base_name + '_best1000G_Y_GTEx_hat.npy', Y_GTEx_hat)

    print 'MAE_va_best : %.6f' % (MAE_va_best)
    print 'MAE_1000G_best : %.6f' % (MAE_1000G_best)
    outlog.write('MAE_va_best : %.6f' % (MAE_va_best) + '\n')
    outlog.write('MAE_1000G_best : %.6f' % (MAE_1000G_best) + '\n')
    outlog.close()

if __name__ == '__main__':
    main()








    


#!/bin/bash

./gct2npy.py bgedv2_QNORM.gctx bgedv2_float64.npy


./kmeans.py
./nodup_idx.py


./bgedv2.py
./bgedv2_reqnorm.py
./bgedv2_norm.py


./GTEx.py
./GTEx_reqnorm.py
./GTEx_norm.py


./1000G.py
./1000G_reqnorm.py
./1000G_norm.py


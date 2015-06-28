#!/usr/bin/env python

import sys

import numpy as np
import cmap.io.gct as gct

GTEx_GCTX = 'GTEx_RNASeq_RPKM_n2921x55993.gctx'
BGEDV2_LM_ID = 'bgedv2_GTEx_1000G_lm.txt'
BGEDV2_TG_ID = 'bgedv2_GTEx_1000G_tg.txt'

def main():
    GTEx_gctobj = gct.GCT(GTEx_GCTX)
    GTEx_gctobj.read()
    GTEx_genes = map(lambda x:x.split('.')[0], GTEx_gctobj.get_rids())

    lm_id = []
    infile = open(BGEDV2_LM_ID)
    for line in infile:
        ID = line.strip('\n').split('\t')[0]
        lm_id.append(ID)
    
    infile.close()
    lm_idx = map(GTEx_genes.index, lm_id)
    
    tg_id = []
    infile = open(BGEDV2_TG_ID)
    for line in infile:
        ID = line.strip('\n').split('\t')[0]
        tg_id.append(ID)
    
    infile.close()
    tg_idx = map(GTEx_genes.index, tg_id)
    
    genes_idx = lm_idx + tg_idx
    
    data = GTEx_gctobj.matrix[genes_idx, :].astype('float64')
    
    np.save('GTEx_float64.npy', data)
    

        
if __name__ == '__main__':
    main()
    
    
    
    
    
    

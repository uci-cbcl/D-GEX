#!/usr/bin/env python

import sys

import numpy as np

RNASeq_1000G = 'GD462.GeneQuantRPKM.50FN.samplename.resk10.txt'
BGEDV2_LM_ID = 'bgedv2_GTEx_1000G_lm.txt'
BGEDV2_TG_ID = 'bgedv2_GTEx_1000G_tg.txt'

def main():
    ONE_K_G_genes = []
    RPKM = []
    infile = open(RNASeq_1000G)
    line = infile.next()
    for line in infile:
        fields = line.strip('\n').split('\t')
        ID = fields[0].split('.')[0]
        rpkm = map(float, fields[4:])
        ONE_K_G_genes.append(ID)
        RPKM.append(rpkm)
    
    infile.close()
    RPKM = np.array(RPKM)
  
    lm_id = []
    infile = open(BGEDV2_LM_ID)
    for line in infile:
        ID = line.strip('\n').split('\t')[0]
        lm_id.append(ID)
    
    infile.close()
    lm_idx = map(ONE_K_G_genes.index, lm_id)
    
    tg_id = []
    infile = open(BGEDV2_TG_ID)
    for line in infile:
        ID = line.strip('\n').split('\t')[0]
        tg_id.append(ID)
    
    infile.close()
    tg_idx = map(ONE_K_G_genes.index, tg_id)
    
    genes_idx = lm_idx + tg_idx
    
    data = RPKM[genes_idx, :].astype('float64')
    
    np.save('1000G_float64.npy', data)
    

        
if __name__ == '__main__':
    main()
    
    
    
    
    
    

#!/usr/bin/env python

import sys

import numpy as np
import cmap.io.gct as gct


def main():
    infile = sys.argv[1]
    outfile = sys.argv[2]
    
    gctobj = gct.GCT(infile)
    gctobj.read()
    
    data = gctobj.matrix[:, :].astype('float64')
    
    np.save(outfile, data)
    
        
if __name__ == '__main__':
    main()
    
    
    
    
    
    

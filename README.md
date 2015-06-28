README for D-GEX
================

INTRODUCTION
============

Large scale gene expression profiling is the primary
tool to reveal the gene expression patterns in cellular responses to
various diseases, genetic perturbations and drug treatments. While
whole genome expression profiling of ~22,000 genes under numerous
experimental conditions is expensive, the expression of ~1,000
landmark genes can be cost-effectively profiled using the L1000
technology developed by researchers from the LINCS program.
The expression of the remaining ~21,000 target genes can be then
computationally inferred based on the existing expression data of
the Gene Expression Omnibus. However, a linear-regression-based
method is currently adopted by the LINCS program for the inference
part, which inevitably ignores the nonlinearity within gene expression
profiles. We present a deep learning method for gene expression
inference (D-GEX). Results on the microarray data of the
Gene Expression Omnibus show that deep learning significantly
outperforms linear regression with 15.33% relative improvement. A
gene-wise comparative analysis shows deep learning achieves lower
error than linear regression in 99.97% of the target genes. Results
on the RNA-Seq data of the Genotype-Tissue Expression show that
deep learning with regularization techniques still outperforms linear
regression with 6.57% relative improvement and achieves lower error
in 81.31% of the target genes, even training and prediction were done
on different platforms of expression data. This code base provides all
the necessary pieces to reproduce the main results of D-GEX.


Prerequisites
=============
**Mandatory** 

* Python (2.7). [Python 2.7.6](http://www.python.org/download/releases/2.7.6/) is recommended.

* [Numpy](http://www.numpy.org/)(>=1.6.1). You can download the source of Numpy from [here](http://sourceforge.net/projects/numpy/files/).

* [Scipy](http://www.scipy.org/)(>=0.10). You can download the source of Scipy from [here](http://sourceforge.net/projects/scipy/files/).

* [Theano](http://deeplearning.net/software/theano/)(0.7). You can download the source of Theano from [here](https://github.com/Theano/Theano/releases).

* [Pylearn2](https://github.com/lisa-lab/pylearn2).

*  

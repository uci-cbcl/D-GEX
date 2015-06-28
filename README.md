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
the necessary pieces to reproduce the main results of D-GEX. If you have any 
questions, please email yil8@uci.edu







PREREQUISITES
=============
* Python (2.7). [Python 2.7.6](http://www.python.org/download/releases/2.7.6/) is recommended.

* [Numpy](http://www.numpy.org/)(>=1.6.1). 

* [Scipy](http://www.scipy.org/)(>=0.10). 

* [Theano](http://deeplearning.net/software/theano/)(0.7).

* [Pylearn2](https://github.com/lisa-lab/pylearn2).

* [Scikit-learn](http://scikit-learn.org/stable/)(>=0.15.2).

* [l1ktools](https://github.com/cmap/l1ktools).






DATA
====
The original data files are not provided within this codebase, as some of them require applying for access. Once you download all of them, please put them in this codebase.

GEO
---
The GEO microarray expression data can be accessed from [lincscloud](http://www.lincscloud.org/l1000/). You need to [apply](https://docs.google.com/forms/d/1j6Vb_s4FrDodxoS3IDZsHWoVNrOnKNQbqwbwcW2a208/viewform) for the access. The original data downloaded is **bgedv2_QNORM.gctx** (data level 3 Q2NORM).


GTEx
----
The GTEx RNA-Seq expression data can be accessed from [GTEx Portal](http://www.gtexportal.org/home/). You need to apply through dbGaP [phs000424.v3.p1](http://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs000424.v3.p1) for the access. The original data downloaded is **GTEx_RNASeq_RPKM_n2921x55993.gctx**.

1000G
-----
The 1000 Genomes RNA-Seq expression data can be accessed from [EMBL-EBI](http://www.ebi.ac.uk/arrayexpress/experiments/E-GEUV-1/files/analysis_results/?ref=E-GEUV-1). The original data downloaded is **GD462.GeneQuantRPKM.50FN.samplename.resk10.txt**.








PREPROCESS
==========
The whole preprocessing step should be done by run
```
$ ./preprocess.sh
```

Specifically, there are four steps.

1. Removing duplicates by k-means: `kmeans.py`, `nodup_idx.py`.
2. Coverting data into numpy format: `bgedv2.py`, `GTEx.py`, `1000G.py`.
3. Quantile normalization: `bgedv2_reqnorm.py`, `GTEx_reqnorm.py`, `1000G_reqnorm.py`.
4. Standardization: `bgedv2_norm.py`, `GTEx_norm.py`, `1000G_norm.py`.





TRAINING
========
Training D-GEX is done by run `H1_0-4760.py`, `H1_4760-9520.py`, `H2_0-4760.py`, `H2_4760-9520.py`, `H3_0-4760.py`, `H3_4760-9520.py`. Each stript trains half of the target genes (0-4760 or 4760-9520) with a certain architecture (1, 2 or 3 hidden layers).

A training example using 200 epoch, 0.75 include rate (0.25 dropout rate) and 9000 hidden units within each hidden layer for 0-4760 target genes with 1 hidden layer is by:
```
$ ./ H1_0-4760.py 9000_H1_0-4760_75 200 9000 0.75
```
In which, **9000_H1_0-4760_75** is the base name for all the output files.



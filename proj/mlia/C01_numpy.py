# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 10:53:30 2014

@author: 1309075
"""

import numpy as np

rands=np.mat(np.random.rand(4,4))
rands

rands_inv=rands.I
rands_inv

my_eye=rands * rands_inv
eye=np.eye(4)
my_eye-eye

import proj.silkyfowl.svmutil 
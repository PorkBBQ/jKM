# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 15:43:56 2014

@author: Josh
"""

hadoop jar $STREAMING \
-input  /user/cloudera/data/jeckle \
-input  /user/cloudera/data/heckle \
-output /tmp/dsc01_02
-mapper /user/cloudera/scripts/cleaning/clean_map.py \
-file /user/cloudera/scripts/cleaning/clean_map.py \
-reducer /user/cloudera/scripts/cleaning/clean_reduce.py \
-file /user/cloudera/scripts/cleaning/clean_reduce.py


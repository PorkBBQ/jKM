# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 15:43:56 2014

@author: Josh
"""

hadoop fs -rm -R /tmp/dsc01_02

hadoop jar $STREAMING \
-input  /user/cloudera/data/jeckle \
-input  /user/cloudera/data/heckle \
-output /tmp/dsc01_02 \
-mapper /home/cloudera/scripts/cleaning/clean_map.py \
-file /home/cloudera/scripts/cleaning/clean_map.py \
-reducer /home/cloudera/scripts/cleaning/clean_reduce.py \
-file /home/cloudera/scripts/cleaning/clean_reduce.py


import proj.jKM
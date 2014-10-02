# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 14:05:31 2014

@author: Josh
"""


'''
for i in range(3):
    for j in range(100):
        print('echo "%s %d %d" >> dir_%s/%d' %(chr(i+97)*3, i+1, j+1, chr(i+97), j+1))


mkdir dir_0 dir_1 dir_2 dir_3 dir_4
'''

import random
env={
    'dir':'dir'
    , 'numGroup':5
    , 'numConfounder':5
    , 'numFile':100
}
for i in range(env['numGroup']):
    for j in range(env['numFile']):
        f = file('dir_%d/%d' %(i, j),'w')
        rand=random.randint(0,env['numConfounder']-1)
        #print('echo "%s %d" >> dir_%s/%d' %(i, rand, i, j))
        f.write("%s %d\n"%(i, rand))
        f.close()

'''
# 100 files ==================================================================    
env={
    'dir':'dir'
    , 'numGroup':5
    , 'numConfounder':5
    , 'numFile':100
}

=======================================================
Summary
-------------------------------------------------------
Correctly Classified Instances          :        100       55.5556%
Incorrectly Classified Instances        :         80       44.4444%
Total Classified Instances              :        180

=======================================================
Confusion Matrix
-------------------------------------------------------
a       b       c       d       e       <--Classified as
25      0       0       6       10       |  41          a     = dir_0
6       22      0       11      5        |  44          b     = dir_1
9       11      10      7       5        |  42          c     = dir_2
0       0       0       24      10       |  34          d     = dir_3
0       0       0       0       19       |  19          e     = dir_4

=======================================================
Statistics
-------------------------------------------------------
Kappa                                       0.4202
Accuracy                                   55.5556%
Reliability                                50.8956%
Reliability (standard deviation)            0.3529

# /100 files ==================================================================    

# 1000 files ==================================================================    
import random
env={
    'dir':'dir'
    , 'numGroup':5
    , 'numConfounder':5
    , 'numFile':1000
}
=======================================================
Summary
-------------------------------------------------------
Correctly Classified Instances          :       1336       67.4747%
Incorrectly Classified Instances        :        644       32.5253%
Total Classified Instances              :       1980

=======================================================
Confusion Matrix
-------------------------------------------------------
a       b       c       d       e       <--Classified as
216     0       72      54      74       |  416         a     = dir_0
61      150     67      77      79       |  434         b     = dir_1
0       0       377     0       0        |  377         c     = dir_2
0       0       47      354     0        |  401         d     = dir_3
0       0       54      59      239      |  352         e     = dir_4

=======================================================
Statistics
-------------------------------------------------------
Kappa                                       0.5906
Accuracy                                   67.4747%
Reliability                                57.1104%
Reliability (standard deviation)            0.3667

# /1000 files ==================================================================    

# 10000 files ==================================================================    
env={
    'dir':'dir'
    , 'numGroup':5
    , 'numConfounder':5
    , 'numFile':10000
}

=======================================================
Summary
-------------------------------------------------------
Correctly Classified Instances          :        654       33.0303%
Incorrectly Classified Instances        :       1326       66.9697%
Total Classified Instances              :       1980

=======================================================
Confusion Matrix
-------------------------------------------------------
a       b       c       d       e       <--Classified as
654     339     325     323     339      |  1980        a     = dir_0
0       0       0       0       0        |  0           b     = dir_1
0       0       0       0       0        |  0           c     = dir_2
0       0       0       0       0        |  0           d     = dir_3
0       0       0       0       0        |  0           e     = dir_4

=======================================================
Statistics
-------------------------------------------------------
Kappa                                       0.0012
Accuracy                                   33.0303%
Reliability                                 5.5051%


# /10000 files ==================================================================  


mahout vectordump \
-i $DH/vector/tf-vectors/part-r-00000 \
-o $DH/tf-vectors-dump
'''
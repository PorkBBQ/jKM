
import numpy as np
a=np.array([1,2,3,4,5])
b=np.array([[1,2,3], [4,5,6]])
b
b[:,1:]

import random
r=rand(5,3)

v=np.array([1,2,3,4,5])
v[v>2]
np.array(range(1,6,2))

m=np.array([[1,4,7,10],[2,5,8,11],[3,6,9,12]])
m
v[v>2]

m=np.array(range(1,13))
m=m.reshape([3,4])

m[0:2,1:]

m=np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]], )

m=np.array(range(1,13))
m=m.reshape([4,3]).T
m
m[:2,1:]

v[5]=6
v=[v,6]
v

import random
random.random()

m=np.array([
[0.9347052, 0.1255551, 0.01339033]
, [0.2121425, 0.2672207, 0.38238796]
, [0.6516738, 0.3861141, 0.86969085]
])

print(m.dot(m))

m.diagonal()

import pandas as pd

df = pd.DataFrame([[1,4],[2,5],[3,6]])
df.columns=['c1', 'c2']
df.sum()


m
pd.DataFrame(m)



m=np.array(range(1,13))
m.reshape([4,3]).T


m=np.array(range(1,13))
m.reshape([3,4], order='F')



np.zeros((5,6))+1

np.arange(10,0)

np.linspace(0,10,5)

set_printoptions(threshold=10)
pd.DataFrame(np.ones(10000).reshape(2000,5))

m

m*m
m.dot(m)

import random

np.random.random((4,5))


np.random.normal(0,1,10)


np.random.uniform(low=0, high=10,size=5)

np.random.normal(loc=0,scale=1, size=5)

np.random.poisson(lam=5, size=10)

m.min(axis=0)

m=arange(1,13).reshape(3,4, order='F')

m.sum(axis=0)

m.cumsum(axis=0)



a=[
    [1,2,3]
    , [4,6,5]
    , [5,4,5]
]


import numpy as np
aa=np.array(a)
aa
np.cov(aa)

#!/user/bin/env/Python

import pandas as pd
import pdb
from pulp import *

# putting python classes in pandas dataframes

class MyPoint:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

my_list = [MyPoint(1, 1), MyPoint(2, 2)]

plane_pd = pd.DataFrame([[p.x, p.y, p] for p in my_list],
                        columns=list('XYO'))

def _addChoices():
    choices = pd.read_csv('sudoku_pandas_df_indices.csv')
    counter = 0
    for r in range(1,10):
        for c in range(1,10):
            for v in range(1,10):
                choices.set_value(counter, 'choice', LpVariable("x_{}_{}_{}".format(v,r,c), 0, 1, LpInteger))
                counter += 1
    return choices

cdf = _addChoices()

i=1
j=1
k=1

y = cdf.iat[]
x = cdf[(cdf['vals'] == i) & (cdf['cols'] == j) & (cdf['rows'] == k)]['choice'].tolist()



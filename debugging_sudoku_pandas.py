#!/user/bin/env/Python

# references
# https://stackoverflow.com/questions/31111032/transform-a-counter-object-into-a-pandas-dataframe

import pandas as pd
from pulp import *

# add to the dataframe
choices = pd.read_csv('sudoku_pandas_df_indices.csv')
LPvars = []
for i in range(729):
    LPvars += [LpVariable("", 0, 1, LpInteger)]

x1 = LpVariable("", 0, 1, LpInteger)

choices["choice"] = pd.Series(LPvars, index = choices.index)

Sequence = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
Vals = Sequence
Rows = Sequence
Cols = Sequence

dict2 = LpVariable.dicts("Choice", (Vals, Rows, Cols), 0, 1, LpInteger)

df2 = pd.DataFrame.from_dict(dict2, 'index')

dict3 = LpVariable.dicts("Choice", (["1","2","3"],["1", "2", "3"]), 0, 1, LpInteger)

df3 = pd.DataFrame.from_dict(dict3, orient='columns')

df3['1'].append(df3['2']).append(df3['3']).reset_index(drop=True)

df4 = pd.DataFrame({'A' : [1,2], 'B' : [3,4]})

df4
#!/user/bin/env/Python

import pandas as pd

# January 10th: Playing with Pandas

# in this file, we follow along with a pandas tutorial
# https://pandas.pydata.org/pandas-docs/stable/tutorials.html

# # general stuff on the tutorial
# # to select a new table for the whole  the row_name is filled with row_value
# row_value-row_name = df[df[row_name] == row_value]

## Creating a dataframe by manually inputting data
# https://stackoverflow.com/questions/32814746/pandas-create-dataframe-manually-and-insert-values
df = pd.DataFrame(columns=["A", "B"], data=[[5,6]])
#https://stackoverflow.com/questions/15315452/selecting-with-complex-criteria-from-pandas-dataframe
df = pd.DataFrame({'A': [5,6], 'B': [6,7]})

## Add Values
df.set_value(1,'A',5)

## Make a List
df['A'].tolist()

## Access df only at rows such that col_name = value (e.g. 'A' == 5.0)
df[df['A'] == 5.0]

## Access df values of 'B' on rows such that col_name = value
df[df['A'] == 5.0]['B']
df[df['A'] == 5.0]['B'].tolist()

## Access df rows such subject to value constraint conditions
df[(df['A']==5.0) & (df['B']==6.0)]

df = pd.read_csv('sudoku_pandas_df_indices.csv')
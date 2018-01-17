#!/user/bin/env/Python

from pulp import *
import pandas as pd

df = pd.DataFrame({'A': [5,8], 'B': [6,7]})

prob = LpProblem("Pet Food with " + "chicken" + " and " + "beef",
                     LpMinimize)

x_1 = LpVariable("chickenPercent", 0, None, LpInteger)
x_2 = LpVariable("beefPercent", 0, None, LpInteger)

generator = df.iterrows()

for row in generator:
    print row

# v = 1 * x_1 + 2 * x_2

# prob += v, ""
#!/user/bin/env/Python

# A list of strings from "1" to "9" is created
Sequence = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

# The Vals, Rows and Cols sequences all follow this form
Vals = Sequence
Rows = Sequence
Cols = Sequence

# # Creating boxes
# Boxes =[]
# for i in range(3):
#     for j in range(3):
#         new_list = [[(Rows[3*i+k],Cols[3*j+l]) for k in range(3) for l in range(3)]]
#         print (new_list)
#         Boxes += new_list

# how about this way
Sequence = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
Vals = Sequence
Rows = Sequence
Cols = Sequence
Boxes = []
for r in range(3):
    for c in range(3):
        list = [[(Rows[3*r + i], Cols[3*c +j]) for i in range(3) for j in range(3)]]
        print(list)
        Boxes += list
print "Here's the whole shebang of elements of the list of boxes"
print(Boxes)
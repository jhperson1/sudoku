#!/user/bin/env/Python

# a file to test syntax

class test():
    def __init__(self):
        self.Rows = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.Cols = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.value = 0
        self.Boxes = self._addBoxes()
        print("The Boxes variable is ", self.Boxes)
        self._addValue()

    # helper functions

    def _addBoxes(self):
        Boxes = []
        for r in range(3):
            for c in range(3):
                list = [[(self.Rows[3*r + i], self.Cols[3*c +j]) for i in range(3) for j in range(3)]]
                Boxes += list
        return Boxes

    def _addValue(self):
        self.Boxes += [[(1,1)]]
class SolverParent(object):
    def __init__(self):
    def addBoard(self, board):
    def solve(self):
    def solutionWriteUpALL(self):
        self.solutionWriteUp()

    # ------ helper methods/ private methods ------ #
    def _welcome(self):
    def _updateStatus(self):
    def _printStatus(self):
    def _addBasicsALL(self):
        self._addBasics()
    def _addChoicesALL(self):
        self._addChoices()
    def _addObjective(self):
    def _addSudokuRulesALL(self):
        self._addSudokuHints()
    def _readFromBoard(self, board):
    def _addSudokuHintsALL(self, hints):
        self._addSudokuHints()
    def _problemWriteUp(self):
    def _writeToBoardALL(self):
        self._writeToBoard()

class SolverPandasDF(SolverParent):
    def solutionWriteUp(self, board):

    # ------ helper methods/ private methods ------ #
    def _addBasics(self):
    def _addChoices(self):
    def _addSudokuRules(self):
    def _addSudokuHints(self, hints):
    def _writeToBoard(self):

class SolverDictionary(SolverParent):
    def solutionWriteUp(self, board):

    # ------ helper methods/ private methods ------ #
    def _addBasics(self):
    def _addChoices(self):
    def _addSudokuRules(self):
    def _addSudokuHints(self, hints):
    def _writeToBoard(self):



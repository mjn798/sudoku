class Backtracking:

    # track the number of iterations / numbers set as a performance indicator
    tracks = 0

    # is it allowed to set a certain value at a certain index in the sudoku?
    def isAllowed(self, sudoku, index, value):
        # create a set of indices of neighbour cells to identify where the value might be set already (= conflict) (row, column, block, not itself)
        neighbours = set()
        for i in range(9): neighbours.update([(((index // 9) * 9) + i), ((index % 9) + (i * 9)), (((index // 27) * 27) + (((index % 9) // 3) * 3) + (i % 3) + ((i // 3) * 9))])
        # return False if the value is conflicting with any neighbour cell, otherwise True
        return not any(sudoku[i] == value for i in (neighbours.difference({index})))

    # recursive backtracking function
    def solveSudoku(self, sudoku):
        # find the first occurance of . in the string
        # if there are no . characters left, the index() function throws an exception and the puzzle is solved
        try:    position = sudoku.index(".")
        except: self.solved = sudoku; return True
        # otherwise, check all numbers between 1 and 9 for the current position - old numbers will just be overwritten
        for value in "123456789":
            # if there are no conflicts with neighbour cells, set the number at the position and continue in the tree
            if self.isAllowed(sudoku, position, value):
                sudoku = sudoku[:position] + value + sudoku[position+1:]
                # track the effort
                self.tracks += 1
                # if the child is completely solved, return True to the parent, otherwise continue in the tree
                if self.solveSudoku(sudoku): return True
        # reset the current position to its original . character to allow the previous branch expanding back to this position within a new iterated parent
        sudoku = sudoku[:position] + "." + sudoku[position+1:]
        # sudoku is not solved yet - continue with the in the parent's for-loop, if last parent then there is no solution to this sudoku puzzle
        return False

    # main method to call, returning either the completed sudoku or "no solution"
    def solve(self, sudoku): return self.solved if self.solveSudoku(sudoku) else "no solution"

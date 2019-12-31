class Logic:

    # track the number of iterations as a performance indicator
    tracks = 0

    # global cache for each individual cell's neighbours
    neighbourCache = list()

    # prepare the neighbourCache for each individual cell - with indices for row, column, block and a combination
    def prepareNeighbourCache(self):
        # for each cell in the sudoku
        for index in range(81):
            # create new distinct sets for neighbours
            neighboursRow = set()
            neighboursColumn = set()
            neighboursBlock = set()
            # each cell has 9 neighbours per row, column and block (including itself)
            for i in range(9):
                neighboursRow.add(((index // 9) * 9) + i)
                neighboursColumn.add((index % 9) + (i * 9))
                neighboursBlock.add(((index // 27) * 27) + (((index % 9) // 3) * 3) + (i % 3) + ((i // 3) * 9))
            # add neighbours to the cache and remove the index, as the cell itself is not its own neighbour
            self.neighbourCache.append({"row": list(neighboursRow.difference({index})), "column": list(neighboursColumn.difference({index})), "block": list(neighboursBlock.difference({index})), "all": list(neighboursRow.union(neighboursColumn, neighboursBlock).difference({index}))})

    # prepare the puzzle
    def preparePuzzle(self, puzzle):
        # add all candidates (1-9) to all individual cells
        cells = list("123456789" for i in range(81))
        # for all non . characters in the puzzle, set the known number
        for index in range(81):
            if puzzle[index] != ".":
                cells = self.setValue(cells, index, puzzle[index])
        # return the prepared puzzle - all fields have max 9 candidates, known values only have 1 candidate
        return cells

    # if a value is allowed, set it as a known value for the cell
    def setValue(self, cells, index, value):
        # is it allowed to set the value at the index?
        if self.isAllowedToSet(cells, index, value):
            # set the value, making it the only possible candidate
            cells[index] = value
            # remove the value from its neighbours' candidates
            for neighbour in self.neighbourCache[index]["all"]:
                # only look at the cell if the value is still a potential candidate
                if value in cells[neighbour]:
                    cells[neighbour] = cells[neighbour].replace(value, "")
                    # naked single - if there is only one candidate left, it must be the known value
                    if len(cells[neighbour]) == 1: self.setValue(cells, neighbour, cells[neighbour])
        return cells

    # find hidden singles - if a candidate only appears once per row, column or block it must be the known value
    def findHiddenSingles(self, cells):
        # check all possible cells
        for index in range(81):
            # only consider if it is not a known value - there must be more than one candidate left
            if len(cells[index]) > 1:
                # search in each row, column and block individually
                for cacheType in ["row", "column", "block"]:
                    # variable to compare to the actual value in the index to its neighbours
                    checkUnit = cells[index]
                    # check all candidate values in all neighbour cells
                    for neighbour in self.neighbourCache[index][cacheType]:
                        for value in cells[neighbour]:
                            # remove all the neighbour's candidate numbers from the comparison
                            checkUnit = checkUnit.replace(value, "")
                    # if there is only one candidate left we have found a hidden single
                    if len(checkUnit) == 1: cells = self.setValue(cells, index, checkUnit); break
        return cells

    # find naked pairs - if a candidate pair appears in only two cells per row, column or block it must be there and cannot be a candidate for any other neighbours
    def findNakedPairs(self, cells):
        # check all possible cells
        for index in range(81):
            # only consider if there are exactly two candidates left
            if len(cells[index]) == 2:
                # search in each row, column and block individually
                for cacheType in ["row", "column", "block"]:
                    # check all the neighbours of the cell for matches
                    for neighbour in self.neighbourCache[index][cacheType]:
                        # is it a match / exactly the same two values?
                        if cells[index] == cells[neighbour]:
                            # all other neighbours get the two candidates removed
                            for affected in list(set(self.neighbourCache[index][cacheType]).difference({neighbour})):
                                for value in cells[index]:
                                    cells[affected] = cells[affected].replace(value, "")
                                # if there's only one candidate left, the affected cell has now a known value
                                if len(cells[affected]) == 1: cells = self.setValue(cells, affected, cells[affected])
        return cells

    # is it allowed to set a certain value at a certain index in the sudoku?
    def isAllowedToSet(self, cells, index, value):
        # return true if the 1) value is a candidate AND 2) the value is not already a known value in any neighbour cell
        return (value in cells[index]) and all(value != cells[neighbour] for neighbour in self.neighbourCache[index]["all"])

    # is there a contradiction in the sudoku, e.g. empty cells or duplicate known values?
    def hasContradiction(self, cells):
        # for each field in the sudoku
        for i in range(81):
            # if there are any empty cells, it is a contradiction
            if len(cells[i]) == 0: return True
            # if there are any two neighbours with the same known value, it is a contradiction
            if len(cells[i]) == 1:
                for neighbour in self.neighbourCache[i]["all"]:
                    if cells[neighbour] == cells[i]: return True
        # if there are no contradictions, return False
        return False

    # recursive backtracking function
    def solveSudoku(self, cells):
        # before doing anything, optimize the cells
        tempcells = list()
        while cells != tempcells:
            cells = self.findHiddenSingles(cells)
            cells = self.findNakedPairs(cells)
            tempcells = cells
        # if there is a contradiction return False - something is wrong with the solution
        if self.hasContradiction(cells):
            return False
        # if all cells only have one candidate left, the puzzle is solved
        if all(len(cell) == 1 for cell in cells):
            self.solved = cells.copy()
            return True
        # get the next open position for setting a value by checking field lengths and take the shortest one
        position = -1
        for i in range(81):
            if (len(cells[i]) == 2): position = i; break
            elif (len(cells[i]) < max(2, len(cells[position]))): position = i
        # check all possible candidates for the current position
        for value in cells[position]:
            # if there are no conflicts with neighbour cells, set the number at the position and continue in the tree
            if self.isAllowedToSet(cells, position, value):
                # track the effort
                self.tracks += 1
                # remember the current state as of now
                oldCells = cells.copy()
                # set the candidate value at the current position
                cells = self.setValue(cells, position, value)
                # if the child is completely solved, return True to the parent, otherwise continue in the tree
                if self.solveSudoku(cells): return True
                # revert to the original state
                cells = oldCells.copy()
        # sudoku is not solved yet - continue with the in the parent's for-loop, if last parent then there is no solution to this sudoku puzzle
        return False

    # main method to call, returning either the completed sudoku or "no solution"
    def solve(self, sudoku): return "".join(self.solved) if self.solveSudoku(self.preparePuzzle(sudoku)) else "no solution"

    # on init, create the neighbourCache for performance
    def __init__(self): self.prepareNeighbourCache()

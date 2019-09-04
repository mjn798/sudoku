class Logic:

    # track the number of iterations / numbers set as a performance indicator
    tracks = 0

    # global cache for each individual cell's neighbours
    neighbourCache = list()

    # prepare the neighbourCache for each individual cell - dictionary with indices for row, column, block and a combination of all of them
    def prepareNeighbourCache(self):
        # for each field in the sudoku
        for index in range(81):
            # create new sets for candidate values - each candidate should only appear once
            neighboursRow = set()
            neighboursColumn = set()
            neighboursBlock = set()
            # each field has 9 neighbours per row, column and block
            for i in range(9):
                neighboursRow.add(((index // 9) * 9) + i)
                neighboursColumn.add((index % 9) + (i * 9))
                neighboursBlock.add(((index // 27) * 27) + (((index % 9) // 3) * 3) + (i % 3) + ((i // 3) * 9))
            # add neighbours to the cache and remove the index - the index itself is not its own neighbour
            self.neighbourCache.append({"row": list(neighboursRow.difference({index})), "column": list(neighboursColumn.difference({index})), "block": list(neighboursBlock.difference({index})), "all": list(neighboursRow.union(neighboursColumn, neighboursBlock).difference({index}))})

    # prepare the puzzle
    def preparePuzzle(self, puzzle):
        # add all candidates (1-9) to individual cells
        cells = list("123456789" for i in range(81))
        # for all non . characters in the puzzle, set the number
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
            # remove the value from all neighbour cells and find any hidden singles
            cells = self.removeFromNeighbours(cells, index, value)
            cells = self.findHiddenSingle(cells, index)
        return cells

    # iterate through all neighbour cells and remove the candidate by blanking it
    def removeFromNeighbours(self, cells, index, value):
        newSingles = list()
        for neighbour in self.neighbourCache[index]["all"]:
            # only look at the cell if the value is still a potential candidate
            if value in cells[neighbour]:
                cells[neighbour] = cells[neighbour].replace(value, "")
                # if there's only one value left as a candidate, it must be the value - set it later
                if len(cells[neighbour]) == 1: newSingles.append(neighbour)
        # set values for cells that had all candidates removed and now have only a single candidate left
        for newSingle in newSingles: cells = self.setValue(cells, newSingle, cells[newSingle])
        return cells

    # find hidden singles wrapper - search for row, column and block
    def findHiddenSingle(self, cells, index):
        for cacheType in ["row", "column", "block"]: cells = self.findHiddenSingleSearch(cells, index, cacheType)
        return cells

    # find hidden singles - if a value only appears once per row, column or block it must be the actual value
    def findHiddenSingleSearch(self, cells, index, cacheType):
        # check the neighbours for the index
        for neighbour in self.neighbourCache[index][cacheType]:
            # only consider if it's not a known value, so more than one candidate
            if len(cells[neighbour]) > 1:
                # checkUnit holds all the candidates in a cell
                checkUnit = cells[neighbour]
                # check the neighbours for the index's neighbour
                for neighboursneighbour in self.neighbourCache[neighbour][cacheType]:
                    # remove each candidate from the checkUnit by blanking the values
                    for value in cells[neighboursneighbour]: checkUnit = checkUnit.replace(value, "")
                # if there's only one number left, it must be the value - so set it
                if len(checkUnit) == 1: cells = self.setValue(cells, neighbour, checkUnit)
        return cells

    # is it allowed to set a certain value at a certain index in the sudoku?
    def isAllowedToSet(self, cells, index, value):
        # return true if the 1) value is a candidate AND 2) the value is not already set in any neighbour cell with a known value (candidate length == 1)
        return (value in cells[index]) and all((value not in cells[neighbour]) for neighbour in self.neighbourCache[index]["all"] if len(cells[neighbour]) == 1)

    # is there a contradiction in the sudoku, e.g. empty cells or duplicate known values?
    def hasContradiction(self, cells):
        # for each field in the sudoku
        for i in range(81):
            # if there are any empty cells, it's a contradiction
            if len(cells[i]) == 0: return True
            # if there are any two neighbours with the same known value, it's a contradiction
            if len(cells[i]) == 1:
                for neighbour in self.neighbourCache[i]["all"]:
                    if cells[neighbour] == cells[i]: return True
        # if there are no contradictions, return False
        return False

    # recursive backtracking function
    def solveSudoku(self, cells):
        # if there's a contradiction return False - something's wrong with the solution
        if self.hasContradiction(cells): return False
        # if all cells only have one candidate left, the puzzle is solved
        if all(len(cell) == 1 for cell in cells):
            self.solved = cells.copy()
            return True
        # get the next open position for setting a value by checking field lengths and take the shortest one (> 1)
        position = -1
        position_length = 11
        for i in range(81):
            if (len(cells[i]) > 1) and (len(cells[i]) < position_length):
                position = i
                position_length = len(cells[i])
            if position_length == 2: break
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

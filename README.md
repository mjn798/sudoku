# sudoku
Sudoku solver using different algorithms

The solver comes with a brute force backtracking algorithm as well as with an algorithm applying a logical candidate elimination before starting a brute force backtracking search.

## Sudoku solver

Run via command line

```
sudoku.py [logic|backtracking]
```

### input.txt

The input.txt file holds Sudoku puzzles represented as a 81 character String - one character per Sudoku field. Known values are written in, unknown values are marked as . or 0 as in the following example:

```
8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..
```

### output.csv

For each valid Sudoku in the input.txt there is one line written into the output.csv, holding the following information:

* the original Sudoku
* the solved Sudoku
* the time to solve (in seconds)
* the number of backtracking steps required to solve

The output.csv file is overwritten with each run.

## Algorithms

### Backtracking

* Find the first empty field and set a valid number (1-9).
* If that's allowed, continue with the next number in the next empty field and so on.
* In case a field cannot hold any number due to row, column and block constraints, revert to a previous state (reset the field to .), go back one field and continue with the next possible number.
* When all fields are filled with valid numbers, the Sudoku must be solved.

### Logic

* Build a cache for getting any field's neighbours instead of calculating them each time.
* Fill all fields with potential candidate numbers (1-9).
* If a known value is set, remove the value from all the neighbour fields in the row, column and block.
* If there's only one single candidate left for a field, this must be the field's known value - so set it ("naked single").
* If there's only one single occurance for a candidate per row, column or block, it must be the known value for this field - so set it ("hidden single).
* If there's an exact pair of candidates per row, column or block the two values can only be in these fields - remove the two numbers from the rest of the potential candidates ("naked pair").
* Once all potential candidates are removed and all Hidden Singles are found, start a backtracking algorithm as explained above.
* When all fields are filled with valid numbers, the Sudoku must be solved.

## Tracks

Tracks (the last field in the output.csv) are performance indicators. The less tracks are required the easier it is to solve the Sudoku. For each number set by the algorithm the track count is increased by one. The 'logic' approach requires usually less tracks as only valid candidates can be set as a potential value, instead of all possible numbers between 1 and 9.
Tracks is measuring the number backtracking steps required to solve a Sudoku.

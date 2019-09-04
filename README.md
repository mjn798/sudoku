# sudoku
Sudoku solver using different algorithms

The solver comes with a brute force backtracking algorithm as well as an algorithm applying a logical candidate elimination before starting a brute force backtracking search.

```
sudoku.py [logic|backtracking]
```

### input.txt

The input.txt file holds Sudoku puzzles as a String with 81 characters - one per field. Known values are written in, unknown values are marked as . or 0 as in the following example:

```
8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..
```

### output.csv

For each valid Sudoku in the input.txt the output.csv holds the following information:

* the original Sudoku
* the solved Sudoku
* the time to solve (in seconds)
* the number of backtracking steps required to solve

The file is overwritten with each run.

## Algorithms

### Backtracking

Find the first empty field and set a valid number (1-9).
If that's allowed, continue with the next number in the next empty field and so on.
If a field can not hold any number, revert to a previous state and continue with the next possible number.
If all fields are filled with valid numbers, the Sudoku must be solved.

### Logic

Use a cache for getting any field's neighbours instead of calculating them each time.

Fill all fields with potential candidate numbers (1-9).
If a value is set, remove the value from all the neighbour fields in the row, column and block.
If there's only one single candidate left for a field, this must be the field's known value - so it's set.
If there's only one single occurance for a candidate per row, column or block, it must be the known value for this field - so it's set.
Once all potential candidates are removed and all Hidden Singles are found, start a backtracking algorithm as explained above.
If all fields are filled with valid numbers, the Sudoku must be solved.

## Tracks

Tracks (the last field in the output) are a performance indicator. The less tracks are required the easier it is to solve the Sudoku. For each number that's set by the algorithm the track count is increased by one. The 'logic' approach requires usually less tracks as only valid candidates can be set as a value, instead of all possible numbers between 1 and 9.
Tracks is measuring the number backtracking steps required to solve a Sudoku.

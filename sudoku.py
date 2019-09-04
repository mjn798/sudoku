import time
import re
import backtracking
import logic
import sys

# check if there's a commandline argument: 'logic' or 'backtracking' - if not, just exit with an error
if len(sys.argv) == 2:
    if sys.argv[1] == "logic":
        solver = logic.Logic()
    elif sys.argv[1] == "backtracking":
        solver = backtracking.Backtracking()
    else: exit("wrong algorithm, use either 'logic' or 'backtracking'")
else:
    exit("no algorithm specified, use either 'logic' or 'backtracking'")

# open input and output files
input = open("input.txt", "r")
output = open("output.csv", "w")

# for every line in the input file
for puzzle in input:

    # allow 0 and . as placeholder characters
    puzzle = puzzle.rstrip('\r\n').replace("0", ".")

    # fit the regex - exactly 81 characters (0-9 and .)
    if re.match("^[\.1-9]{81}$", puzzle):

        # start timer
        time_start = time.time()

        # solve the puzzle
        solver.tracks = 0
        result = solver.solve(puzzle)

        # end timer
        time_end = time.time()

        # write to the .csv output file and feedback in the commandline
        output.write(puzzle + ", " + result + ", " + str(time_end - time_start) + ", " + str(solver.tracks) + "\n")
        print(puzzle + ", " + result + ", " + str(time_end - time_start) + ", " + str(solver.tracks))

# close input and output files
input.close()
output.close()

"""
Compute the matching distance between two modules of your own.

A module is a list of rectangles, and each rectangle is written as its top-right corner
followed by its bottom-left corner: [(6, 6), (0, 0)] is the square with corners (0, 0) and
(6, 6). For a rectangle that is unbounded on one side, use a large number such as 10**8 for
that side. Change M and N below, save the file, and run

    python my_example.py
"""
from matching_distance import run_one

M = [[(6, 6), (0, 0)]]                       # one rectangle
N = [[(8, 4), (4, 2)], [(2, 10), (1, 5)]]    # two rectangles

result = run_one(M, N)
print("matching distance:", result.exact)

# The line on which the distance is attained has direction m through the point b.
line = result.best_line
print("attained on the line with direction", tuple(line.m), "through", tuple(line.b))

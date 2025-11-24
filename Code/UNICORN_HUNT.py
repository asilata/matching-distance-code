import sys
from imports import *
import csv
import random
import settings
import cleanup_helper_funcs as chf

if __name__ == '__main__':

    # sys.argv = [script, M, N, seed]
    if len(sys.argv) != 4:
        print("Usage: python UNICORN_HUNT.py M N seed")
        sys.exit(1)

    rects_in_M = int(sys.argv[1])
    rects_in_N = int(sys.argv[2])
    seed        = int(sys.argv[3])

    settings.print_output = True
    settings.save_figure = True
    path = f"UNICORN_FIGS/figure_{rects_in_M}_{rects_in_N}_{seed}.png"
    # path = "UNICORN_FIGS/"+ "figure.png"
    # rects_in_M = 1
    # rects_in_N = 1
    # seed = 1
    M, N = chf.generate_random_rectangles(rects_in_M, rects_in_N, seed)
    chf.plot_rectangles(M, N, path)

import sys
from imports import *
import csv
import random
import settings
import cleanup_helper_funcs as chf

if __name__ == '__main__':

    settings.print_output = True
    settings.save_figure = True

    path = "UNICORN_FIGS/"+ "figure.png"
    rects_in_M = 1
    rects_in_N = 1
    seed = 1
    M, N = chf.generate_random_rectangles(rects_in_M, rects_in_N, seed)
    chf.plot_rectangles(M, N, path)

import sys
from imports import *
import csv
import random
import settings

if __name__ == '__main__':

    settings.print_output = True
    settings.save_figure = True
    # M, N, title = chf.generate_rects_experiment_2_12()
    # M, N, title = chf.generate_rects_experiment_2_13()
    M, N, title = chf.generate_rects_experiment_2_14()
    rects_in_M = len(M)
    rects_in_N = len(N)


    # ALL PRUNE now
    settings.old_pruning = True 
    settings.new_pruning_march_2025 = True 
    print("~~~ALL (including NEW) PRUNING~~~")
    if settings.print_output:
        print("_____________________________________\nAPPROX\n_____________________________________")
        print('Rects in M: ',rects_in_M)
        print('Rects in N: ',rects_in_N)

    prune_time, approx_time, prune_match_dist, max_dist_critpts, max_grids_lines = chf.to_prune_or_not_to_prune_csv(M,N)

    if settings.print_output:
        print("_____________________________________\nEND\n_____________________________________")

    print("match dist: ",prune_match_dist, "crit pts max: ", max_dist_critpts,"grid lines max: ", max_grids_lines)

    if settings.save_figure:
        settings.figure_title = title + ". Exact matching distance: ", str("%0.2f"%prune_match_dist) + "."
        img_path = 'EXPERIMENT_FIGS/' + title + '_m'+ str(rects_in_M) + '_n' + str(rects_in_N) +'.png'
        chf.plot_rectangles(M,N, img_path)


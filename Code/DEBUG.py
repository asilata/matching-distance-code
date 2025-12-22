import sys
from imports import *
import csv
import random
import settings

if __name__ == '__main__':

################# SETTINGS TO CHANGE (all settings are integers > 0)
    rects_in_M = 1
    rects_in_N = 1
    seed = 11
################# END OF SETTINGS TO CHANGE
    settings.print_output = True
    settings.save_figure = True
    settings.debug = True

    M, N = chf.generate_random_rectangles(rects_in_M,rects_in_N, seed=seed)

 
    settings.new_pruning_march_2025 = False
    settings.old_pruning = False
    print("\n\n!!!!!")
    print("|  NEW RUN BEGINS  |")
    print("~~~NO PRUNING WHATSOEVER~~~")
    

    if settings.save_figure:
        settings.figure_title = 'M:'+ str(rects_in_M) +  ' N:' + str(rects_in_N) + ' seed:' + str(seed)

        img_path = 'GROUP_FIGS/' + 'm'+ str(rects_in_M) + '_n' + str(rects_in_N) + '_seed' + str(seed) +'.png'
        chf.plot_rectangles(M,N, img_path)

    if settings.print_output:
        print("_____________________________________\nAPPROX\n_____________________________________")
        print('Rects in M: ',rects_in_M)
        print('Rects in N: ',rects_in_N)

    prune_time, approx_time, prune_match_dist, max_dist_critpts, max_grids_lines = chf.to_prune_or_not_to_prune_csv(M,N)

    if settings.print_output:
        print("_____________________________________\nEND\n_____________________________________")

    # only OLD PRUNE now
    settings.old_pruning = True 
    settings.new_pruning_march_2025 = False
    print("~~~ONLY OLD PRUNING~~~")
    if settings.print_output:
        print("_____________________________________\nAPPROX\n_____________________________________")
        print('Rects in M: ',rects_in_M)
        print('Rects in N: ',rects_in_N)

    prune_time, approx_time, prune_match_dist, max_dist_critpts, max_grids_lines = chf.to_prune_or_not_to_prune_csv(M,N)

    if settings.print_output:
        print("_____________________________________\nEND\n_____________________________________")

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

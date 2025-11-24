import sys
from imports import *
import csv
import random
import settings

if __name__ == '__main__':

################# SETTINGS TO CHANGE (all settings are integers > 0)
    rects_in_M = int(sys.argv[1])
    rects_in_N = int(sys.argv[2])
    seed = int(sys.argv[3])
    # only set this to True if you're fixing bad no-prune data
    only_redo_bad_data = False
################# END OF SETTINGS TO CHANGE
    settings.print_output = True
    settings.save_figure = False
    M, N = chf.generate_random_rectangles(rects_in_M,rects_in_N, seed=seed)

    if only_redo_bad_data == False: 
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
    if only_redo_bad_data:
        print("\n\n")
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

    if only_redo_bad_data == False:
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

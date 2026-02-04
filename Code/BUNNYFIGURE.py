import sys
from imports import *
import csv
import random
import settings
import examples as ex
import bunny_003


if __name__ == '__main__':
    print("\n\n!!!!!")
    print("|  NEW RUN BEGINS  |")
    # note: for this we will use the incredibly ridiculously bad coding practice of just overwriting the critical values in the computation. leave M and N at 1 because they don't actually matter, and we want this to go quickly. 
    # (M, N, seed: ints over 1)
    rects_in_M = 1
    rects_in_N = 1
    seed = 11
    settings.save_figure = True
    settings.debug = True
    # this will overwrite the crit vals obtained from M and N in chf.do_all_the_things()

    # # GRAPH ONE: poisson critical values
    # # num of verts to match bunny (or close) : poisson intensity
    # # 4 -> 1.3
    # # 9 -> 2.5
    # # 16 -> 5.5
    # # 24 ! No, 23 9.19
    # # 34 -> 12
    # settings.overwrite_critvals = True
    # poisson_intensity = 12
    # seed = 0
    # critvals, nolub = ex.critvals_poisson(poisson_intensity, seed)
    # settings.critvals_to_overwrite = critvals
    # settings.nolub_to_overwrite = nolub
    # print("NUMBER OF CRITVALS: ", len(critvals))

    # # GRAPH TWO: BUNNY
    # bunnypoints = bunny_003.bunny_34()
    # seed = 4
    # # critvals = nolub here. seems like that is how we did it for the socg sub
    # critvals, nolub = ex.bunny_into_critvals(bunnypoints, seed)
    # settings.overwrite_critvals = True
    # settings.critvals_to_overwrite = critvals
    # settings.nolub_to_overwrite = nolub
    # print("NUMBER OF CRITVALS: ", len(critvals))

    # GRAPH THREE: RANDOM RECTS
    # rects_in_M = 5
    # rects_in_N = 6

    # GRAPH FOUR (redo of stats; random rects)
    # seed: 1,2,3,4,5
    rects_in_M = 2
    rects_in_N = 2
    seed = 5
    print("Seed: ", seed)
  




    # DON'T EDIT AFTER HERE
    M, N = chf.generate_random_rectangles(rects_in_M,rects_in_N, seed=seed)
 
    # ALL PRUNE now
    settings.old_pruning = True 
    settings.new_pruning_march_2025 = True 
    print("~~~ALL (including NEW) PRUNING~~~")
    print("_____________________________________\nAPPROX\n_____________________________________")
    print('Rects in M: ',rects_in_M)
    print('Rects in N: ',rects_in_N)

    prune_time, approx_time, prune_match_dist, max_dist_critpts, max_grids_lines = chf.to_prune_or_not_to_prune_csv(M,N)

    print("_____________________________________\nEND\n_____________________________________")

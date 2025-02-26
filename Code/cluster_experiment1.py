import sys
# caution: path[0] is reserved for script path (or '' in REPL)
from imports import *
import csv
import random
import settings

"""This is the code to run experiment 1 in the cluster. 
We compute the number of lines computed by our algorithm for the matching distance 

a: we do the experiment with balanced 
b: we do the experiment with different numbers of rectangles in M and N increasing the total number 
"""


def make_csv(file_path):
    data = {
            "Label":None,
        "rects in M":None,
        "rects in N":None,
        "seed":None,
        "number of lines":None
        }

    # # FIRST TIME USAGE ONLY
    # # a for append or w for write
    with open(file_path, 'w') as csv_file:  
        writer = csv.writer(csv_file)
        # thing.items() is the struct above
        for key, value in data.items():
            writer.writerow([key, value])



# Only call the greeter when run as
# a script (with python mymodule.py)
if __name__ == '__main__':

    # false by default but makes it easy to make new csv
    first_time = False 
    file_path = '../output/experiment_1_balanced.csv'
    

    if first_time:
        make_csv(file_path)

    else:
        for i in range(1,10): # default (1,2) for non-cluster use

            for j in range(1): 
                ## run the computation with same number of rectangles several times 
                # Balanced number of recangles in M and N
                rects_in_M = i
                rects_in_N = i 
                seed = random.randint(0, 100)

                ## make random rectangles 
                M, N = chf.generate_random_rectangles(rects_in_M,rects_in_N, seed=seed)

                if settings.save_figure:
                    img_path = '../output/cluster/img' + str(i) +'.png'
                    chf.plot_rectangles(M,N, img_path)

                if settings.print_output:
                    print('Rects in M: ',rects_in_M)
                    print('Rects in N: ',rects_in_N)
                # prune_time, no_prune_time, approx_time, prune_match_dist, no_prune_match_dist, max_dist_critpts, max_grids_lines = chf.to_prune_or_not_to_prune_csv(M,N)
                num_lines = chf.experiment_1(M,N)

                data = {
                    "Label":"Run " + str(i),
                "rects in M": rects_in_M,
                "rects in N": rects_in_N,
                "seed": seed,
                "number of lines": num_lines
                }

                chf.append_to_csv(file_path, data) ## There is a bug here, when I re run the experiment, it replaces the already existing runs with the new ones... 

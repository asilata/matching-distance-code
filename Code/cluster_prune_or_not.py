import sys
# caution: path[0] is reserved for script path (or '' in REPL)
from imports import *
import csv
import random
import settings


def make_csv(file_path):
    data = {
            "Label":None,
        "rects in M":None,
        "rects in N":None,
        "seed":None,
        "Prune Matching dist":None,
        # "No Prune Matching dist":None,
        # "Approx Matching dist through cps":None,
        "Approx Matching dist grid":None,
        "Time Prune":None,
        # "Time No Prune":None,
        "Time Approx":None,

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
    print("\n\nNEW RUN BEGINS")
    # false by default but makes it easy to make new csv
    first_time = False
    file_path = '../output/cluster/output.csv'
    

    if first_time:
        make_csv(file_path)

    else:
        # for i in range(1,2):
            i = 1
            # default (1,2) for non-cluster use
            rects_in_M = 2
            rects_in_N = 2
            seed = random.randint(0, 100)
            seed = 3

            settings.new_pruning_march_2025 = True

            #  one rectangle from create_random_rectangle: 
            #  M and N are just lists of random rects
            # corners 

            # an example
            # 0,0 to 4,4 M 
            # 2,2 to 6,6 N
            # [(tr_x, tr_y), (bl_x, bl_y)]
            # M 0,7 x 0,8 and 0,7 x 4,11
            # M1 x,y coords: (0,4) to (7,11)
            # M2 x,y coords: (0,0) to (7,8)
            # N 0,7 x 4,8 and 0,7 x 0,11
            # N1 x,y coords: (0,0) to (7,11)
            # N2 x,y coords: (0,4) to (7,8)

            # [(tr_x, tr_y), (bl_x, bl_y)]

            # # uncomment below for an example
            # rects_in_M =  2
            # rects_in_N = 2
            # M = [[(7,11), (0,4)],[(7,8), (0,0)]]
            # N = [[(7,11), (0,0)], [(7,8), (0,4)]]
            

            M, N = chf.generate_random_rectangles(rects_in_M,rects_in_N, seed=seed)

            if settings.save_figure:
                img_path = '../output/cluster/img' + str(i) +'.png'
                chf.plot_rectangles(M,N, img_path)

            if settings.print_output:
                print("_____________________________________\nAPPROX\n_____________________________________")
                print('Rects in M: ',rects_in_M)
                print('Rects in N: ',rects_in_N)
            # prune_time, no_prune_time, approx_time, prune_match_dist, no_prune_match_dist, max_dist_critpts, max_grids_lines = chf.to_prune_or_not_to_prune_csv(M,N)
            prune_time, approx_time, prune_match_dist, max_dist_critpts, max_grids_lines, _ = chf.to_prune_or_not_to_prune_csv(M,N)

            # print("approx time: ", approx_time)
            # print("approx match dist grid: ", max_grids_lines)
            data = {
                "Label":"Run " + str(i),
            "rects in M": rects_in_M,
            "rects in N": rects_in_N,
            "seed": seed,
            "Prune Matching dist": prune_match_dist,
            # "No Prune Matching dist": no_prune_match_dist,
            # "Approx Matching dist through cps": max_dist_critpts,
            "Approx Matching dist grid":max_grids_lines ,
            "Time Prune" :prune_time,
            # "Time No Prune": no_prune_time,
            "Time Approx": approx_time

            }

            chf.append_to_csv(file_path, data)
            if settings.print_output:
                print("_____________________________________\nEND\n_____________________________________")

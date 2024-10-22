import sys
# caution: path[0] is reserved for script path (or '' in REPL)
from imports import *
import csv
import random


def make_csv():
    data = {
            "Label":None,
        "rects in M":None,
        "rects in N":None,
        "seed":None,
        "Prune Matching dist":None,
        "No Prune Matching dist":None,
        "Approx Matching dist through cps":None,
        "Approx Matching dist grid":None,
        "Time Prune":None,
        "Time No Prune":None,
        "Time Approx":None,

        }

    # # FIRST TIME USAGE ONLY
    # # a for append or w for write
    with open('../output/cluster/output.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        # thing.items() is the struct above
        for key, value in data.items():
            writer.writerow([key, value])



# Only call the greeter when run as
# a script (with python mymodule.py)
if __name__ == '__main__':

    # false by default but makes it easy to make new csv
    first_time = False

    if first_time:
        make_csv()

    else:
        for i in range(1,2):
            # default (1,2) for non-cluster use
            rects_in_M = i
            rects_in_N = 1
            seed = random.randint(0, 100)
            file_path = '../output/cluster/output.csv'
            img_path = '../output/cluster/img' + str(i) +'.png'


            M, N = chf.generate_random_rectangles(rects_in_M,rects_in_N, seed=seed)

            chf.plot_rectangles(M,N, img_path)
            prune_time, no_prune_time, approx_time, prune_match_dist, no_prune_match_dist, max_dist_critpts, max_grids_lines = chf.to_prune_or_not_to_prune_csv(M,N)

            data = {
                "Label":"Run " + str(i),
            "rects in M": rects_in_M,
            "rects in N": rects_in_N,
            "seed": seed,
            "Prune Matching dist": prune_match_dist,
            "No Prune Matching dist": no_prune_match_dist,
            "Approx Matching dist through cps": max_dist_critpts,
            "Approx Matching dist grid":max_grids_lines ,
            "Time Prune" :prune_time,
            "Time No Prune": no_prune_time,
            "Time Approx": approx_time

            }

            chf.append_to_csv(file_path, data)

import sys
import argparse
from imports import *
import csv
import random
import settings

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Compute matching distance for random rectangle modules.")
    parser.add_argument("M", nargs="?", type=int, default=None, help="Number of rectangles in M")
    parser.add_argument("N", nargs="?", type=int, default=None, help="Number of rectangles in N")
    parser.add_argument("seed", nargs="?", type=int, default=None, help="Random seed")
    parser.add_argument("--no-figure", action="store_true", help="Skip figure generation")
    args = parser.parse_args()

    ################# SETTINGS TO CHANGE (all settings are integers > 0)
    rects_in_M = args.M if args.M is not None else 2
    rects_in_N = args.N if args.N is not None else 1
    seed = args.seed if args.seed is not None else 13
    ################# END OF SETTINGS TO CHANGE
    settings.save_figure = not args.no_figure
    settings.debug = False

    M, N = chf.generate_random_rectangles(rects_in_M, rects_in_N, seed=seed)

    settings.section5_pruning = False
    settings.section4_pruning = False
    print("\n\n!!!!!")
    print("|  NEW RUN BEGINS  |")
    # print("~~~NO PRUNING WHATSOEVER~~~")

    # TODO: save best lines from all outputs overlaid on figure
    if settings.save_figure:
        settings.figure_title = (
            "M:" + str(rects_in_M) + " N:" + str(rects_in_N) + " seed:" + str(seed)
        )

        img_path = (
            "DEBUG_FIGS/"
            + "m"
            + str(rects_in_M)
            + "_n"
            + str(rects_in_N)
            + "_seed"
            + str(seed)
            + ".png"
        )
        chf.plot_rectangles(M, N, img_path)
        if settings.debug:
            debug_M = M
            debug_N = N
            debug_seed = seed
            # go plot the figure in place with slopes

    # print(
    #     "_____________________________________\nAPPROX\n_____________________________________"
    # )
    # print("Rects in M: ", rects_in_M)
    # print("Rects in N: ", rects_in_N)

    # (
    #     prune_time,
    #     approx_time,
    #     prune_match_dist,
    #     max_dist_critpts,
    #     max_grids_lines,
    #     best_line,
    # ) = chf.compute_distances(M, N)

    # print(
    #     "_____________________________________\nEND\n_____________________________________"
    # )

    # # only OLD PRUNE now
    # settings.section4_pruning = True
    # settings.section5_pruning = False
    # print("~~~ONLY OLD PRUNING~~~")
    # print(
    #     "_____________________________________\nAPPROX\n_____________________________________"
    # )
    # print("Rects in M: ", rects_in_M)
    # print("Rects in N: ", rects_in_N)

    # (
    #     prune_time,
    #     approx_time,
    #     prune_match_dist,
    #     max_dist_critpts,
    #     max_grids_lines,
    #     best_line,
    # ) = chf.compute_distances(M, N)

    # print(
    #     "_____________________________________\nEND\n_____________________________________"
    # )

    # ALL PRUNE now
    settings.section4_pruning = True
    settings.section5_pruning = True
    print("~~~ALL (including NEW) PRUNING~~~")
    print(
        "_____________________________________\nAPPROX\n_____________________________________"
    )
    print("Rects in M: ", rects_in_M)
    print("Rects in N: ", rects_in_N)

    (
        prune_time,
        approx_time,
        prune_match_dist,
        max_dist_critpts,
        max_grids_lines,
        best_line,
    ) = chf.compute_distances(M, N)

    print(
        "_____________________________________\nEND\n_____________________________________"
    )

    # Save figure with best line and distance annotations
    if settings.save_figure and best_line is not None:
        result_path = img_path.replace(".png", "_result.png")  # type: ignore
        chf.save_result_figure(
            M, N, best_line,
            max_dist_critpts, max_grids_lines, prune_match_dist,
            settings.figure_title, result_path,
        )
        print(f"Saved result figure to {result_path}")

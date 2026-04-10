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

    settings.new_pruning_march_2025 = False
    settings.old_pruning = False
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
    # ) = chf.to_prune_or_not_to_prune_csv(M, N)

    # print(
    #     "_____________________________________\nEND\n_____________________________________"
    # )

    # # only OLD PRUNE now
    # settings.old_pruning = True
    # settings.new_pruning_march_2025 = False
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
    # ) = chf.to_prune_or_not_to_prune_csv(M, N)

    # print(
    #     "_____________________________________\nEND\n_____________________________________"
    # )

    # ALL PRUNE now
    settings.old_pruning = True
    settings.new_pruning_march_2025 = True
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
    ) = chf.to_prune_or_not_to_prune_csv(M, N)

    print(
        "_____________________________________\nEND\n_____________________________________"
    )

    # Save figure with best line and distance annotations
    if settings.save_figure and best_line is not None:
        from matplotlib import patches

        fig, ax = plt.subplots()

        # Plot rectangles in M (red) with corner points and coordinates
        for rect in M:
            tr, bl = rect
            tl = (bl[0], tr[1])
            br = (tr[0], bl[1])
            width = tr[0] - bl[0]
            height = tr[1] - bl[1]
            ax.add_patch(
                patches.Rectangle(
                    bl,
                    width,
                    height,
                    linewidth=1,
                    edgecolor="r",
                    facecolor="red",
                    alpha=0.3,
                )
            )
            for corner in [bl, br, tl, tr]:
                ax.plot(corner[0], corner[1], "r.", markersize=5)
                ax.annotate(
                    f"({corner[0]:.1f}, {corner[1]:.1f})",
                    corner,
                    textcoords="offset points",
                    xytext=(4, 4),
                    fontsize=5,
                    color="darkred",
                )

        # Plot rectangles in N (blue) with corner points and coordinates
        for rect in N:
            tr, bl = rect
            tl = (bl[0], tr[1])
            br = (tr[0], bl[1])
            width = tr[0] - bl[0]
            height = tr[1] - bl[1]
            ax.add_patch(
                patches.Rectangle(
                    bl,
                    width,
                    height,
                    linewidth=1,
                    edgecolor="b",
                    facecolor="blue",
                    alpha=0.3,
                )
            )
            for corner in [bl, br, tl, tr]:
                ax.plot(corner[0], corner[1], "b.", markersize=5)
                ax.annotate(
                    f"({corner[0]:.1f}, {corner[1]:.1f})",
                    corner,
                    textcoords="offset points",
                    xytext=(4, -8),
                    fontsize=5,
                    color="darkblue",
                )

        # Draw the best line: L(s) = (m1, m2)*s + (b1, b2)
        m1, m2 = best_line.m
        b1, b2 = best_line.b
        t_min, t_max = -5, 25
        x_vals = [m1 * t + b1 for t in [t_min, t_max]]
        y_vals = [m2 * t + b2 for t in [t_min, t_max]]
        ax.plot(x_vals, y_vals, "k-", linewidth=1.5, label="Best line")
        # Line equation annotation along the line
        t_mid = (t_min + t_max) / 2 * 0.4
        x_mid = m1 * t_mid + b1
        y_mid = m2 * t_mid + b2
        slope = m2 / m1
        y_int = b2 - m2 * b1 / m1
        line_eq = f'$y = {slope:.2f}x {"+" if y_int >= 0 else "-"} {abs(y_int):.2f}$'
        ax.annotate(
            line_eq,
            (x_mid, y_mid),
            textcoords="offset points",
            xytext=(8, -12),
            fontsize=6,
            color="black",
            fontstyle="italic",
        )

        # Annotation text
        text = (
            f"Approx (crit pts): {max_dist_critpts:.3f}\n"
            f"Approx (grid): {max_grids_lines:.3f}\n"
            f"Exact: {prune_match_dist:.3f}"
        )
        ax.text(
            0.98,
            0.02,
            text,
            transform=ax.transAxes,
            fontsize=8,
            verticalalignment="bottom",
            horizontalalignment="right",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.4),
        )

        # Set limits and labels
        all_x = [rect[1][0] for rect in M + N] + [rect[0][0] for rect in M + N]
        all_y = [rect[1][1] for rect in M + N] + [rect[0][1] for rect in M + N]
        margin = 2
        ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
        ax.set_ylim(min(all_y) - margin, max(all_y) + margin)
        ax.set_aspect("equal")
        ax.set_title(settings.figure_title)

        import matplotlib.lines as mlines

        legend_M = mlines.Line2D([], [], color="red", marker="D", ls="", label="M")
        legend_N = mlines.Line2D([], [], color="blue", marker="D", ls="", label="N")
        legend_line = mlines.Line2D([], [], color="black", ls="-", label="Best line")
        leg = ax.legend(handles=[legend_M, legend_N, legend_line], fontsize=7)
        leg.get_frame().set_alpha(0.4)

        result_path = img_path.replace(".png", "_result.png")  # type: ignore
        fig.savefig(result_path, format="png", dpi=250)
        print(f"Saved result figure to {result_path}")

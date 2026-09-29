"""
Generate fresh 1:1 (M=1, N=1) matching-distance experiment outputs.

Each run computes the exact matching distance (with full pruning) plus the two
approximations and the rectangle corners, for a block of seeds. Multiple people
can run disjoint seed ranges and combine the resulting CSVs afterwards.

Usage:
    python3 DEBUG_1v1.py --start-seed 0 --count 100 --name barbara
    python3 DEBUG_1v1.py --start-seed 1000 --count 100 --name robyn

Output: DEBUG_1v1_OUTPUT/debug_1v1_{name}_seed{start}-{end}.csv
"""

import os
import io
import csv
import argparse
import contextlib

import settings
import cleanup_helper_funcs as chf

OUTPUT_DIR = os.path.join(settings.output_dir, "batch_1v1")
FIGS_DIR = os.path.join(OUTPUT_DIR, "figs")
TOLERANCE = 0.0015  # a unicorn = exact differs from both approximations by more than this

FIELDNAMES = [
    "M", "N", "seed", "config_type",
    "exact", "approx_grid", "approx_crit_pts", "is_unicorn",
    "exact_time", "approx_time",
    "a_bl_M_x", "a_bl_M_y",
    "b_tr_M_x", "b_tr_M_y",
    "c_bl_N_x", "c_bl_N_y",
    "d_tr_N_x", "d_tr_N_y",
]


def classify_config(M, N):
    """Classify the geometric relationship between the 1:1 rectangles M and N.

    M = [b_tr_M, a_bl_M], N = [d_tr_N, c_bl_N] (each rect is [(tr), (bl)]).
    """
    tr_M, bl_M = M[0][0], M[0][1]
    tr_N, bl_N = N[0][0], N[0][1]
    a_x, a_y = bl_M
    b_x, b_y = tr_M
    c_x, c_y = bl_N
    d_x, d_y = tr_N

    x_overlap = a_x < d_x and c_x < b_x
    y_overlap = a_y < d_y and c_y < b_y
    M_in_N = c_x <= a_x and c_y <= a_y and b_x <= d_x and b_y <= d_y
    N_in_M = a_x <= c_x and a_y <= c_y and d_x <= b_x and d_y <= b_y

    if M_in_N or N_in_M:
        return "nested"
    if x_overlap and y_overlap:
        return "overlapping"
    if x_overlap and not y_overlap:
        return "disjoint_stacked"
    if y_overlap and not x_overlap:
        return "disjoint_sidebyside"
    return "disjoint_diagonal"


def compute_row(seed, name, save_figure):
    """Run the matching distance computation for a single 1:1 seed.

    Optionally saves a figure to DEBUG_1v1_OUTPUT/figs/. Returns the CSV row dict.
    """
    M, N = chf.generate_random_rectangles(1, 1, seed=seed)
    # Silence the unconditional prints inside compute_matching_dist.
    # to_prune_or_not_to_prune_csv returns:
    #   (exact_time, approx_time, exact, crit_approx, grid_approx, best_line)
    with contextlib.redirect_stdout(io.StringIO()):
        exact_time, approx_time, exact, crit_approx, grid_approx, best_line = chf.to_prune_or_not_to_prune_csv(M, N)

    # M[0] = [(tr_x, tr_y), (bl_x, bl_y)]
    bl_M, tr_M = M[0][1], M[0][0]
    bl_N, tr_N = N[0][1], N[0][0]
    config_type = classify_config(M, N)
    is_unicorn = (
        abs(exact - crit_approx) > TOLERANCE and abs(exact - grid_approx) > TOLERANCE
    )

    if save_figure and best_line is not None:
        os.makedirs(FIGS_DIR, exist_ok=True)
        fig_path = os.path.join(FIGS_DIR, f"debug_1v1_{name}_seed{seed}_{config_type}.png")
        title = f"M:1 N:1 seed:{seed} ({config_type})"
        chf.save_result_figure(M, N, best_line, crit_approx, grid_approx, exact, title, fig_path)

    return {
        "M": 1, "N": 1, "seed": seed,
        "config_type": config_type,
        "exact": f"{exact:.6f}",
        "approx_grid": f"{grid_approx:.6f}",
        "approx_crit_pts": f"{crit_approx:.6f}",
        "is_unicorn": is_unicorn,
        "exact_time": f"{exact_time:.3f}",
        "approx_time": f"{approx_time:.3f}",
        "a_bl_M_x": f"{bl_M[0]:.9f}", "a_bl_M_y": f"{bl_M[1]:.9f}",
        "b_tr_M_x": f"{tr_M[0]:.9f}", "b_tr_M_y": f"{tr_M[1]:.9f}",
        "c_bl_N_x": f"{bl_N[0]:.9f}", "c_bl_N_y": f"{bl_N[1]:.9f}",
        "d_tr_N_x": f"{tr_N[0]:.9f}", "d_tr_N_y": f"{tr_N[1]:.9f}",
    }


def done_seeds(output_path):
    """Return the set of seeds already present in an existing output file."""
    if not os.path.exists(output_path):
        return set()
    done = set()
    with open(output_path, newline="") as f:
        for row in csv.DictReader(f):
            try:
                done.add(int(row["seed"]))
            except (KeyError, ValueError):
                continue
    return done


def main():
    parser = argparse.ArgumentParser(
        description="Generate fresh 1:1 matching-distance experiment outputs."
    )
    parser.add_argument("--start-seed", type=int, default=0, help="First seed (default: 0)")
    parser.add_argument("--count", type=int, default=100, help="Number of seeds (default: 100)")
    parser.add_argument(
        "--name", type=str, default="batch",
        help="Tag for the output filename (default: your username)",
    )
    parser.add_argument(
        "--figures", action="store_true",
        help="Save a figure per seed to DEBUG_1v1_OUTPUT/figs/ (off by default; slow for large batches)",
    )
    args = parser.parse_args()

    # Full pruning for speed; quiet, no figures.
    settings.old_pruning = True
    settings.new_pruning_march_2025 = True
    settings.save_figure = False
    settings.print_output = False
    settings.actually_compute_matching_distance = True

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    end_seed = args.start_seed + args.count - 1
    output_path = os.path.join(
        OUTPUT_DIR, f"debug_1v1_{args.name}_seed{args.start_seed}-{end_seed}.csv"
    )

    already = done_seeds(output_path)
    file_exists = os.path.exists(output_path)
    if already:
        print(f"Resuming: {len(already)} of {args.count} seeds already done in {os.path.basename(output_path)}")

    seeds = [s for s in range(args.start_seed, end_seed + 1) if s not in already]

    with open(output_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
            f.flush()

        for i, seed in enumerate(seeds):
            row = compute_row(seed, args.name, save_figure=args.figures)
            writer.writerow(row)
            f.flush()
            print(
                f"[{i+1}/{len(seeds)}] seed {seed} ({row['config_type']}): "
                f"exact={row['exact']} grid={row['approx_grid']} crit={row['approx_crit_pts']}"
            )

    print(f"\nDone. Results in {output_path}")


if __name__ == "__main__":
    main()

"""
Compare old (pre-bugfix) matching distance results from dardel runs
against the current (debugged) code.

Usage:
    python3 dardel/compare_old_new.py          # re-run all unicorns + 10 random non-unicorns
    python3 dardel/compare_old_new.py --n 5    # re-run all unicorns + 5 random non-unicorns
    python3 dardel/compare_old_new.py --n 0    # only parse old files, no re-runs
"""

import os
import sys
import re
import csv
import random
import subprocess
import argparse
import glob

# Allow importing from Code/ when running from dardel/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import cleanup_helper_funcs as chf  # noqa: E402

EXPERIMENTS_DIR = os.path.join(os.path.dirname(__file__), "experiments_output")
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), "new_vs_old.csv")
TOLERANCE = 0.0015  # values printed to 3 decimal places


def parse_txt_file(filepath):
    """Parse a dardel experiment txt file. Returns dict or None if unparseable."""
    with open(filepath) as f:
        content = f.read()

    if not content.strip():
        return None

    # Find the ALL PRUNING section
    marker = "~~~ALL (including NEW) PRUNING~~~"
    idx = content.find(marker)
    if idx == -1:
        return None
    section = content[idx:]

    crit_match = re.search(
        r"Maximum distance for lines through critical points:\s+([\d.]+)", section
    )
    grid_match = re.search(
        r"Maximum distance computed for grid of lines:\s+([\d.]+)", section
    )
    exact_match = re.search(r"Matching dist:\s+([\d.]+)", section)

    if not all([crit_match, grid_match, exact_match]):
        return None

    return {
        "crit_approx": float(crit_match.group(1)),  # type: ignore
        "grid_approx": float(grid_match.group(1)),  # type: ignore
        "exact": float(exact_match.group(1)),  # type: ignore
    }


def parse_debug_output(output):
    """Parse the stdout of DEBUG.py. Returns dict or None."""
    marker = "~~~ALL (including NEW) PRUNING~~~"
    idx = output.find(marker)
    if idx == -1:
        return None
    section = output[idx:]

    crit_match = re.search(
        r"Maximum distance for lines through critical points:\s+([\d.]+)", section
    )
    grid_match = re.search(
        r"Maximum distance computed for grid of lines:\s+([\d.]+)", section
    )
    exact_match = re.search(r"Matching dist:\s+([\d.]+)", section)

    if not all([crit_match, grid_match, exact_match]):
        return None

    return {
        "crit_approx": float(crit_match.group(1)),  # type: ignore
        "grid_approx": float(grid_match.group(1)),  # type: ignore
        "exact": float(exact_match.group(1)),  # type: ignore
    }


def is_unicorn(result):
    """A unicorn is a result where exact differs from both approximations."""
    return (
        abs(result["exact"] - result["crit_approx"]) > TOLERANCE
        and abs(result["exact"] - result["grid_approx"]) > TOLERANCE
    )


def run_debug(m, n, seed, save_figures=False):
    """Run DEBUG.py with given parameters and return parsed output."""
    cmd = ["python3", "DEBUG.py", str(m), str(n), str(seed)]
    if not save_figures:
        cmd.append("--no-figure")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,
            cwd=os.path.join(os.path.dirname(__file__), ".."),
        )
        return parse_debug_output(result.stdout)
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT: {m}_{n}_{seed}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Compare old vs new matching distances."
    )
    parser.add_argument(
        "--n",
        type=int,
        default=10,
        help="Max total cases to re-run (default: 10)",
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Random seed for sampling non-unicorns"
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--just-unicorns", action="store_true",
        help="Only run unicorns (skip non-unicorns)",
    )
    mode.add_argument(
        "--no-unicorns", action="store_true",
        help="Only run non-unicorns (skip unicorns)",
    )
    mode.add_argument(
        "--only-1-v-1", action="store_true",
        help="Only run M=1 N=1 cases (fast; ~1 sec each)",
    )
    parser.add_argument(
        "--corners-to-csv", action="store_true",
        help="Add rectangle corner coordinates to CSV (requires --only-1-v-1)",
    )
    parser.add_argument(
        "--save-figures", action="store_true",
        help="Save figures to DEBUG_FIGS/ for each run (slower)",
    )
    args = parser.parse_args()

    if args.corners_to_csv and not args.only_1_v_1:
        parser.error("--corners-to-csv requires --only-1-v-1")

    # Step 1: Parse all old txt files
    txt_files = glob.glob(os.path.join(EXPERIMENTS_DIR, "*.txt"))
    entries = []

    for filepath in sorted(txt_files):
        basename = os.path.basename(filepath)

        # Skip experiment/corrected files
        if "experiment" in basename.lower() or "corrected" in basename.lower():
            continue

        # Parse M_N_seed from filename
        name = basename.replace(".txt", "")
        parts = name.split("_")
        if len(parts) != 3:
            continue
        try:
            m, n, seed = int(parts[0]), int(parts[1]), int(parts[2])
        except ValueError:
            continue

        result = parse_txt_file(filepath)
        if result is None:
            continue

        unicorn = is_unicorn(result)
        entries.append(
            {
                "M": m,
                "N": n,
                "seed": seed,
                "unicorn": unicorn,
                "old_crit_approx": result["crit_approx"],
                "old_grid_approx": result["grid_approx"],
                "old_exact": result["exact"],
            }
        )

    unicorns = [e for e in entries if e["unicorn"]]
    non_unicorns = [e for e in entries if not e["unicorn"]]

    print(
        f"Parsed {len(entries)} files: {len(unicorns)} unicorns, {len(non_unicorns)} non-unicorns"
    )

    # Step 2: Select which to re-run and choose output file
    suffix = f"_n{args.n}_seed{args.seed}.csv"
    if args.just_unicorns:
        to_run = unicorns[: args.n]
        output_csv = os.path.join(os.path.dirname(__file__), f"new_vs_old_unicorns{suffix}")
        print(f"Will re-run {len(to_run)} unicorns")
    elif args.no_unicorns:
        rng = random.Random(args.seed)
        sample_size = min(args.n, len(non_unicorns))
        to_run = rng.sample(non_unicorns, sample_size)
        output_csv = os.path.join(os.path.dirname(__file__), f"new_vs_old_non_unicorns{suffix}")
        print(f"Will re-run {len(to_run)} non-unicorns")
    elif args.only_1_v_1:
        one_v_one = [e for e in entries if e["M"] == 1 and e["N"] == 1]
        to_run = one_v_one[: args.n]
        output_csv = os.path.join(os.path.dirname(__file__), f"new_vs_old_1v1{suffix}")
        print(f"Will re-run {len(to_run)} 1v1 cases (out of {len(one_v_one)} total)")
    else:
        to_run = unicorns[: args.n]
        remaining = args.n - len(to_run)
        if remaining > 0 and non_unicorns:
            rng = random.Random(args.seed)
            sample_size = min(remaining, len(non_unicorns))
            to_run += rng.sample(non_unicorns, sample_size)
        output_csv = os.path.join(os.path.dirname(__file__), f"new_vs_old{suffix}")
        n_unicorns_to_run = min(len(unicorns), args.n)
        print(f"Will re-run {len(to_run)} cases ({n_unicorns_to_run} unicorns + {len(to_run) - n_unicorns_to_run} non-unicorns)")

    if args.n == 0:
        # Just print unicorn summary, no re-runs
        print("\nUnicorns found:")
        for e in unicorns:
            print(
                f"  {e['M']}_{e['N']}_{e['seed']}: crit={e['old_crit_approx']:.3f}, grid={e['old_grid_approx']:.3f}, exact={e['old_exact']:.3f}"
            )
        return

    def corner_columns(m, n, seed):
        """For 1v1 cases, return dict of corner coords with 9-digit precision."""
        M, N = chf.generate_random_rectangles(m, n, seed=seed)
        # M[0] = [(tr_x, tr_y), (bl_x, bl_y)]
        bl_M, tr_M = M[0][1], M[0][0]
        bl_N, tr_N = N[0][1], N[0][0]
        return {
            "a_bl_M_x": f"{bl_M[0]:.9f}", "a_bl_M_y": f"{bl_M[1]:.9f}",
            "b_tr_M_x": f"{tr_M[0]:.9f}", "b_tr_M_y": f"{tr_M[1]:.9f}",
            "c_bl_N_x": f"{bl_N[0]:.9f}", "c_bl_N_y": f"{bl_N[1]:.9f}",
            "d_tr_N_x": f"{tr_N[0]:.9f}", "d_tr_N_y": f"{tr_N[1]:.9f}",
        }

    # Step 3: Run DEBUG.py for each selected case
    rows = []
    for i, entry in enumerate(to_run):
        m, n, seed = entry["M"], entry["N"], entry["seed"]
        label = "UNICORN" if entry["unicorn"] else "non-unicorn"
        print(
            f"[{i+1}/{len(to_run)}] Running {m}_{n}_{seed} ({label})...",
            end=" ",
            flush=True,
        )

        new_result = run_debug(m, n, seed, save_figures=args.save_figures)

        if new_result is None:
            print("FAILED")
            row = {
                "M": m,
                "N": n,
                "seed": seed,
                "was_unicorn": entry["unicorn"],
                "is_unicorn": "",
                "old_exact": entry["old_exact"],
                "new_exact": "",
                "new_same_as_old": "",
                "grid_approx": "",
                "crit_pts_approx": "",
            }
            if args.corners_to_csv:
                row.update(corner_columns(m, n, seed))
            rows.append(row)
            continue

        same = abs(new_result["exact"] - entry["old_exact"]) < TOLERANCE
        new_is_unicorn = is_unicorn(new_result)
        print(
            f"old={entry['old_exact']:.3f} new={new_result['exact']:.3f} {'SAME' if same else 'CHANGED'}"
        )

        row = {
            "M": m,
            "N": n,
            "seed": seed,
            "was_unicorn": entry["unicorn"],
            "is_unicorn": new_is_unicorn,
            "old_exact": entry["old_exact"],
            "new_exact": new_result["exact"],
            "new_same_as_old": same,
            "grid_approx": new_result["grid_approx"],
            "crit_pts_approx": new_result["crit_approx"],
        }
        if args.corners_to_csv:
            row.update(corner_columns(m, n, seed))
        rows.append(row)

    # Step 4: Write CSV
    fieldnames = [
        "M",
        "N",
        "seed",
        "was_unicorn",
        "is_unicorn",
        "old_exact",
        "new_exact",
        "new_same_as_old",
        "grid_approx",
        "crit_pts_approx",
    ]
    if args.corners_to_csv:
        fieldnames += [
            "a_bl_M_x", "a_bl_M_y",
            "b_tr_M_x", "b_tr_M_y",
            "c_bl_N_x", "c_bl_N_y",
            "d_tr_N_x", "d_tr_N_y",
        ]
    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nResults written to {output_csv}")

    # Summary
    changed = [r for r in rows if r["new_same_as_old"] is False]
    if changed:
        print(f"\n{len(changed)} results CHANGED:")
        for r in changed:
            print(
                f"  {r['M']}_{r['N']}_{r['seed']}: old={r['old_exact']}, new={r['new_exact']}"
            )
    else:
        print("\nAll re-run results match the old values.")


if __name__ == "__main__":
    main()

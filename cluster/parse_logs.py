"""
Parse the logs of `run_example.py --pruning compare --verbose` into one CSV row per
(M, N, seed, pruning variant), with the columns used for Figures 9-12 of the paper.

    python cluster/parse_logs.py LOG_DIR -o timings.csv

Log files are named M_N_seed.txt (or .out); the seed is taken from the file name.
"""
import argparse
import csv
import glob
import os
import re

COLUMNS = ["M", "N", "seed", "match", "crit_pt_lines_counted", "time_crit_pts", "exact_lines_counted",
           "time_bneck", "time_switch", "time_match_dist", "total_exact_time", "prune"]

PATTERNS = {
    "M": (r"Rects in M:\s*(\d+)", int),
    "N": (r"Rects in N:\s*(\d+)", int),
    "crit_point_dist": (r"Maximum distance for lines through critical points:\s*([\d.]+)", float),
    "grid_dist": (r"Maximum distance computed for grid of lines:\s*([\d.]+)", float),
    "exact_dist": (r"Matching dist:\s*([\d.]+)", float),
    "crit_pt_lines_counted": (r"Lines counted crit pts:\s*(\d+)", int),
    "time_crit_pts": (r"Time to get approx. from crit pts:\s*([\d.]+)", float),
    "exact_lines_counted": (r"Lines counted:\s*(\d+)", int),
    "time_bneck": (r"Time to compute bottleneck dists:\s*([\d.]+)", float),
    "time_switch": (r"Time to compute switch pts:\s*([\d.]+)", float),
    "time_match_dist": (r"Time to compute match dist:\s*([\d.]+)", float),
    "total_exact_time": (r"Total time elapsed in exact computation:\s*([\d.]+)", float),
}


def parse_log(path):
    """Rows (dicts with COLUMNS) for every pruning section of one log file."""
    content = open(path).read()
    seed = int(os.path.splitext(os.path.basename(path))[0].split("_")[-1])
    sections = re.split(r"~~~(.*?)~~~", content)  # [before, header1, body1, header2, body2, ...]
    rows = []
    for i in range(1, len(sections), 2):
        body = sections[i + 1]
        values = {}
        for key, (pattern, cast) in PATTERNS.items():
            m = re.search(pattern, body)
            if m:
                values[key] = cast(m.group(1))
        if "exact_dist" not in values:
            continue
        agree = values.get("crit_point_dist") == values.get("grid_dist") == values["exact_dist"]
        row = {c: values.get(c, "") for c in COLUMNS}
        row.update(seed=seed, prune=sections[i].strip(),
                   match="yes" if agree else f"crit_point_dist: {values.get('crit_point_dist')}, "
                                             f"grid_dist: {values.get('grid_dist')}, exact_dist: {values['exact_dist']}")
        rows.append(row)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("log_dir")
    parser.add_argument("-o", "--output", default="timings.csv")
    args = parser.parse_args()
    files = sorted(glob.glob(os.path.join(args.log_dir, "*.txt")) + glob.glob(os.path.join(args.log_dir, "*.out")))
    rows = [row for f in files for row in parse_log(f)]
    with open(args.output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} rows from {len(files)} log files written to {args.output}")


if __name__ == "__main__":
    main()

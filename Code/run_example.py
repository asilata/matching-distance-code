"""
Compute the matching distance between two rectangle-decomposable persistence modules.

    python Code/run_example.py --M 2 --N 1 --seed 13             random modules
    python Code/run_example.py --toy                              the paper's small example
    python Code/run_example.py --example 2.13                     Examples 2.12-2.14 of arXiv:2210.12868
    python Code/run_example.py --M 2 --N 2 --seed 3 --pruning compare

Prints the two approximations and the exact matching distance.  --pruning chooses which
candidate switch points are discarded: none, section4, all (Sections 4 and 5, the default),
or compare to run all three and tabulate them.  --figure saves the modules and the optimal
line, --plot-candidates the candidate switch points of each algorithm, under output/figures/
(or --out).  --verbose shows the pipeline's own progress output, in the log format that
cluster/parse_logs.py reads.
"""
import argparse
import os

import settings
import cleanup_helper_funcs as chf
from experiment import PRUNING, add_module_args, load_modules, run_one


def describe_line(line):
    return f"direction ({line.m[0]:.3f}, {line.m[1]:.3f}) through ({line.b[0]:.3f}, {line.b[1]:.3f})"


def print_result(res):
    print(f"approximation, lines through pairs of critical values : {res.approx_crit_pts:.6f}")
    print(f"approximation, grid of lines                          : {res.approx_grid:.6f}")
    print(f"exact matching distance, pruning = {res.variant:<8s}           : {res.exact:.6f}")
    if res.best_line is not None:
        print(f"  attained on the line with {describe_line(res.best_line)}")
    print(f"  lines evaluated: {res.num_lines}    time: {res.exact_time:.2f} s exact, {res.approx_time:.2f} s approximations")


def print_comparison(results):
    print(f"{'pruning':10s} {'exact':>12s} {'lines evaluated':>16s} {'time (s)':>10s}")
    for res in results:
        print(f"{res.variant:10s} {res.exact:12.6f} {res.num_lines:16d} {res.exact_time:10.2f}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_module_args(parser)
    parser.add_argument("--pruning", choices=sorted(PRUNING) + ["compare"], default="all",
                        help="candidate switch points to discard (default: all)")
    parser.add_argument("--figure", action="store_true", help="save the modules and the optimal line as PNG")
    parser.add_argument("--plot-candidates", action="store_true",
                        help="save the candidate switch points computed by each algorithm")
    parser.add_argument("--out", default=os.path.join(settings.output_dir, "figures"), help="directory for figures")
    parser.add_argument("--verbose", action="store_true", help="show the pipeline's progress output")
    args = parser.parse_args()

    M, N, label, description = load_modules(args)
    settings.save_figure = False
    print(f"M: {len(M)} rectangle(s), N: {len(N)} rectangle(s)  ({description})")

    candidate_dir = None
    if args.figure or args.plot_candidates:
        os.makedirs(args.out, exist_ok=True)
    if args.plot_candidates:
        candidate_dir = os.path.join(args.out, label + "_candidates")
        os.makedirs(candidate_dir, exist_ok=True)

    variants = sorted(PRUNING, key=list(PRUNING).index) if args.pruning == "compare" else [args.pruning]
    results = [run_one(M, N, v, verbose=args.verbose, candidate_figure_dir=candidate_dir) for v in variants]

    if args.pruning == "compare":
        print_comparison(results)
    else:
        print_result(results[0])

    if args.figure:
        res = results[-1]
        settings.figure_title = f"{description}: M with {len(M)}, N with {len(N)} rectangle(s)"
        modules_path = os.path.join(args.out, label + ".png")
        chf.plot_rectangles(M, N, modules_path)
        result_path = os.path.join(args.out, label + "_result.png")
        chf.save_result_figure(M, N, res.best_line, res.approx_crit_pts, res.approx_grid, res.exact,
                               settings.figure_title, result_path)
        print(f"figures saved to {modules_path} and {result_path}")
    if candidate_dir:
        print(f"candidate switch point figures saved to {candidate_dir}")


if __name__ == "__main__":
    main()

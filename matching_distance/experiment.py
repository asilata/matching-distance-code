"""
Shared scaffolding for the command-line scripts.

Pruning variants, running one pair of modules through the pipeline, and building
modules from command-line arguments (random modules, the paper's small example, or
Examples 2.12-2.14 of Bapat et al., arXiv:2210.12868).
"""
import contextlib
import io
from dataclasses import dataclass

import matplotlib
matplotlib.use("Agg")

from . import settings
from . import distance as md
from . import examples as ex

# variant -> (section4_pruning, section5_pruning)
PRUNING = {
    "none": (False, False),     # keep every candidate switch point
    "section4": (True, False),  # CheckPts, CheckPts2, CheckOmega, CheckOmega2 (Section 4)
    "all": (True, True),        # Section 4 plus Corollary 5.2 with the approximation as lower bound
}

# Headers printed before each variant in verbose mode, as in the logs of the timing
# experiments of the paper (Figures 9-12).
LOG_HEADERS = {
    "none": "~~~NO PRUNING WHATSOEVER~~~",
    "section4": "~~~ONLY OLD PRUNING~~~",
    "all": "~~~ALL (including NEW) PRUNING~~~",
}

EXAMPLES = {
    "2.12": md.generate_rects_experiment_2_12,
    "2.13": md.generate_rects_experiment_2_13,
    "2.14": md.generate_rects_experiment_2_14,
}


def set_pruning(variant):
    settings.section4_pruning, settings.section5_pruning = PRUNING[variant]


@dataclass
class RunResult:
    variant: str
    exact: float
    approx_crit_pts: float   # max weighted bottleneck distance over lines through pairs of critical values
    approx_grid: float       # max over a grid of lines
    best_line: object        # modules.Line on which the exact distance is attained
    num_lines: int           # lines on which the weighted bottleneck distance was evaluated
    exact_time: float
    approx_time: float


def run_one(M, N, variant="all", verbose=False, candidate_figure_dir=None):
    """Approximations and exact matching distance of the modules M, N under one pruning variant.

    With verbose=False the pipeline's own progress output is suppressed.  With
    candidate_figure_dir set, the candidate switch points of each algorithm are drawn there.
    """
    set_pruning(variant)
    settings.print_output = verbose
    settings.compare_line_counts = verbose
    if verbose:
        print(LOG_HEADERS[variant])
        print("Rects in M: ", len(M))
        print("Rects in N: ", len(N))
        out = md.compute_distances(M, N, candidate_figure_dir)
    else:
        with contextlib.redirect_stdout(io.StringIO()):
            out = md.compute_distances(M, N, candidate_figure_dir)
    exact_time, approx_time, exact, crit, grid, best_line, num_lines = out
    return RunResult(variant, exact, crit, grid, best_line, num_lines, exact_time, approx_time)


def add_module_args(parser):
    group = parser.add_argument_group("modules (random: --M --N --seed; or --toy; or --example)")
    group.add_argument("--M", type=int, help="number of rectangles in the random module M")
    group.add_argument("--N", type=int, help="number of rectangles in the random module N")
    group.add_argument("--seed", type=int, help="seed of the random modules")
    group.add_argument("--toy", action="store_true", help="the small example of the paper (Figure 6)")
    group.add_argument("--example", choices=sorted(EXAMPLES), help="Examples 2.12-2.14 of Bapat et al., arXiv:2210.12868")


def load_modules(args):
    """Return (M, N, label, description) from the parsed module arguments."""
    if args.toy:
        M, N = ex.small_socg_ex_rects()
        return M, N, "toy", "the small example of the paper"
    if args.example:
        M, N, _ = EXAMPLES[args.example]()
        return M, N, "example_" + args.example.replace(".", "_"), f"Example {args.example} of Bapat et al., arXiv:2210.12868"
    if args.M is None or args.N is None or args.seed is None:
        raise SystemExit("give --M, --N and --seed, or --toy, or --example")
    M, N = md.generate_random_rectangles(args.M, args.N, seed=args.seed)
    return M, N, f"m{args.M}_n{args.N}_seed{args.seed}", f"random modules, seed {args.seed}"

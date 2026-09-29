"""Global switches read by the library and the scripts."""
import os
import shutil

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
output_dir = os.path.join(REPO_ROOT, "output")          # everything the scripts write; not tracked
figure_dir = os.path.join(REPO_ROOT, "paper_figures")   # figures reproduced for the paper; tracked
write_candidate_csvs = False   # also dump the candidate switch points of every run to output/candidates/

# Figures use LaTeX for text when a TeX installation is available; otherwise matplotlib's
# own mathtext renders the same labels.
use_tex = shutil.which("latex") is not None and shutil.which("dvipng") is not None

print_output = True            # print progress and results
save_figure = True             # scripts save figures
compare_line_counts = True and print_output
section5_pruning = True        # Section 5 pruning (Corollary 5.2), needs lower_bound_D
section4_pruning = True        # Section 4 pruning (CheckPts, CheckPts2, CheckOmega, CheckOmega2)
lower_bound_D = 100            # lower bound on the matching distance used by Section 5 pruning
figure_title = ""
debug = False

# For tests to run faster, set this to False. Note that this will NOT compute the
# bottleneck distance if False, which is the main point of the code.
actually_compute_matching_distance = True

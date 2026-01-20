global print_output, require_sys_version, save_figure, compare_line_counts, actually_compute_matching_distance

# Normally TRUE. can set to FALSE for cluster use.
TF = True
# here are the settings affected in cluster use
require_sys_version = True
print_output = True
save_figure = True
compare_line_counts = True and print_output
new_pruning_march_2025 = True
old_pruning = True
lower_bound_D = 100
figure_title = ""
debug = False
debug_M: list[list[tuple[float, float]]] = []
debug_N: list[list[tuple[float, float]]] = []
debug_seed = 0
overwrite_critvals = False
critvals_to_overwrite = []
nolub_to_overwrite = []

# for tests to run faster, set this to False. Note that this will NOT compute the bottleneck distance if false, which is the main point of the code.
actually_compute_matching_distance = True
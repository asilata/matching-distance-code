# Global switches read by the library and the scripts.

print_output = True            # print progress and results
save_figure = True             # scripts save figures
compare_line_counts = True and print_output
new_pruning_march_2025 = True  # Section 5 pruning (Corollary 5.2), needs lower_bound_D
old_pruning = True             # Section 4 pruning (CheckPts, CheckPts2, CheckOmega, CheckOmega2)
lower_bound_D = 100            # lower bound on the matching distance used by Section 5 pruning
figure_title = ""
debug = False

# For tests to run faster, set this to False. Note that this will NOT compute the
# bottleneck distance if False, which is the main point of the code.
actually_compute_matching_distance = True

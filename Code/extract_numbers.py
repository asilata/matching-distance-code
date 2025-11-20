import re
import pandas as pd

def extract_values(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    seed = int(file_path.split('_')[-1].split('.')[0])
    # Split the file into sections based on pruning labels
    sections = re.split(r'~~~(.*?)~~~', content)
    # Sections should be in the format: [text_before, title1, content1, title2, content2, ...]
    # So we'll extract pairs of (section title, section content)
    df = pd.DataFrame(columns = ['M', 'N', 'seed', 'match', 'crit_pt_lines_counted', 'time_crit_pts', 'exact_lines_counted', 'time_bneck', 'time_switch', 'time_match_dist', 'total_exact_time', 'prune'])
    for i in range(1, len(sections), 2):
        section_name = sections[i].strip()
        section_content = sections[i + 1]
        
        match = re.search(r'Rects in M:\s*([\d]+)', section_content)
        if match:
            M = int(match.group(1))
            
        match = re.search(r'Rects in N:\s*([\d]+)', section_content)
        if match:
            N = int(match.group(1))
        
        match = re.search(r'Maximum distance for lines through critical points:\s*([\d.]+)', section_content)
        if match:
            crit_point_dist = float(match.group(1))
            
        match = re.search(r'Maximum distance computed for grid of lines:\s*([\d.]+)', section_content)
        if match:
            grid_dist = float(match.group(1))
            
        match = re.search(r'Matching dist:\s*([\d.]+)', section_content)
        if match:
            exact_dist = float(match.group(1))
            
        if crit_point_dist == grid_dist == exact_dist:
            dist_match = 'yes'
        else:
            dist_match = f"crit_point_dist: {crit_point_dist}, grid_dist: {grid_dist}, exact_dist: {exact_dist}"
                
        match = re.search(r'Lines counted crit pts:\s*([\d]+)', section_content)
        if match:
            crit_pt_lines_counted = int(match.group(1))
        
        match = re.search(r'Time to get approx. from crit pts:\s*([\d.]+)', section_content)
        if match:
            time_crit_pts = float(match.group(1))
        
        match = re.search(r'Lines counted:\s*([\d]+)', section_content)
        if match:
             exact_lines_counted = int(match.group(1))
                
        match = re.search(r'Time to compute bottleneck dists:\s*([\d.]+)', section_content)
        if match:
            time_bneck = float(match.group(1))
            
        match = re.search(r'Time to compute switch pts:\s*([\d.]+)', section_content)
        if match:
            time_switch = float(match.group(1))
        
        match = re.search(r'Time to compute match dist:\s*([\d.]+)', section_content)
        if match:
            time_match_dist = float(match.group(1))
            
        match = re.search(r'Total time elapsed in exact computation:\s*([\d.]+)', section_content)
        if match:
            total_exact_time = float(match.group(1))
       
        row = pd.Series({'M': M, 'N': N, 'seed': seed, 'match': dist_match, 'crit_pt_lines_counted': crit_pt_lines_counted, 'time_crit_pts': time_crit_pts, 'exact_lines_counted': exact_lines_counted, 'time_bneck': time_bneck, 'time_switch': time_switch, 'time_match_dist': time_match_dist, 'total_exact_time': total_exact_time, 'prune': section_name})
        df = pd.concat([df, row.to_frame().T], ignore_index=True)
    return df


dfs = []

# Example: simulate adding small DataFrames in a loop
for file_path in ['six_experiments/5_1_3.txt', 'six_experiments/1_5_3.txt', 'six_experiments/2_4_3.txt', 'six_experiments/4_2_3.txt', 'six_experiments/3_3_3.txt', 'six_experiments/5_1_4.txt', 'six_experiments/1_5_4.txt', 'six_experiments/2_4_4.txt', 'six_experiments/4_2_4.txt', 'six_experiments/3_3_4.txt', 'six_experiments/5_1_5.txt', 'six_experiments/1_5_5.txt', 'six_experiments/2_4_5.txt', 'six_experiments/4_2_5.txt', 'six_experiments/3_3_5.txt', 'six_experiments/5_1_6.txt', 'six_experiments/1_5_6.txt', 'six_experiments/2_4_6.txt', 'six_experiments/4_2_6.txt', 'six_experiments/3_3_6.txt', 'six_experiments/5_1_7.txt', 'six_experiments/1_5_7.txt', 'six_experiments/2_4_7.txt', 'six_experiments/4_2_7.txt', 'six_experiments/3_3_7.txt']:
    temp_df = extract_values(file_path)
    dfs.append(temp_df)

# Concatenate all DataFrames at once
six_results = pd.concat(dfs, ignore_index=True)

six_results.to_csv('six_results_3_Nov.csv', index=False)
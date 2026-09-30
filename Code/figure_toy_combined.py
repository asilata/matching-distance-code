"""
Assemble Figure 6 of the paper from its panels.

Regenerates the panels with figure_toy_example.py (upper two rows: the modules and
Algorithms 3, 5 and 7 with Section 4 pruning) and figure_toy_pruning.py (bottom row: the
effect of Section 5 pruning), then places them in the layout of the paper:

    modules            Algorithm 3
    Algorithm 5        Algorithm 7
    Section 5 pruning (full width)

Run from anywhere:  python Code/figure_toy_combined.py
Output:             paper_figures/combination_rerun.png (tracked)
"""
import os
import subprocess
import sys

from PIL import Image

import settings

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(settings.figure_dir, "combination_rerun.png")
ROWS = [["MN.png", "MN3v1.png"], ["MN2v2p.png", "MN2v2unp.png"], ["MN_section5_pruning.png"]]
MARGIN = 80       # pixels around the figure
ROW_GAP = 90      # pixels between rows
DPI = 300         # the panels are saved at this resolution


def regenerate_panels():
    for script in ("figure_toy_example.py", "figure_toy_pruning.py"):
        subprocess.run([sys.executable, os.path.join(HERE, script)], check=True)


def assemble(rows, out_path):
    """Two panels per row are centred in the two halves of the page, a single one across it."""
    ims = [[Image.open(os.path.join(settings.figure_dir, name)).convert("RGBA") for name in row] for row in rows]
    cell = max(im.size[0] for row in ims for im in row if len(row) == 2)
    width = max(max(im.size[0] for row in ims if len(row) == 1 for im in row), 2 * cell) + 2 * MARGIN
    height = sum(max(im.size[1] for im in row) for row in ims) + ROW_GAP * (len(ims) - 1) + 2 * MARGIN
    sheet = Image.new("RGB", (width, height), "white")
    y = MARGIN
    for row in ims:
        row_height = max(im.size[1] for im in row)
        slot = (width - 2 * MARGIN) / len(row)
        for k, im in enumerate(row):
            x = MARGIN + slot * k + (slot - im.size[0]) / 2
            sheet.paste(im, (round(x), y + (row_height - im.size[1]) // 2), im)
        y += row_height + ROW_GAP
    sheet.save(out_path, dpi=(DPI, DPI))


if __name__ == "__main__":
    regenerate_panels()
    assemble(ROWS, OUT_PNG)
    print("Figure 6 written to", OUT_PNG)

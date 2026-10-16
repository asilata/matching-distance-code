"""Random pairs of single rectangles, with the distances of an earlier batch run."""
import csv
import os

import pytest

from matching_distance import distance as md
from matching_distance import experiment
from conftest import FIXTURES

ROWS = list(csv.DictReader(open(os.path.join(FIXTURES, "random_1v1_expected.csv"))))


@pytest.mark.parametrize("row", ROWS, ids=[f"seed{r['seed']}-{r['config_type']}" for r in ROWS])
def test_distances(row):
    M, N = md.generate_random_rectangles(1, 1, seed=int(row["seed"]))
    res = experiment.run_one(M, N, "all")
    assert res.exact == pytest.approx(float(row["exact"]), abs=1e-6)
    assert res.approx_crit_pts == pytest.approx(float(row["approx_crit_pts"]), abs=1e-6)
    assert res.approx_grid == pytest.approx(float(row["approx_grid"]), abs=1e-6)
    # both approximations are lower bounds on the matching distance
    assert res.exact >= max(res.approx_crit_pts, res.approx_grid) - 1e-9


def test_random_modules_depend_only_on_the_seed():
    assert md.generate_random_rectangles(2, 3, seed=5) == md.generate_random_rectangles(2, 3, seed=5)
    assert md.generate_random_rectangles(2, 3, seed=5) != md.generate_random_rectangles(2, 3, seed=6)

"""The small example of the paper (Figure 6): candidate counts, lower bound and distance."""
import json
import os
import random

import pytest

import examples as ex
import experiment
import omega_pts as omega
import settings
import toy_example_helpers as teh
from conftest import FIXTURES

EXPECTED = json.load(open(os.path.join(FIXTURES, "toy_example_counts.json")))


def counts(res):
    return {
        "alg3": {"raw": res["alg3"]["raw"], "distinct_points": len(res["alg3"]["points"])},
        "alg5": {"raw": res["alg5"]["raw"], "distinct_slopes": len(res["alg5"]["slopes"])},
        "alg7": {"raw": res["alg7"]["raw"], "distinct_points": len(res["alg7"]["points"]),
                 "distinct_slopes": len(res["alg7"]["slopes"])},
    }


@pytest.mark.parametrize("variant, prune, section5", [("none", False, False), ("section4", True, False),
                                                       ("section4_5", True, True)])
def test_candidate_counts(variant, prune, section5):
    critpts, _, _, _ = ex.small_socg_ex_M_N()
    settings.section5_pruning = section5
    settings.lower_bound_D = EXPECTED["lower_bound_D"]
    expected = {k: v for k, v in EXPECTED[variant].items() if k != "lines_evaluated"}
    assert counts(teh.run_algorithms(critpts, prune)) == expected


def test_lower_bound_and_distance():
    M, N = ex.small_socg_ex_rects()
    res = experiment.run_one(M, N, "all")
    assert max(res.approx_crit_pts, res.approx_grid) == pytest.approx(EXPECTED["lower_bound_D"])
    assert res.exact == pytest.approx(EXPECTED["exact_distance"])


@pytest.mark.parametrize("variant, key", [("section4", "section4"), ("all", "section4_5")])
def test_lines_evaluated(variant, key):
    M, N = ex.small_socg_ex_rects()
    res = experiment.run_one(M, N, variant)
    assert res.num_lines == EXPECTED[key]["lines_evaluated"]
    assert res.exact == pytest.approx(EXPECTED["exact_distance"])


def test_enumeration_size():
    """Section 6: C(n, 4) sets of four points and 3 C(n, 3) sets of three with one repetition."""
    from math import comb
    for n in (4, 7, 9):
        assert sum(1 for _ in omega.quadruples(list(range(n)), repetition=True)) == comb(n, 4) + 3 * comb(n, 3)
        assert sum(1 for _ in omega.quadruples(list(range(n)), repetition=False)) == comb(n, 4)


def test_candidates_do_not_depend_on_the_order_of_the_critical_values():
    critpts, _, _, _ = ex.small_socg_ex_M_N()
    settings.section5_pruning = False
    reference = teh.run_algorithms(critpts, True)
    rng = random.Random(0)
    for _ in range(3):
        shuffled = critpts[:]
        rng.shuffle(shuffled)
        assert teh.run_algorithms(shuffled, True) == reference

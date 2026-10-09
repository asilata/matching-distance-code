"""Figures 7 and 8: the candidate-count logs, the script that writes them and the worst-case bound."""
import os
from math import comb

import pytest

import count_candidates as cc
import figure_candidate_counts as fcc

LOGS = ["rand_rects_stats", "bunnyruns_random_rects", "bunnyruns_poisson"]
ALGORITHMS = ("3v1", "2v2paired", "2v2unpaired")


def archived(name):
    return fcc.parse_log(os.path.join(fcc.DATA_DIR, name + ".txt"))


def test_worst_case_bound():
    """The sum of Section 6 against its closed form, (13/4) n(n-1)(n-2)(n + 17/13)."""
    assert fcc.worst_case_bound(4) == 78 + 3 * 4 * 28 == 414
    for n in range(3, 60):
        assert fcc.worst_case_bound(n) == 78 * comb(n, 4) + 84 * comb(n, 3)
        assert fcc.worst_case_bound(n) == pytest.approx(13 / 4 * n * (n - 1) * (n - 2) * (n + 17 / 13))


@pytest.mark.parametrize("name", LOGS)
def test_full_and_shortened_logs_agree(name):
    full = fcc.parse_log(os.path.join(fcc.DATA_DIR, name + ".txt"))
    short = fcc.parse_log(os.path.join(fcc.DATA_DIR, name + "_shortened.txt"))
    drop = ("M", "N")  # the shortened bunnyruns logs do not repeat the module sizes
    assert [{k: v for k, v in r.items() if k not in drop} for r in full] == \
           [{k: v for k, v in r.items() if k not in drop} for r in short]


def test_archived_figure_7_runs():
    runs = archived("rand_rects_stats")
    assert sorted((r["M"], r["N"], r["seed"]) for r in runs) == \
           [(m, n, s) for m, n in [(1, 1), (1, 2), (2, 2), (3, 2), (3, 3)] for s in range(1, 6)]
    assert runs[0]["3v1"] == (79, 32) and runs[0]["critvals"] == 6


def test_archived_figure_8_runs():
    poisson, rects = archived("bunnyruns_poisson"), archived("bunnyruns_random_rects")
    assert [r["critvals"] for r in poisson] == [4, 9, 16, 23, 34]
    assert [r["critvals"] for r in rects] == list(range(6, 34, 3))
    assert poisson[-1]["3v1"] == (379412, 288967)
    assert rects[-1]["2v2unpaired"] == (56322, 38635)


def test_figure_7_runs():
    runs = fcc.parse_log(fcc.FIG7_LOG)
    assert [(r["M"], r["N"], r["seed"]) for r in runs] == \
           [(m, n, s) for m, n in cc.FIG7_CONFIGS for s in cc.FIG7_SEEDS]
    assert runs[0]["3v1"] == (137, 35) and runs[0]["critvals"] == 6


def test_figure_8_runs():
    poisson = fcc.parse_log(fcc.FIG8_PANELS[0][1])
    rects = fcc.parse_log(fcc.FIG8_PANELS[1][1])
    assert [r["critvals"] for r in poisson] == [4, 9, 16, 23, 34]
    assert [(r["M"], r["N"], r["seed"]) for r in rects] == [(t // 2, t - t // 2, 11) for t in range(2, 12)]
    assert [r["critvals"] for r in rects] == list(range(6, 34, 3))
    assert poisson[-1]["3v1"] == (417060, 303026)
    assert rects[-1]["2v2unpaired"] == (96106, 57328)


def test_count_candidates_reproduces_the_logs():
    """The smallest logged runs of Figure 8, recomputed: random rectangles with seed 11, and
    the Poisson points for 9 critical values."""
    rects = fcc.parse_log(fcc.FIG8_PANELS[1][1])[0]
    critvals, D = cc.rectangle_input(1, 1, cc.FIG8_SEED)
    assert len(critvals) == rects["critvals"]
    assert cc.candidate_counts(critvals, D) == {k: rects[k] for k in ALGORITHMS}
    poisson = fcc.parse_log(fcc.FIG8_PANELS[0][1])[1]
    critvals = cc.poisson_critical_values(2.5, seed=1)
    assert len(critvals) == poisson["critvals"] == 9
    assert cc.candidate_counts(critvals, None) == {k: poisson[k] for k in ALGORITHMS}

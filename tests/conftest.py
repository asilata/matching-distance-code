import os
import sys

import matplotlib
import pytest

matplotlib.use("Agg")

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "Code"))
FIXTURES = os.path.join(REPO, "tests", "fixtures")

import settings  # noqa: E402

_DEFAULTS = {k: v for k, v in vars(settings).items() if isinstance(v, (bool, int, float, str))}


@pytest.fixture(autouse=True)
def quiet_settings():
    """Quiet output and no figures during a test; restore every switch afterwards."""
    settings.print_output = False
    settings.compare_line_counts = False
    settings.save_figure = False
    yield
    for k, v in _DEFAULTS.items():
        setattr(settings, k, v)

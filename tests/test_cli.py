"""The command-line entry point, run as a user would from an arbitrary directory."""
import os
import subprocess
import sys

from conftest import REPO


def test_run_example_from_another_directory(tmp_path):
    out = subprocess.run([sys.executable, os.path.join(REPO, "run_example.py"), "--M", "1", "--N", "1",
                          "--seed", "0"], cwd=tmp_path, capture_output=True, text=True, timeout=300)
    assert out.returncode == 0, out.stderr
    assert "exact matching distance, pruning = all" in out.stdout
    assert "3.206211" in out.stdout
    assert list(tmp_path.iterdir()) == []  # nothing is written into the working directory

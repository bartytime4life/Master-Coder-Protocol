import os
import subprocess
import sys


def run(args):
    return subprocess.run([sys.executable, "-m", "polymerlab.cli.app"] + args, capture_output=True, text=True)


def test_cli_version():
    res = run(["version"])
    assert res.returncode == 0


def test_cli_data_flow(tmp_path):
    res = run(["data-validate", "--in", "data/raw/example_polymer.json"])
    assert res.returncode == 0
    res = run(["data-featurize", "--in", "data/raw", "--out", "data/processed"])
    assert res.returncode == 0
    assert os.path.exists("data/processed/features.csv")

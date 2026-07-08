"""End-to-end tests (require the database + plotting stack). Auto-skipped if DB is down."""
import socket

import pytest

from locuscompare import example_path, locuscompare
from locuscompare.config import get_db_config


def _db_reachable():
    cfg = get_db_config()
    try:
        with socket.create_connection((cfg["host"], cfg["port"]), timeout=5):
            return True
    except OSError:
        return False


pytestmark = pytest.mark.skipif(not _db_reachable(), reason="reference DB not reachable")


def test_combine_false_returns_three_panels():
    res = locuscompare(example_path("gwas.tsv"), example_path("eqtl.tsv"), combine=False)
    assert set(res.keys()) == {"locuscompare", "locuszoom1", "locuszoom2"}


def test_combined_figure_is_produced():
    fig = locuscompare(example_path("gwas.tsv"), example_path("eqtl.tsv"))
    # a real plotnine composition, not the combine=False dict of panels
    assert not isinstance(fig, dict)
    assert hasattr(fig, "save")


def test_custom_ld_non_default_path():
    import numpy as np
    import pandas as pd

    import locuscompare as lc

    g, e = example_path("gwas.tsv"), example_path("eqtl.tsv")
    # Build custom LD relative to a known lead SNP, bypassing retrieve_LD.
    d1 = lc.read_metal(g)
    d2 = lc.read_metal(e)
    merged = d1.merge(d2, on="rsid", suffixes=("1", "2"))
    snp = "rs9349379"
    my_ld = pd.DataFrame(
        {
            "SNP_A": snp,
            "SNP_B": merged["rsid"].to_numpy(),
            "R2": np.resize([0.9, 0.5, 0.1], len(merged)),
        }
    )
    res = locuscompare(g, e, snp=snp, ld=my_ld, combine=False)
    assert set(res.keys()) == {"locuscompare", "locuszoom1", "locuszoom2"}

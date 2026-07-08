"""Reference-database tests. Skipped automatically when the DB is unreachable."""
import socket

import pandas as pd
import pytest

from locuscompare import get_position, retrieve_LD
from locuscompare.config import get_db_config


def _db_reachable():
    cfg = get_db_config()
    try:
        with socket.create_connection((cfg["host"], cfg["port"]), timeout=5):
            return True
    except OSError:
        return False


pytestmark = pytest.mark.skipif(not _db_reachable(), reason="reference DB not reachable")


def test_get_position():
    d = pd.DataFrame({"rsid": ["rs9349379", "rs1333049"]})
    res = get_position(d, "hg19")
    assert {"chr", "pos"}.issubset(res.columns)
    assert (res["rsid"] == "rs9349379").any()


def test_retrieve_LD():
    ld = retrieve_LD("6", "rs9349379", "EUR")
    assert {"SNP_A", "SNP_B", "R2"}.issubset(ld.columns)
    assert len(ld) > 0

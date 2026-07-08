"""Offline validation tests for locuscompare() (no database needed)."""
import pandas as pd
import pytest

from locuscompare import locuscompare


def test_ld_without_snp_errors():
    ld = pd.DataFrame({"SNP_A": ["rs1"], "SNP_B": ["rs2"], "R2": [0.5]})
    with pytest.raises(ValueError, match="lead 'snp'"):
        locuscompare("a.tsv", "b.tsv", ld=ld)


def test_malformed_ld_errors():
    bad = pd.DataFrame({"A": ["rs1"], "B": ["rs2"], "r2": [0.5]})
    with pytest.raises(ValueError, match="SNP_A, SNP_B, R2"):
        locuscompare("a.tsv", "b.tsv", snp="rs1", ld=bad)

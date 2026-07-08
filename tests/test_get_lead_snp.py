import numpy as np
import pandas as pd
import pytest

from locuscompare import get_lead_snp


def test_min_pval_backward_compatible():
    m = pd.DataFrame(
        {
            "rsid": ["a", "b", "c"],
            "pval1": [0.1, 0.001, 0.5],
            "pval2": [0.2, 0.01, 0.5],
            "logp1": [1, 3, 0.3],
            "logp2": [0.7, 2, 0.3],
        }
    )
    assert get_lead_snp(m) == "b"


def test_fallback_when_pval_zero():
    m = pd.DataFrame(
        {
            "rsid": ["a", "b"],
            "pval1": [0.0, 0.3],
            "pval2": [0.99, 0.3],
            "logp1": [307.6, 0.523],
            "logp2": [0.0044, 0.523],
        }
    )
    # min(pval): b (0.6) < a (0.99); max(logp): a (307.6) > b (1.05) -> fallback picks 'a'
    assert get_lead_snp(m) == "a"


def test_fallback_when_pval_nan():
    m = pd.DataFrame(
        {
            "rsid": ["a", "b"],
            "pval1": [np.nan, np.nan],
            "pval2": [np.nan, np.nan],
            "logp1": [10, 2],
            "logp2": [1, 8],
        }
    )
    assert get_lead_snp(m) == "a"  # a = 11 > b = 10


def test_explicit_snp_validated():
    m = pd.DataFrame(
        {"rsid": ["a", "b"], "pval1": [0.1, 0.2], "pval2": [0.1, 0.2], "logp1": [1, 0.7], "logp2": [1, 0.7]}
    )
    assert get_lead_snp(m, "b") == "b"
    with pytest.raises(ValueError, match="not found"):
        get_lead_snp(m, "zzz")

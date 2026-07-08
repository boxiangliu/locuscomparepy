import numpy as np
import pandas as pd
import pytest

from locuscompare import read_metal


def test_pval_zero_floored_with_warning():
    d = pd.DataFrame({"rsid": ["rs1", "rs2"], "pval": [1e-10, 0.0]})
    with pytest.warns(UserWarning, match="underflow"):
        res = read_metal(d)
    assert np.isfinite(res["logp"]).all()
    assert res["logp"].iloc[1] == pytest.approx(-np.log10(np.finfo(float).tiny))


def test_normal_pvalues_unchanged():
    d = pd.DataFrame({"rsid": ["rs1", "rs2"], "pval": [0.5, 1e-8]})
    res = read_metal(d)
    assert res["logp"].to_numpy() == pytest.approx(-np.log10([0.5, 1e-8]))


def test_logp_col_used_and_pval_nan():
    d = pd.DataFrame({"rsid": ["rs1", "rs2"], "neglogp": [5.0, 320.0]})
    res = read_metal(d, logp_col="neglogp")
    assert res["logp"].tolist() == [5.0, 320.0]
    assert res["pval"].isna().all()


def test_zscore_matches_two_sided_p():
    res = read_metal(pd.DataFrame({"rsid": ["rs1"], "z": [1.959964]}), zscore_col="z")
    assert res["logp"].iloc[0] == pytest.approx(-np.log10(0.05), abs=1e-4)
    assert res["pval"].isna().all()


def test_zscore_sign_agnostic():
    res = read_metal(pd.DataFrame({"rsid": ["a", "b"], "z": [5.0, -5.0]}), zscore_col="z")
    assert res["logp"].iloc[0] == pytest.approx(res["logp"].iloc[1])


def test_large_z_no_inf():
    res = read_metal(pd.DataFrame({"rsid": ["a"], "z": [50.0]}), zscore_col="z")
    assert np.isfinite(res["logp"].iloc[0]) and res["logp"].iloc[0] > 500


def test_zscore_and_logp_mutually_exclusive():
    with pytest.raises(ValueError, match="only one"):
        read_metal(
            pd.DataFrame({"rsid": ["a"], "z": [1.0], "lp": [1.0]}),
            zscore_col="z",
            logp_col="lp",
        )


def test_missing_column_errors():
    with pytest.raises(ValueError, match="not found"):
        read_metal(pd.DataFrame({"rsid": ["a"], "pval": [0.1]}), logp_col="nope")

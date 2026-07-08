"""Read association summary statistics (port of R ``read_metal``)."""
import os
import warnings

import numpy as np
import pandas as pd
from scipy.stats import norm


def read_metal(in_fn, marker_col="rsid", pval_col="pval", zscore_col=None, logp_col=None):
    """Read association summary statistics into a ``(rsid, pval, logp)`` DataFrame.

    Exactly one input mode is used:

    * **p-value** (default) -- ``logp = -log10(pval)``. p-values that underflow to
      ``0`` are floored at ``-log10(tiny)`` (~307.6) with a warning.
    * **z-score** (``zscore_col``) -- a numerically stable two-sided ``-log10(p)``
      that never underflows for large ``|z|``. ``pval`` is set to ``NaN``.
    * **logp** (``logp_col``) -- a pre-computed ``-log10(p)`` used directly.
      ``pval`` is set to ``NaN``.

    Parameters
    ----------
    in_fn : str or pandas.DataFrame
        Path to a tab-delimited file, or a DataFrame.
    """
    if isinstance(in_fn, pd.DataFrame):
        d = in_fn.copy()
    elif isinstance(in_fn, (str, os.PathLike)):
        d = pd.read_csv(in_fn, sep="\t")
    else:
        raise TypeError('"in_fn" must be a path or a pandas DataFrame.')

    if marker_col in d.columns:
        d = d.rename(columns={marker_col: "rsid"})
    if "rsid" not in d.columns:
        raise ValueError(f'marker column "{marker_col}" not found.')

    if zscore_col is not None and logp_col is not None:
        raise ValueError("Supply only one of zscore_col or logp_col.")

    if zscore_col is not None:
        if zscore_col not in d.columns:
            raise ValueError(f'Column "{zscore_col}" (zscore_col) not found.')
        z = d[zscore_col].to_numpy(dtype=float)
        # stable two-sided -log10(p): -(log(2 * Phi(-|z|)))/log(10)
        logp = -(norm.logsf(np.abs(z)) + np.log(2.0)) / np.log(10.0)
        pval = np.full(len(d), np.nan)
    elif logp_col is not None:
        if logp_col not in d.columns:
            raise ValueError(f'Column "{logp_col}" (logp_col) not found.')
        logp = d[logp_col].to_numpy(dtype=float)
        if np.any(~np.isfinite(logp) | (logp < 0)):
            raise ValueError("logp values must be finite and non-negative.")
        pval = np.full(len(d), np.nan)
    else:
        if pval_col not in d.columns:
            raise ValueError(f'Column "{pval_col}" (pval_col) not found.')
        pval = d[pval_col].to_numpy(dtype=float)
        if np.any((pval < 0) | (pval > 1)):
            raise ValueError("p-values must be between 0 and 1.")
        with np.errstate(divide="ignore"):
            logp = -np.log10(pval)
        n_floored = int(np.isinf(logp).sum())
        if n_floored:
            floor = -np.log10(np.finfo(float).tiny)
            logp = np.where(np.isinf(logp), floor, logp)
            warnings.warn(
                f"{n_floored} p-value(s) were 0 (underflow); flooring -log10(p) at {floor:.1f}.",
                stacklevel=2,
            )

    return pd.DataFrame(
        {"rsid": d["rsid"].astype(str).to_numpy(), "pval": pval, "logp": logp}
    )

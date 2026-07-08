"""End-to-end orchestrator (port of R ``locuscompare``)."""
import warnings

import pandas as pd

from .analysis import get_lead_snp
from .db import get_position, retrieve_LD
from .io import read_metal
from .plot import make_combined_plot


def locuscompare(
    in_fn1,
    in_fn2,
    marker_col1="rsid",
    pval_col1="pval",
    title1="eQTL",
    marker_col2="rsid",
    pval_col2="pval",
    title2="GWAS",
    snp=None,
    population="EUR",
    combine=True,
    genome="hg19",
    ld=None,
):
    """Make a LocusCompare figure from two association summary-statistics inputs.

    Parameters mirror the R package. Supply ``ld`` (a DataFrame with columns
    ``SNP_A``, ``SNP_B``, ``R2`` where ``SNP_A`` is the lead ``snp``) to bypass the
    reference database; ``snp`` is then required and ``population`` is ignored.
    """
    if ld is not None:
        if snp is None:
            raise ValueError(
                "When supplying 'ld', you must also specify the lead 'snp' the LD is relative to."
            )
        if not isinstance(ld, pd.DataFrame) or not {"SNP_A", "SNP_B", "R2"}.issubset(ld.columns):
            raise ValueError("'ld' must be a DataFrame with columns SNP_A, SNP_B, R2.")
        if snp not in set(ld["SNP_A"]):
            warnings.warn(
                f"None of the supplied LD rows have SNP_A == '{snp}'; "
                "all SNPs will be colored as low-LD.",
                stacklevel=2,
            )

    d1 = read_metal(in_fn1, marker_col1, pval_col1)
    d2 = read_metal(in_fn2, marker_col2, pval_col2)
    merged = d1.merge(d2, on="rsid", suffixes=("1", "2"))

    if genome not in ("hg19", "hg38"):
        raise ValueError("genome must be 'hg19' or 'hg38'.")
    merged = get_position(merged, genome)

    chrs = list(pd.unique(merged["chr"]))
    if len(chrs) != 1:
        raise ValueError("There must be one and only one chromosome.")
    chr = chrs[0]

    snp = get_lead_snp(merged, snp)
    if ld is None:
        ld = retrieve_LD(chr, snp, population)

    return make_combined_plot(merged, title1, title2, ld, chr, snp, combine)

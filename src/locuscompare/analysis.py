"""Lead-SNP selection and LD colouring (port of R ``get_lead_snp`` and ``assign_color``)."""
import pandas as pd

_LD_BINS = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
_LD_LABELS = ["blue4", "skyblue", "darkgreen", "orange", "red"]


def get_lead_snp(merged, snp=None):
    """Return the lead SNP rsID.

    When ``snp`` is ``None``, the lead is ``argmin(pval1 + pval2)`` if p-values are
    usable (no ``NaN`` and all > 0), otherwise ``argmax(logp1 + logp2)`` -- the
    fallback for z-score / logp input or underflowed p-values.
    """
    if snp is None:
        p1, p2 = merged["pval1"], merged["pval2"]
        use_pval = (
            not p1.isna().any()
            and not p2.isna().any()
            and (p1 > 0).all()
            and (p2 > 0).all()
        )
        if use_pval:
            idx = (p1 + p2).idxmin()
        else:
            idx = (merged["logp1"] + merged["logp2"]).idxmax()
        snp = merged.loc[idx, "rsid"]
    else:
        if snp not in set(merged["rsid"]):
            raise ValueError(f"{snp} not found in the intersection of in_fn1 and in_fn2.")
    return str(snp)


def assign_color(rsid, snp, ld):
    """Map each rsID to a colour by its r2 with ``snp``.

    Returns a ``dict`` {rsid: colour}. The lead SNP is ``'purple'``; SNPs with no
    LD record default to ``'blue4'``. Colours are binned as in the R package:
    (0,0.2]->blue4, (0.2,0.4]->skyblue, (0.4,0.6]->darkgreen, (0.6,0.8]->orange,
    (0.8,1]->red.
    """
    ld_lead = ld[ld["SNP_A"] == snp]
    binned = pd.cut(ld_lead["R2"], bins=_LD_BINS, labels=_LD_LABELS, include_lowest=True)
    b2c = dict(zip(ld_lead["SNP_B"].astype(str), binned.astype(object)))
    colors = {str(r): b2c.get(str(r), "blue4") for r in rsid}
    colors[str(snp)] = "purple"
    return colors

"""Plotting with plotnine (port of the R ggplot2/cowplot figures)."""
import pandas as pd
from plotnine import (
    aes,
    geom_point,
    geom_text,
    ggplot,
    labs,
    scale_color_manual,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_classic,
)

# r2 bin -> colour, matching the R package's R colour names as hex.
_COLOR_HEX = {
    "[0,0.2]": "#00008B",    # blue4
    "(0.2,0.4]": "#87CEEB",  # skyblue
    "(0.4,0.6]": "#006400",  # darkgreen
    "(0.6,0.8]": "#FFA500",  # orange
    "(0.8,1]": "#FF0000",    # red
    "lead SNP": "#A020F0",   # purple
}
_LD_ORDER = ["[0,0.2]", "(0.2,0.4]", "(0.4,0.6]", "(0.6,0.8]", "(0.8,1]", "lead SNP"]
_PURPLE = _COLOR_HEX["lead SNP"]


def _r2_group(r2):
    if pd.isna(r2) or r2 <= 0.2:
        return "[0,0.2]"
    if r2 <= 0.4:
        return "(0.2,0.4]"
    if r2 <= 0.6:
        return "(0.4,0.6]"
    if r2 <= 0.8:
        return "(0.6,0.8]"
    return "(0.8,1]"


def _prepare(merged, ld, snp):
    lead = ld[ld["SNP_A"] == snp][["SNP_B", "R2"]].rename(columns={"SNP_B": "rsid"})
    df = merged.merge(lead, on="rsid", how="left")
    df["r2_group"] = [
        "lead SNP" if r == snp else _r2_group(v) for r, v in zip(df["rsid"], df["R2"])
    ]
    df["r2_group"] = pd.Categorical(df["r2_group"], categories=_LD_ORDER, ordered=True)
    df["is_lead"] = df["rsid"] == snp
    return df


def make_scatterplot(df, title1, title2):
    """LocusCompare scatter: -log10(P) study 1 vs study 2, coloured by r2."""
    lead = df[df["is_lead"]]
    return (
        ggplot(df, aes("logp1", "logp2"))
        + geom_point(aes(color="r2_group"), size=2.0, alpha=0.8)
        + geom_point(lead, aes("logp1", "logp2"), color=_PURPLE, shape="D", size=4.0)
        + geom_text(lead, aes("logp1", "logp2", label="rsid"), va="bottom", ha="right", size=9)
        + scale_color_manual(values=_COLOR_HEX, name="r2", drop=False)
        + scale_x_continuous(expand=(0.06, 0, 0.10, 0))
        + scale_y_continuous(expand=(0.05, 0, 0.13, 0))
        + labs(x=f"{title1} -log10(P)", y=f"{title2} -log10(P)")
        + theme_classic()
    )


def make_locuszoom(df, title, chr, ycol):
    """A LocusZoom panel: -log10(P) vs genomic position (Mb), coloured by r2."""
    lead = df[df["is_lead"]]
    return (
        ggplot(df, aes("pos", ycol))
        + geom_point(aes(color="r2_group"), size=2.0, alpha=0.8)
        + geom_point(lead, aes("pos", ycol), color=_PURPLE, shape="D", size=4.0)
        + geom_text(lead, aes("pos", ycol, label="rsid"), va="bottom", ha="center", size=9)
        + scale_color_manual(values=_COLOR_HEX, drop=False)
        + scale_x_continuous(labels=lambda xs: [f"{x / 1e6:.1f}" for x in xs], expand=(0.05, 0, 0.05, 0))
        + scale_y_continuous(expand=(0.05, 0, 0.13, 0))
        + labs(x=f"chr{chr} (Mb)", y=f"{title} -log10(P)")
        + theme_classic()
        + theme(legend_position="none")
    )


def make_combined_plot(merged, title1, title2, ld, chr, snp=None, combine=True):
    """Assemble the LocusCompare scatter with two stacked LocusZoom panels.

    When ``combine`` is True, returns a plotnine composition
    (scatter | (locuszoom1 / locuszoom2)); call ``.save(path, ...)`` to write it.
    When ``combine`` is False, returns a ``dict`` of the three plotnine plots.
    """
    from .analysis import get_lead_snp

    snp = get_lead_snp(merged, snp)
    df = _prepare(merged, ld, snp)
    p1 = make_scatterplot(df, title1, title2)
    p2 = make_locuszoom(df, title1, chr, "logp1")
    p3 = make_locuszoom(df, title2, chr, "logp2")
    if not combine:
        return {"locuscompare": p1, "locuszoom1": p2, "locuszoom2": p3}
    return p1 | (p2 / p3)  # plotnine native composition

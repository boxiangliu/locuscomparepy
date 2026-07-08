# locuscomparepy

Python port of the R package [**locuscomparer**](https://github.com/boxiangliu/locuscomparer) for visualizing GWAS–QTL colocalization events. Given two association summary-statistics datasets (e.g. GWAS and eQTL), it produces a combined figure: a LocusCompare scatter (−log10 P vs −log10 P) flanked by two LocusZoom panels, with SNPs colored by LD r² to the lead SNP.

> Shares the same reference database as the R package, and is kept at feature parity with it.

## Installation

```bash
pip install git+https://github.com/boxiangliu/locuscomparepy
# (PyPI: `pip install locuscomparepy` once published)
```

## Quickstart

```python
import locuscompare as lc

gwas = lc.example_path("gwas.tsv")
eqtl = lc.example_path("eqtl.tsv")

fig = lc.locuscompare(gwas, eqtl, title1="CAD GWAS", title2="Coronary Artery eQTL")
fig.save("locuscompare.png", width=10, height=5, dpi=150)   # combined figure
```

Input files are tab-delimited with `rsid` and `pval` columns. You can also pass
**z-scores** (`zscore_col=`) or a pre-computed **−log10(p)** (`logp_col=`), and
**bring your own LD** via `ld=` (a `SNP_A`/`SNP_B`/`R2` table) to bypass the
reference database:

```python
# z-scores instead of p-values
lc.read_metal("gwas.tsv", zscore_col="z")

# custom LD (e.g. from a multi-ancestry panel)
lc.locuscompare(gwas, eqtl, snp="rs9349379", ld=my_ld)   # my_ld: SNP_A/SNP_B/R2
```

To edit individual panels, pass `combine=False` to get a dict of three
[plotnine](https://plotnine.org) plots (`locuscompare`, `locuszoom1`, `locuszoom2`).

## API

| Function | Purpose |
|----------|---------|
| `read_metal(in_fn, marker_col, pval_col, zscore_col, logp_col)` | Load summary stats → `(rsid, pval, logp)` |
| `get_position(x, genome)` | Append `chr`/`pos` from the reference DB |
| `retrieve_LD(chr, snp, population)` | Pairwise LD r² for a lead SNP |
| `get_lead_snp(merged, snp)` | Pick the lead SNP |
| `assign_color(rsid, snp, ld)` | Map rsIDs → colors by r² |
| `make_scatterplot` / `make_locuszoom` / `make_combined_plot` | Build figures |
| `locuscompare(in_fn1, in_fn2, ...)` | End-to-end |

## Notes

- Plotting uses **plotnine** (a ggplot2 grammar port), so the figures mirror the R package closely.
- `get_position`, `retrieve_LD`, and full `locuscompare` calls query a shared MySQL
  database over the network (non-standard port; some institutional firewalls may block it).
  Override the connection with `LOCUSCOMPARE_DB_*` environment variables.

## License

GPL-3.0-or-later. Port of `locuscomparer` by Boxiang Liu et al. If you use this,
please cite the [LocusCompare paper](https://www.nature.com/articles/s41588-019-0404-0):
Liu, Gloudemans, Rao, Ingelsson & Montgomery (2019), *Nature Genetics*.

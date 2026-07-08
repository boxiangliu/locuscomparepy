# LocusComparePy <img src="docs/logo.png" align="right" height="139" alt="locuscompare hex logo" />

> 📦 **R users:** the original R package is [**locuscomparer**](https://github.com/boxiangliu/locuscomparer).

## News

- **v0.1.0** (2026-07-08) — Initial Python port of `locuscomparer`, at feature parity with the R package v1.1.0: p-value / z-score (`zscore_col`) / `logp_col` input, custom LD via `ld=`, and the combined LocusCompare + LocusZoom figure via [plotnine](https://plotnine.org).

See [NEWS.md](NEWS.md) for the full changelog.

## 1. Installation

LocusComparePy is a Python package for visualization of GWAS-eQTL colocalization events.

Install from PyPI (use the second line for the development version):

```bash
pip install locuscomparepy
# pip install git+https://github.com/boxiangliu/locuscomparepy
```

## 2. Example

To illustrate the use of locuscomparepy, we use the GWAS dataset from Nikpay et al. (2015) and the coronary artery eQTL dataset from GTEx v7 at the *PHACTR1* locus:

```python
import locuscompare as lc

gwas_fn = lc.example_path("gwas.tsv")
eqtl_fn = lc.example_path("eqtl.tsv")
fig = lc.locuscompare(in_fn1=gwas_fn, in_fn2=eqtl_fn,
                      title1="CAD GWAS", title2="Coronary Artery eQTL")
fig.save("locuscompare.png", width=10, height=5, dpi=150)
```

The output from `locuscompare` is a figure like the following:

![](https://raw.githubusercontent.com/boxiangliu/locuscomparepy/main/docs/locuscompare.png)

The labeled SNP is the lead SNP (in this case for both studies), and other SNPs are colored according to their LD r² with the lead SNP.

## 3. Using your own dataset

The input to `locuscompare()` is a tab-delimited text file with two columns:

1. rsid
2. pval

Here is an example file:

```
rsid	pval
rs62156064	0.564395
rs7562234	0.399642
rs11677377	0.34308
rs35076156	0.625237
```

You can download the example files here: [GWAS](https://raw.githubusercontent.com/boxiangliu/locuscomparepy/main/src/locuscompare/data/gwas.tsv) and [eQTL](https://raw.githubusercontent.com/boxiangliu/locuscomparepy/main/src/locuscompare/data/eqtl.tsv) datasets.

Then run the following commands:

```python
import locuscompare as lc

gwas_fn = "path/to/gwas.tsv"
eqtl_fn = "path/to/eqtl.tsv"
fig = lc.locuscompare(in_fn1=gwas_fn, in_fn2=eqtl_fn, title1="GWAS", title2="eQTL")
```

You can also supply **z-scores** (`zscore_col=`) or pre-computed **−log10(p)** (`logp_col=`) instead of p-values, and **bring your own LD** via `ld=` (a `SNP_A`/`SNP_B`/`R2` table) to bypass the reference database.

## 4. Documentation

To view documentation for each function, use `help(function)` (or `function?` in IPython/Jupyter). LocusComparePy exports the following functions:

**Data munging**

- `assign_color`: Assign color to each SNP according to LD.
- `get_lead_snp`: Get the lead SNP from the intersection of two studies.
- `get_position`: Append two columns, chromosome (chr) and position (pos), to the input.

**Plotting**

- `locuscompare`: Make a locuscompare plot.
- `make_combined_plot`: Combine two locuszoom plots with a locuscompare plot.
- `make_locuszoom`: Make a locuszoom plot.
- `make_scatterplot`: Make a scatter plot (the LocusCompare plot).

**Data loading**

- `read_metal`: Read association summary statistics from file.
- `retrieve_LD`: Retrieve SNP pairwise LD from the database.
- `example_path`: Path to a bundled example dataset (`gwas.tsv`, `eqtl.tsv`).

Position/LD lookups query a shared MySQL database over the network (non-standard port; some institutional firewalls may block it). Override the connection with `LOCUSCOMPARE_DB_*` environment variables.

## 5. Citation

If you use locuscompare, please cite the following paper: https://www.nature.com/articles/s41588-019-0404-0

Boxiang Liu, Michael J. Gloudemans, Abhiram S. Rao, Erik Ingelsson & Stephen B. Montgomery (2019) Abundant associations with gene expression complicate GWAS follow-up, *Nature Genetics*

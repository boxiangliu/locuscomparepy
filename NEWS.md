# Version 0.1.2 (2026-07-08):

- The r2 legend is now a compact stepped colorbar drawn inside the scatter panel
  (five colour blocks with 0.2/0.4/0.6/0.8 ticks), matching the R package's inset
  legend.

# Version 0.1.1 (2026-07-08):

- Match the R package's figure proportions: the LocusCompare scatter is now a
  square panel with the r2 legend placed inside it, and the two LocusZoom panels
  are wide-and-short (2:1) so that, stacked, they span the same height and align
  with the scatter.

# Version 0.1.0 (2026-07-08):

Initial Python port of the R package
[locuscomparer](https://github.com/boxiangliu/locuscomparer), at feature parity
with locuscomparer v1.1.0:

- `read_metal`: p-value, z-score (`zscore_col`) and pre-computed -log10(p)
  (`logp_col`) input; p-values that underflow to 0 are floored with a warning.
- `get_position`, `retrieve_LD`: queries against the same reference database.
- `get_lead_snp`, `assign_color`: lead-SNP selection and LD-based coloring.
- `make_scatterplot`, `make_locuszoom`, `make_combined_plot`, `locuscompare`:
  the combined LocusCompare + LocusZoom figure, via plotnine.
- Bring-your-own LD through the `ld=` argument of `locuscompare`.

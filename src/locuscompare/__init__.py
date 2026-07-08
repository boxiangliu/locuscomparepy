"""locuscompare: visualize GWAS-QTL colocalization events.

Python port of the R package ``locuscomparer``
(https://github.com/boxiangliu/locuscomparer).
"""
from .analysis import assign_color, get_lead_snp
from .core import locuscompare
from .datasets import example_path
from .db import get_position, retrieve_LD
from .io import read_metal
from .plot import make_combined_plot, make_locuszoom, make_scatterplot

__version__ = "0.1.0"
__all__ = [
    "read_metal",
    "get_position",
    "retrieve_LD",
    "get_lead_snp",
    "assign_color",
    "make_scatterplot",
    "make_locuszoom",
    "make_combined_plot",
    "locuscompare",
    "example_path",
]

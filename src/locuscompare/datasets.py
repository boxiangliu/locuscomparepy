"""Access to bundled example datasets."""
from importlib import resources


def example_path(name):
    """Return the filesystem path to a bundled example file.

    Examples
    --------
    >>> example_path("gwas.tsv")  # doctest: +SKIP
    '.../locuscompare/data/gwas.tsv'
    """
    return str(resources.files("locuscompare.data").joinpath(name))

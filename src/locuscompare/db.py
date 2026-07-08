"""Reference-database queries (port of R ``get_position`` and ``retrieve_LD``)."""
import pandas as pd
import pymysql

from .config import get_db_config


def _connect():
    cfg = get_db_config()
    return pymysql.connect(
        host=cfg["host"],
        user=cfg["user"],
        password=cfg["password"],
        port=cfg["port"],
        database=cfg["database"],
    )


def _query(sql, params=None):
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or [])
            cols = [c[0] for c in cur.description]
            rows = cur.fetchall()
    finally:
        conn.close()
    return pd.DataFrame(rows, columns=cols)


def get_position(x, genome="hg19"):
    """Append ``chr`` and ``pos`` by looking up rsIDs in ``tkg_p3v5a_<genome>``."""
    if genome not in ("hg19", "hg38"):
        raise ValueError("genome must be 'hg19' or 'hg38'.")
    if "rsid" not in x.columns:
        raise ValueError("input must have an 'rsid' column.")
    rsids = x["rsid"].astype(str).tolist()
    if not rsids:
        raise ValueError("input has no rsIDs.")
    placeholders = ",".join(["%s"] * len(rsids))
    sql = f"SELECT rsid, chr, pos FROM tkg_p3v5a_{genome} WHERE rsid IN ({placeholders})"
    res = _query(sql, rsids)
    return x.merge(res, on="rsid")


def retrieve_LD(chr, snp, population):
    """Retrieve pairwise LD r2 for ``snp`` (only r2 > 0.2 is stored in the DB)."""
    table = f"tkg_p3v5a_ld_chr{chr}_{population}"
    a = _query(f"SELECT SNP_A, SNP_B, R2 FROM {table} WHERE SNP_A = %s", [snp])
    b = _query(f"SELECT SNP_B AS SNP_A, SNP_A AS SNP_B, R2 FROM {table} WHERE SNP_B = %s", [snp])
    return pd.concat([a, b], ignore_index=True)

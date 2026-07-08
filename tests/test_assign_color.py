import pandas as pd

from locuscompare import assign_color


def test_lead_is_purple_and_ld_colors():
    ld = pd.DataFrame(
        {"SNP_A": ["rs1"] * 3, "SNP_B": ["rs2", "rs3", "rs4"], "R2": [0.9, 0.5, 0.1]}
    )
    colors = assign_color(["rs1", "rs2", "rs3", "rs4", "rs5"], "rs1", ld)
    assert colors["rs1"] == "purple"       # lead SNP
    assert colors["rs2"] == "red"          # 0.9 -> (0.8, 1]
    assert colors["rs3"] == "darkgreen"    # 0.5 -> (0.4, 0.6]
    assert colors["rs4"] == "blue4"        # 0.1 -> [0, 0.2]
    assert colors["rs5"] == "blue4"        # no LD record -> default


def test_lead_added_if_absent_from_rsid_list():
    ld = pd.DataFrame({"SNP_A": ["rsX"], "SNP_B": ["rsY"], "R2": [0.5]})
    colors = assign_color(["rsY"], "rsX", ld)
    assert colors["rsX"] == "purple"
    assert colors["rsY"] == "darkgreen"

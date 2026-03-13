from __future__ import annotations

MANUSCRIPT_TARGETS = {
    "domain_1_v_0p1_t_30p0": {"A": 0.970, "B": 1.321, "R0": 0.0},
    "domain_2_v_0p1_t_30p0": {"A": 1.848, "B": 1.135, "R0": 1.292},
}


def get_target(base_name: str):
    return MANUSCRIPT_TARGETS.get(base_name)

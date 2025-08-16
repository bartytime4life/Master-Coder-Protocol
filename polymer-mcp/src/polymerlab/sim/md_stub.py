"""
MD Simulation Stub: generate a synthetic density-vs-temperature curve and estimate Tg by
simple piecewise-linear intersection. Saves CSV, plot PNG, and tg text.
"""
from __future__ import annotations

import os
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml


def _synthesize_density(T: np.ndarray, Tg: float) -> np.ndarray:
    """Simple piecewise-linear density model with a slope change at Tg."""
    dens = np.where(
        T < Tg,
        1.02 - 3e-4 * (T - Tg),
        0.98 - 8e-4 * (T - Tg),
    )
    return dens


def run_md_cooling(conf_path: str) -> Tuple[float, str, str]:
    conf = yaml.safe_load(open(conf_path, "r", encoding="utf-8"))
    out_csv = conf["output"]["csv"]
    out_png = conf["output"]["plot_png"]
    out_txt = conf["output"]["tg_txt"]
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    os.makedirs(os.path.dirname(out_png), exist_ok=True)

    T = np.linspace(conf["protocol"]["cool"]["end_C"], conf["protocol"]["cool"]["start_C"], 150)
    Tg_true = 105.0
    dens = _synthesize_density(T, Tg_true)

    n = len(T)
    lo_idx = slice(0, int(0.4 * n))
    hi_idx = slice(int(0.6 * n), n)
    coeff_lo = np.polyfit(T[lo_idx], dens[lo_idx], 1)
    coeff_hi = np.polyfit(T[hi_idx], dens[hi_idx], 1)
    a1, b1 = coeff_lo
    a2, b2 = coeff_hi
    Tg_est = (b2 - b1) / (a1 - a2)

    df = pd.DataFrame({"T_C": T, "density_g_cm3": dens})
    df.to_csv(out_csv, index=False)

    plt.figure()
    plt.plot(T, dens)
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Density (g/cm³)")
    plt.title("Synthetic MD cooling curve")
    plt.tight_layout()
    plt.savefig(out_png, dpi=180)
    plt.close()

    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(f"{Tg_est:.2f}\n")

    return Tg_est, out_csv, out_png

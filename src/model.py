from __future__ import annotations
import pandas as pd
import numpy as np
from typing import Dict, List

PARTIES = ['Ap','H','FrP','SV','Sp','V','KrF','MDG','R','Andre']

def recency_weights(dates: pd.Series, half_life_days: int = 21) -> pd.Series:
    today = pd.Timestamp.today().normalize()
    d = pd.to_datetime(dates, errors='coerce').fillna(today)
    dt = (today - d).dt.days.clip(lower=0)
    lam = np.log(2)/half_life_days
    w = np.exp(-lam * dt)
    return w / (w.sum() if w.sum() else 1.0)

def weighted_average(df: pd.DataFrame, weight_col: str) -> pd.Series:
    w = df[weight_col].values.reshape(-1,1)
    vals = df[PARTIES].fillna(0.0).values
    wa = (w * vals).sum(axis=0) / (w.sum() + 1e-9)
    return pd.Series(wa, index=PARTIES)

def simulate_majority(avg: pd.Series, n_draws: int = 20000, threshold: float = 4.0) -> Dict[str, float]:
    p = avg.clip(lower=0)
    p = p / p.sum()
    k = 500.0
    alpha = p * k + 1e-6
    draws = np.random.dirichlet(alpha, size=n_draws)
    draws = np.where(draws*100 >= threshold, draws, 0.0)
    draws = draws / draws.sum(axis=1, keepdims=True)
    seats = np.round(draws * 169).astype(int)
    left_idx = [PARTIES.index(p) for p in ['Ap','SV','Sp','R','MDG'] if p in PARTIES]
    right_idx = [PARTIES.index(p) for p in ['H','FrP','V','KrF'] if p in PARTIES]
    left_seats = seats[:, left_idx].sum(axis=1)
    right_seats = seats[:, right_idx].sum(axis=1)
    return {
        'left_majority_prob': float((left_seats >= 85).mean()),
        'right_majority_prob': float((right_seats >= 85).mean())
    }

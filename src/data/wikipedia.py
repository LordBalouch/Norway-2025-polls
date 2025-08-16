from __future__ import annotations
import pandas as pd
import re
from datetime import datetime
from typing import List, Dict, Any, Tuple

WIKI_URL = "https://en.wikipedia.org/wiki/Opinion_polling_for_the_2025_Norwegian_parliamentary_election"

PARTY_MAP = {
    'Ap': 'Ap', 'Labour': 'Ap',
    'H': 'H', 'Conservative': 'H',
    'Frp': 'FrP', 'FrP': 'FrP', 'Progress': 'FrP',
    'SV': 'SV',
    'Sp': 'Sp', 'Centre': 'Sp',
    'V': 'V', 'Liberal': 'V',
    'KrF': 'KrF', 'Christian Democratic': 'KrF',
    'MDG': 'MDG', 'Green': 'MDG',
    'R': 'R', 'Red': 'R',
    'Others': 'Andre', 'Other': 'Andre'
}

def _standardize_party_cols(cols: List[str]) -> List[str]:
    std = []
    for c in cols:
        c_clean = re.sub(r"\[.*?\]", "", c)
        c_clean = c_clean.strip()
        c_clean = re.sub(r"\s*%$", "", c_clean)
        std.append(PARTY_MAP.get(c_clean, c_clean))
    return std

def fetch_wikipedia_polls() -> pd.DataFrame:
    dfs = pd.read_html(WIKI_URL)
    candidates = []
    for df in dfs:
        cols = _standardize_party_cols([str(c) for c in df.columns])
        if any(p in cols for p in ['Ap','H','FrP','SV','Sp','V','KrF','MDG','R']):
            df.columns = cols
            candidates.append(df)
    if not candidates:
        raise RuntimeError("Fant ingen tabeller med partikolonner på Wikipedia-siden.")
    df = max(candidates, key=lambda d: d.shape[1]).copy()
    rename_map = {
        'Polling firm': 'pollster',
        'Client': 'client',
        'Fieldwork date(s)': 'fieldwork',
        'Date(s) conducted': 'fieldwork',
        'Sample size': 'sample_size',
        'Population': 'population',
        'Source': 'url',
        'Link': 'url'
    }
    df.rename(columns={k:v for k,v in rename_map.items() if k in df.columns}, inplace=True)
    party_cols = [c for c in df.columns if c in ['Ap','H','FrP','SV','Sp','V','KrF','MDG','R','Andre']]
    for c in party_cols:
        df[c] = (df[c].astype(str)
                 .str.replace(',', '.')
                 .str.extract(r'([0-9]+(?:\.[0-9]+)?)')[0]
                 .astype(float))
    if 'sample_size' in df.columns:
        df['sample_size'] = (df['sample_size'].astype(str)
                             .str.replace(r'[^0-9]', '', regex=True)
                             .replace('', None)
                             .astype(float))
    def parse_fieldwork(s: str) -> Tuple[str,str]:
        if not isinstance(s, str):
            return None, None
        s = s.replace('–','-').replace('—','-')
        parts = re.split(r'\s*[–-]\s*', s)
        try:
            if len(parts)==2:
                end = pd.to_datetime(parts[1], dayfirst=True, errors='coerce')
                start = pd.to_datetime(parts[0] + ' ' + str(end.year), dayfirst=True, errors='coerce') if pd.notnull(end) else pd.NaT
            else:
                start = end = pd.to_datetime(s, dayfirst=True, errors='coerce')
        except Exception:
            start = end = pd.NaT
        return (start.date().isoformat() if pd.notnull(start) else None,
                end.date().isoformat() if pd.notnull(end) else None)
    if 'fieldwork' in df.columns:
        starts, ends = zip(*df['fieldwork'].map(parse_fieldwork))
        df['fieldwork_start'] = starts
        df['fieldwork_end'] = ends
    if 'url' not in df.columns and 'Source' in df.columns:
        df['url'] = df['Source']
    keep_cols = ['pollster','client','fieldwork_start','fieldwork_end','sample_size','population','url'] + party_cols
    df = df[[c for c in keep_cols if c in df.columns]].dropna(how='all')
    df['source'] = 'wikipedia'
    return df

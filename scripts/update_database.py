#!/usr/bin/env python3
from __future__ import annotations
import argparse
import pandas as pd
from src.db import get_conn, init_db, insert_poll
from src.data.wikipedia import fetch_wikipedia_polls

def ingest_wikipedia(conn):
    df = fetch_wikipedia_polls()
    for _, row in df.iterrows():
        meta = {
            'source': 'wikipedia',
            'pollster': row.get('pollster'),
            'client': row.get('client'),
            'fieldwork_start': row.get('fieldwork_start'),
            'fieldwork_end': row.get('fieldwork_end'),
            'publish_date': None,
            'sample_size': int(row['sample_size']) if pd.notnull(row.get('sample_size')) else None,
            'population': row.get('population'),
            'url': row.get('url')
        }
        results = {p: row.get(p) for p in ['Ap','H','FrP','SV','Sp','V','KrF','MDG','R','Andre'] if p in row.index}
        insert_poll(conn, meta, results)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', choices=['wikipedia'], default='wikipedia')
    args = ap.parse_args()
    conn = get_conn()
    init_db(conn)
    if args.source == 'wikipedia':
        ingest_wikipedia(conn)
    print('OK')

if __name__ == '__main__':
    main()

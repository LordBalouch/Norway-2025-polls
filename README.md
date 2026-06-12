# Norway 2025 Election Polls — Forecast & Post-Election Review

End-to-end pipeline that forecasted the 2025 Norwegian parliamentary election from public polling data, and an honest comparison of the model's predictions against the actual result on 8 September 2025.

## Project overview

I built a reproducible workflow to collect, clean, explore, and model Norwegian polling data for the 2025 Storting election using Python, SQLite, and Jupyter.

- Automated poll collection from pollofpolls.no and seed CSVs
- SQLite database for consistent querying
- EDA of party trends (rolling 4w and 12w averages)
- Bayesian forecast model in PyMC (Dirichlet prior, Multinomial likelihood, MCMC)
- Coalition analysis: posterior probability of red-bloc vs blue-bloc majority

The election took place on 8 September 2025, so the README now includes a post-election review of how the model performed against the real outcome.

See also: [`ETHICS.md`](ETHICS.md) — notes on data sources, scope, and limitations.

## Model prediction (before the election)

The Bayesian model gave the following headline outputs:

- **Red-bloc majority probability: ~73%**
- **Blue-bloc majority probability: ~27%**
- Strongest parties in the posterior: Ap ~27–28%, H ~18–20%, FrP ~20–22%

## Actual result (8 September 2025)

- **Ap 28.0%** (53 seats) — remained the largest party
- **FrP 23.9%** (47 seats) — biggest gain of the night, +12.3 pp
- **H 14.6%** (24 seats)
- Sp 5.6%, SV 5.6%, R 5.3%, MDG 4.7%, KrF 4.2%, V 3.7%
- **Red bloc: 88 seats. Blue bloc: 81 seats.** (85 needed for majority.)

The red bloc won by a narrow 5-seat margin, and Jonas Gahr Støre remained Prime Minister.

Sources: [valgresultat.no](https://valgresultat.no/valg/2025/st), [Wikipedia — 2025 Norwegian parliamentary election](https://en.wikipedia.org/wiki/2025_Norwegian_parliamentary_election).

## Post-election review — what the model got right and wrong

**What the model got right**
- **Predicted the winning bloc.** Red-bloc majority at ~73% — and that's what happened.
- **Ap landing point.** Posterior centred at ~27–28%; the actual share was 28.0%.
- **Narrow margin not ruled out.** The 27% probability of a blue-bloc majority reflected a genuinely live scenario — the result came down to a 5-seat gap.

**What the model missed**
- **Underestimated FrP.** Posterior ~20–22% vs an actual 23.9%. The late-campaign FrP surge (+12.3 pp on 2021) wasn't fully picked up.
- **Overestimated Høyre.** Posterior ~18–20% vs an actual 14.6%. Some of what the model gave to H likely flowed to FrP on the right.

**What I'd do differently**
- Weight polls closer to election day more heavily (recency-weighted likelihood), to catch late shifts like the FrP surge.
- Model the H/FrP correlation explicitly rather than treat parties as independent — voters moved between them, and the priors should reflect that.
- Track forecast vs outcome at every poll release, not just once, so calibration can be evaluated over the campaign.

The model got the macro call right (which bloc won) and was on the money for the largest party. Where it stumbled was on the second- and third-place reshuffle inside the blue bloc — a real, instructive miss rather than a fatal one.

## Repository structure

```
Norway-2025-polls/
├── data/
│   ├── raw/          # Raw input polls
│   └── processed/    # SQLite database with cleaned polls
├── notebooks/
│   ├── 01_ingest_polls.ipynb     # Data ingestion + SQL setup
│   └── 02_eda_and_model.ipynb    # EDA + Bayesian forecast
├── scripts/
│   └── fetch_pollofpolls_monthly.py   # Scraper for monthly averages
├── ETHICS.md          # Data sources, scope, limitations
├── requirements.txt   # Python dependencies
└── README.md
```

## How to run

### 1. Setup environment

```
git clone https://github.com/LordBalouch/Norway-2025-polls.git
cd Norway-2025-polls
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run notebooks

Open JupyterLab or VS Code with the `Norway-Polls` Python kernel:

- `01_ingest_polls.ipynb` — loads polls into SQLite and verifies the dataset
- `02_eda_and_model.ipynb` — runs EDA and the Bayesian forecast model

### 3. Refresh data

Fetch monthly averages from pollofpolls.no:

```
PYTHONPATH=. python scripts/fetch_pollofpolls_monthly.py --year 2025
```

## Skills demonstrated

- **Data collection & cleaning** — CSV ingestion, regex scraping, SQL upserts
- **Database** — SQLite with pandas
- **EDA** — time-series visualisation of party trends, rolling averages
- **Bayesian modelling in PyMC** — Dirichlet prior + Multinomial likelihood, MCMC, posterior credible intervals
- **Coalition analysis** — posterior probability of red-bloc vs blue-bloc majority
- **Honest evaluation** — comparing model output to the realised outcome and articulating what to change next time
- **Reproducibility** — venv, requirements, modular scripts

## Author

Babak Balouch — Data Analyst, Norway

# Prediksjon av Stortingsvalget 2025 (Norge)

En reproduserbar, gratis pipeline som henter siste meningsmålinger, analyserer og predikerer partienes oppslutning og sannsynligheten for blokkflertall.

## Innhold
- **Datainnhenting** fra åpne kilder (Wikipedia, Pollofpolls, PolitPro) til SQLite.
- **EDA** og enkel modell (vekting av målinger + simulering) for å predikere oppslutning.
- **Blokk-/koalisjonsanalyse** via konfigurerbar blokkinndeling og sannsynlighetsmatrise.
- **Evaluering** mot fasit etter valget.
- **Etikk og transparens** i `ETHICS.md` og `MODELCARD.md`.

> Merk: Kildene har ofte ingen offisiell API-støtte. Parsing skjer fra offentlig tilgjengelige HTML-tabeller. Respekter vilkår og ikke overbelast sidene.

## Hurtigstart
```bash
# 1) Lag og aktiver venv (anbefalt)
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# 2) Installer avhengigheter
pip install -r requirements.txt
# 3) Oppdater databasen med siste målinger (Wikipedia-connector som eksempel)
python scripts/update_database.py --source wikipedia
# 4) Åpne notebook for EDA/model
jupyter lab
```

## Struktur
```
norway-2025-polls/
├─ data/
│  ├─ raw/
│  └─ processed/
├─ notebooks/
│  ├─ 01_ingest_polls.ipynb
│  └─ 02_eda_and_model.ipynb
├─ src/
│  ├─ data/
│  │  └─ wikipedia.py
│  ├─ utils/
│  │  └─ party_maps.py
│  ├─ db.py
│  └─ model.py
├─ scripts/
│  └─ update_database.py
├─ config/
│  ├─ parties.yml
│  └─ blocks.yml
├─ ETHICS.md
├─ MODELCARD.md
├─ requirements.txt
├─ LICENSE
└─ .gitignore
```

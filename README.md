# Norway 2025 Election Polls – Data Analysis & Forecasting

## Project Overview
This project analyzes and models the Norwegian 2025 Parliamentary Election polls.  
I built an end-to-end workflow to collect, clean, explore, and model polling data using Python, SQL, and Jupyter Notebooks.

The main goals were:
- Automate poll collection from pollofpolls.no and seed CSV data.  
- Store and query polls in a SQLite database.  
- Perform Exploratory Data Analysis (EDA) of party trends.  
- Train a Bayesian election forecast model.  
- Communicate results with clear visualizations.  

This project is structured for portfolio demonstration to highlight practical data analyst and data science skills.

---

## Repository Structure

```
Norway-2025-polls/
│
├── data/
│   ├── raw/          # Raw input polls
│   ├── processed/    # SQLite database with cleaned polls
│
├── notebooks/
│   ├── 01_ingest_polls.ipynb     # Data ingestion + SQL setup
│   ├── 02_eda_and_model.ipynb    # EDA + forecasting model
│
├── scripts/
│   ├── fetch_pollofpolls_monthly.py   # Scraper for monthly averages
│
├── requirements.txt   # Python dependencies
├── README.md          # Project documentation (this file)
```

---

## How to Run

### 1. Setup environment
```bash
# Clone repo
git clone https://github.com/YOUR-USERNAME/Norway-2025-polls.git
cd Norway-2025-polls

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run notebooks
Open JupyterLab or VSCode, and select kernel "Python (Norway-Polls)".

- 01_ingest_polls.ipynb → loads polls into SQLite and verifies dataset.  
- 02_eda_and_model.ipynb → runs EDA and the forecasting model.  

### 3. Update data
Fetch monthly averages from pollofpolls.no:
```bash
PYTHONPATH=. python scripts/fetch_pollofpolls_monthly.py --year 2025
```

---

## Results

- Polls are centralized in SQLite for consistent querying.  
- Exploratory plots show recent shifts:  
  - FRP trending upwards (>20%)  
  - Høyre trending downwards (<20%)  
  - Arbeiderpartiet stabilizing around 27–28%  

- A Bayesian election model produces:  
  - Posterior party vote share distributions  
  - Probability estimates for left vs right majority  

---

## Skills Demonstrated

- Data Collection & Cleaning: CSV ingestion, regex scraping, SQL upserts.  
- Database Management: SQLite integration with pandas.  
- Exploratory Data Analysis: Visualization of time series and party trends.  
- Bayesian Forecasting: Simple probabilistic model for seat projections.  
- Reproducibility: Virtual environment + requirements.txt + modular scripts.  

---

## Next Steps

- Automate daily poll updates via GitHub Actions.  
- Add interactive dashboard (Streamlit or Databutton).  
- Extend forecast with coalition simulations.  

---

## Author

Babak Balouch 
Data Analyst
Norway  


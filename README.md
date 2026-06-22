# U.S.-Iran Conflict Oil Risk Analytics

**A Python-based business analytics project analyzing how U.S.-Iran geopolitical conflict risk affects oil prices, U.S. gasoline prices, market volatility, media attention, and business decision-making.**

This repository is designed as a **GitHub portfolio-quality data analytics project** for Business Analytics, Data Analyst, BI Analyst, and entry-level Data Science roles. It uses public data sources, reproducible Python code, event-study logic, time-series analysis, regression, predictive modeling, and business-facing risk scoring.

> **Important:** This project does not fake results. It fetches current public data when you run the pipeline. The event dates in `config/config.yaml` are editable so the project can be updated when the conflict timeline changes.

---

## 1. Executive Summary

The U.S.-Iran conflict matters to business analytics because geopolitical risk can quickly move energy prices, consumer fuel costs, inflation expectations, financial markets, and business operating costs. The most important mechanism is the **Strait of Hormuz**, a critical oil chokepoint connecting the Persian Gulf with global markets.

The project investigates whether conflict-related news attention and event windows are associated with changes in:

- WTI crude oil prices
- Brent crude oil prices
- U.S. gasoline prices
- Brent-WTI spread
- market volatility
- S&P 500 performance
- business risk indicators

The goal is not only to analyze oil prices, but to show how a data analyst can translate a geopolitical event into **business decisions**, such as fuel-cost planning, pricing strategy, risk monitoring, executive reporting, and dashboard design.

---

## 2. Business Problem

Companies exposed to transportation, delivery, manufacturing, consumer spending, advertising, or subscription revenue need to understand how geopolitical shocks affect business conditions.

A conflict involving Iran can affect U.S. business through:

1. higher crude oil prices;
2. higher gasoline prices;
3. higher freight and logistics costs;
4. inflation pressure;
5. market volatility;
6. changing consumer behavior;
7. uncertainty in executive planning.

This project answers a practical business question:

> **How can a data analytics team detect, measure, visualize, and communicate the business impact of U.S.-Iran oil-risk events?**

---

## 3. Research Questions

### Research Question 1

**How did crude oil and U.S. gasoline prices behave before, during, and after the Iran conflict event window?**

**Why it matters:**  
This tells decision-makers whether the conflict created a measurable energy-price shock and whether prices normalized after de-escalation.

**Methods used:**

- before/after event-window comparison
- descriptive statistics
- boxplots
- time-series visualization
- Brent-WTI spread analysis

**Expected output:**

- `data/processed/before_after_summary.csv`
- `reports/figures/01_oil_prices_event_window.png`
- `reports/figures/02_oil_to_gasoline_pass_through.png`
- `reports/figures/04_before_after_wti_boxplot.png`

---

### Research Question 2

**Does conflict-related news attention help explain short-term oil-price movement?**

**Why it matters:**  
Markets often price geopolitical risk before physical supply is fully disrupted. If media attention rises alongside oil-price movement, analysts can use news volume as an early warning signal.

**Methods used:**

- GDELT news timeline volume
- daily WTI returns
- robust OLS regression
- correlation matrix
- market control variables such as VIX and S&P 500 returns

**Expected output:**

- `data/processed/news_oil_regression.csv`
- `reports/figures/03_gdelt_news_attention.png`
- `reports/figures/06_correlation_matrix.png`

**Important interpretation rule:**  
Regression results show statistical association, not automatic causation. A high coefficient does not prove media attention caused oil prices to rise; it shows whether news attention and oil-price changes moved together after controlling for available market indicators.

---

### Research Question 3

**How strongly do oil-price changes pass through to U.S. gasoline prices, and how can this be converted into a business risk score?**

**Why it matters:**  
Gasoline prices affect consumers, delivery costs, commuting, logistics, inflation expectations, and company margins. A business-facing risk index helps executives understand when energy risk becomes operationally important.

**Methods used:**

- lag correlation between WTI changes and gasoline changes
- gasoline price prediction model
- business risk scoring
- risk-level classification
- interactive map of strategic locations

**Expected output:**

- `data/processed/lag_correlation_oil_gas.csv`
- `data/processed/gasoline_prediction_model.csv`
- `data/processed/business_risk_index.csv`
- `reports/figures/05_lag_correlation_oil_gas.png`
- `reports/maps/hormuz_oil_risk_map.html`

---

## 4. Data Sources

| Source | Dataset | Use in Project | Link |
|---|---|---|---|
| FRED / EIA | WTI crude oil, `DCOILWTICO` | U.S. crude benchmark | https://fred.stlouisfed.org/series/DCOILWTICO |
| FRED / EIA | Brent crude oil, `DCOILBRENTEU` | Global crude benchmark | https://fred.stlouisfed.org/series/DCOILBRENTEU |
| FRED / EIA | U.S. regular gasoline, `GASREGW` | Consumer fuel-price impact | https://fred.stlouisfed.org/series/GASREGW |
| FRED / BLS | CPI, `CPIAUCSL` | Inflation context | https://fred.stlouisfed.org/series/CPIAUCSL |
| FRED / BEA | PCE price index, `PCEPI` | Inflation context | https://fred.stlouisfed.org/series/PCEPI |
| FRED | VIX, `VIXCLS` | market stress | https://fred.stlouisfed.org/series/VIXCLS |
| FRED | S&P 500, `SP500` | broad equity market response | https://fred.stlouisfed.org/series/SP500 |
| GDELT | Doc API timeline volume | news attention proxy | https://www.gdeltproject.org/data.html |
| EIA / IEA | Strait of Hormuz facts | oil chokepoint context | https://www.eia.gov/todayinenergy/detail.php?id=65504 and https://www.iea.org/about/oil-security-and-emergency-response/strait-of-hormuz |

---

## 5. Project Architecture

```text
iran_oil_conflict_analytics_project/
│
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
│
├── config/
│   └── config.yaml
│
├── data/
│   ├── raw/
│   │   ├── strategic_locations.csv
│   │   └── fred_*.csv                  # generated by pipeline
│   └── processed/
│       ├── master_timeseries.csv       # generated by pipeline
│       ├── before_after_summary.csv
│       ├── lag_correlation_oil_gas.csv
│       ├── news_oil_regression.csv
│       ├── gasoline_prediction_model.csv
│       └── business_risk_index.csv
│
├── src/
│   ├── fetch_fred.py                   # downloads FRED energy/macro data
│   ├── fetch_gdelt.py                  # downloads news attention data
│   ├── build_features.py               # creates master time-series dataset
│   ├── analysis.py                     # runs statistical analysis
│   ├── visualize.py                    # creates charts and graphs
│   ├── maps.py                         # creates interactive map
│   ├── business_impact_model.py        # creates business risk index
│   ├── run_pipeline.py                 # one-command pipeline
│   └── utils.py
│
├── reports/
│   ├── figures/                        # PNG charts generated here
│   └── maps/                           # interactive HTML map generated here
│
├── notebooks/                          # optional exploratory notebooks
├── docs/
│   ├── data_dictionary.md
│   └── research_design.md
└── tests/
    └── test_config.py
```

---

## 6. Methodology

### 6.1 Event-Window Design

The analysis uses configurable event windows:

- **Pre-conflict period:** normal baseline before escalation
- **Conflict period:** escalation / active disruption risk
- **De-escalation period:** tentative agreement or stabilization period

These dates are defined in `config/config.yaml`:

```yaml
event_windows:
  baseline_start: "2025-01-01"
  pre_conflict_end: "2026-02-27"
  conflict_start: "2026-02-28"
  tentative_deescalation_start: "2026-06-15"
  analysis_end: "2026-06-21"
```

If your instructor, article, or data source defines a different conflict timeline, update the config and rerun the pipeline.

---

### 6.2 Before / After Analysis

The project compares average, median, standard deviation, minimum, and maximum values across periods. This answers whether the conflict period had different oil and gasoline price behavior compared with the pre-conflict period.

Metrics include:

- WTI crude price
- Brent crude price
- U.S. regular gasoline price
- Brent-WTI spread
- VIX
- S&P 500
- GDELT news attention

---

### 6.3 News Attention Analysis

The project uses the GDELT Doc API timeline volume as a proxy for media attention. The query focuses on Iran, Hormuz, oil, crude, gasoline, tankers, sanctions, and energy.

Example query:

```text
(Iran OR Iranian OR Hormuz OR "Strait of Hormuz")
(oil OR crude OR gasoline OR tanker OR energy OR sanctions)
```

This produces a daily time series showing the share of online news matching the query. The pipeline compares this attention signal to oil-price returns.

---

### 6.4 Lag Analysis

Oil-price changes do not always affect gasoline prices immediately. The project calculates correlations where oil-price changes lead gasoline-price changes by 0 to 21 days.

This helps identify whether gasoline prices react with a delay.

---

### 6.5 Predictive Modeling

The project trains a simple linear regression model to predict gasoline prices using features such as:

- WTI crude price
- Brent crude price
- Brent-WTI spread
- VIX
- federal funds rate
- news attention

This model is intentionally explainable. For a portfolio project, interpretability is more valuable than a black-box model.

---

### 6.6 Business Risk Index

The project creates a business-facing risk index based on standardized components:

- oil shock score
- consumer fuel pressure score
- market volatility score
- geopolitical attention score

The final index is classified into:

- Low
- Normal
- Elevated
- High

This helps executives understand when geopolitical energy risk is becoming operationally important.

---

## 7. How to Run the Project

### Step 1: Clone or download the repository

```bash
git clone https://github.com/your-username/iran-oil-conflict-analytics.git
cd iran-oil-conflict-analytics
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
# .venv\Scripts\activate       # Windows
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the full pipeline

```bash
python src/run_pipeline.py
```

### Step 5: Review outputs

Open:

```text
reports/figures/
reports/maps/hormuz_oil_risk_map.html
data/processed/
```

---

## 8. Expected Visualizations

The pipeline creates the following visuals:

| Chart | File | Purpose |
|---|---|---|
| Oil price event window | `01_oil_prices_event_window.png` | Shows WTI/Brent before, during, and after conflict window |
| Oil-to-gasoline pass-through | `02_oil_to_gasoline_pass_through.png` | Shows relationship between crude and gasoline prices |
| News attention | `03_gdelt_news_attention.png` | Shows Iran/Hormuz/oil media attention |
| Before-after boxplot | `04_before_after_wti_boxplot.png` | Compares WTI price distributions by period |
| Lag correlation | `05_lag_correlation_oil_gas.png` | Shows delayed gasoline response to oil changes |
| Correlation matrix | `06_correlation_matrix.png` | Shows relationships across energy, market, and news variables |
| Strategic map | `hormuz_oil_risk_map.html` | Interactive map of chokepoints and business hubs |

---

## 9. Business Use Cases

### 9.1 Executive Dashboard

A leadership team can use this project to track:

- current energy risk level;
- oil and gasoline price trend;
- market stress;
- news attention spikes;
- exposure of business operations to higher energy costs.

### 9.2 Pricing Strategy

If oil and gasoline prices rise, companies may need to adjust:

- delivery fees;
- subscription pricing;
- operating budgets;
- inventory timing;
- promotional strategy.

### 9.3 Streaming / Digital Business Impact

For a streaming or digital subscription business, Iran-related oil shocks may seem indirect, but they can still matter:

- higher gasoline and inflation reduce disposable income;
- households may cancel non-essential subscriptions;
- advertising demand can weaken if businesses face higher costs;
- consumer sentiment may decline during geopolitical stress;
- market volatility can affect technology-sector valuations.

This project can be extended with company-level customer data to analyze churn, engagement, and price sensitivity during macroeconomic shocks.

---

## 10. Data Quality and Limitations

This project is intentionally transparent about limitations:

1. **Correlation is not causation.** News attention and oil prices may move together without one directly causing the other.
2. **Event windows are assumptions.** Update `config.yaml` if the conflict timeline changes.
3. **GDELT is a media proxy.** It measures news attention, not actual conflict severity.
4. **Gasoline prices are not only crude oil.** Taxes, refining, inventories, seasonal demand, and regional supply also matter.
5. **Daily and weekly data are mixed.** Weekly gasoline data is forward-filled for daily alignment.
6. **The model is explainable, not perfect.** It is designed for business interpretation, not high-frequency trading.

---

## 11. Resume Bullet Ideas

Use only after you have run the project and verified the outputs:

- Built an end-to-end Python analytics pipeline to measure the impact of U.S.-Iran geopolitical risk on oil, gasoline, market volatility, and business risk indicators using FRED, EIA, and GDELT data.
- Developed before/after event-window analysis, lag correlation, regression modeling, and interactive geospatial visualization to quantify oil-price shocks and U.S. gasoline pass-through.
- Created an executive-ready business risk index translating energy-market volatility and news attention into actionable risk levels for pricing, operations, and strategic planning.

---

## 12. Future Improvements

Possible extensions:

- add sector ETFs such as XLE, JETS, XRT, and SPY;
- build a Streamlit dashboard;
- add sentiment analysis from news headlines;
- use Prophet or ARIMA for forecasting;
- add regional gasoline price data by U.S. state;
- connect to a streaming-platform churn dataset;
- deploy dashboard on Streamlit Cloud;
- add automated GitHub Actions pipeline.

---

## 13. Key Skills Demonstrated

- Python
- pandas / NumPy
- time-series analysis
- regression modeling
- predictive modeling
- event-study design
- news analytics
- geospatial visualization
- business risk scoring
- data storytelling
- GitHub project organization
- reproducible analytics pipeline

---

## 14. References

- U.S. Energy Information Administration, Strait of Hormuz oil chokepoint: https://www.eia.gov/todayinenergy/detail.php?id=65504
- International Energy Agency, Strait of Hormuz overview: https://www.iea.org/about/oil-security-and-emergency-response/strait-of-hormuz
- FRED WTI crude oil: https://fred.stlouisfed.org/series/DCOILWTICO
- FRED Brent crude oil: https://fred.stlouisfed.org/series/DCOILBRENTEU
- FRED U.S. gasoline price: https://fred.stlouisfed.org/series/GASREGW
- FRED CPI: https://fred.stlouisfed.org/series/CPIAUCSL
- GDELT data documentation: https://www.gdeltproject.org/data.html

---

## 15. Project Owner

**Kiran Kanth Madigani**  
MS Business Analytics | Data Analytics | Python | SQL | Power BI | Machine Learning

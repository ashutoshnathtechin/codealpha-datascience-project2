# TASK 2: Unemployment Analysis with Python

> An end-to-end data science investigation analyzing macroeconomic labor market dynamics in India, the impact of the COVID-19 pandemic and nationwide lockdown, rural vs. urban disparities, regional vulnerability, and evidence-based economic policy recommendations. Includes an interactive localhost web dashboard.

---

## 🌐 Live Localhost Web Application

The interactive web dashboard is running live on:
👉 **[http://localhost:5005](http://localhost:5005)** or **[http://127.0.0.1:5005](http://127.0.0.1:5005)**

### Features:
- **Interactive KPI Ribbon**: Live metrics for Pre-Lockdown, Lockdown Peak, Recovery, Displaced Workforce, and Labour Force Participation Drop.
- **National Trajectory & Trends**: Monthly trends of unemployment rate vs active workforce.
- **Urban vs. Rural Divergence**: Comparative area chart showing the urban vulnerability penalty.
- **State-by-State Lockdown Shock**: Interactive ranking of all 27 states by shock intensity.
- **Interactive Geospatial Map of India**: Leaflet.js-powered map with color-coded markers for each Indian state.
- **5 Strategic Policy Pillars**: Interactive action matrix and recommendations for economic resiliency.
- **Live Data Explorer**: Filterable and searchable table with instant CSV export.
- **Publication Figures Gallery**: High-resolution PNGs generated from Seaborn & Matplotlib.

---

## 📊 Key Empirical Findings

### 1. The COVID-19 Lockdown Shock (The "Sudden Stop")
- **National Unemployment Spike**: Surged from **9.76%** (Pre-Lockdown average) to a peak of **22.75%** during the nationwide lockdown (April–May 2020), representing a **+133.06% relative surge** (+12.99 percentage points).
- **Workforce Contraction**: Total active employed workforce plummeted from **400.6 million** to **292.8 million**—a sudden displacement of **over 107.8 million jobs** (and over 131 million at its lowest April trough).
- **Discouraged Worker Effect**: The Labour Force Participation Rate (LFPR) plunged from **44.18%** down to **37.51%** (-6.67 pp drop), reflecting widespread discouragement and physical mobility restrictions.
- **Initial V-Shaped Rebound**: Post-lockdown (June–October 2020), headline unemployment normalized back to **9.56%**, aided by Unlock phases and rural absorption.

### 2. Urban vs. Rural Structural Divergence
| Pandemic Phase | Rural Unemployment Rate (%) | Urban Unemployment Rate (%) | Urban Excess Penalty (pp) |
|:---|:---:|:---:|:---:|
| **Pre-Lockdown** | 8.24% | 10.91% | +2.67 pp |
| **Lockdown Peak (Apr-May 2020)** | **21.48%** | **26.93%** | **+5.45 pp** |
| **Post-Lockdown (Jun 2020)** | 11.83% | 11.98% | +0.15 pp |

- **Urban Centers Suffered Disproportionately**: Urban unemployment reached nearly 27–28% due to total cessation of non-essential services, construction, manufacturing, and transportation.
- **Rural India as Economic Buffer**: Rural economies served as a shock-absorber for millions of reverse-migrant workers, cushioned by timely agricultural sowing (Kharif season) and emergency expansions of the MGNREGA program.

### 3. State-Level Sensitivity & Crisis Hotspots
- **Most Severely Impacted**:
  1. **Puducherry**: Skyrocketed from 1.18% to **67.02%** (+65.84 pp increase) due to severe tourism and informal service dependency.
  2. **Jharkhand**: Rose from 10.23% to **53.16%** (+42.93 pp increase).
  3. **Tamil Nadu**: Jumped from 3.35% to **41.50%** (+38.14 pp increase; +1,137% surge) due to industrial manufacturing closures.
  4. **Bihar**: Spiked from 12.11% to **46.30%** (+34.19 pp increase) from returning migrant worker influx.
  5. **Karnataka**: Rose from 3.31% to **24.90%** (+21.60 pp increase).
- **Most Resilient States**:
  - **Sikkim, Himachal Pradesh, Uttarakhand, Chhattisgarh, Meghalaya**: Maintained stability or counter-cyclical resilience due to self-reliant agrarian economies and early agricultural exemptions.

### 4. Macro-Zonal Impact
- **South Zone** and **East Zone** absorbed the steepest shock (+25.49 pp and +24.96 pp respectively).
- **North Zone** maintained the highest structural baseline (15.10%), driven by persistent unemployment in Haryana and Jammu & Kashmir.

---

## 🏛️ Policy Recommendations

1. **National Urban Employment Guarantee Scheme (NUEGS / DUET)**:
   - Establish a statutory 100-day guaranteed employment scheme in urban centers focused on municipal maintenance, green infrastructure, and climate adaptation.
2. **Shock-Responsive Parametric Cash Transfers (DBT)**:
   - Implement automated liquidity transfers linked to the Jan Dhan-Aadhaar-Mobile (JAM) trinity that trigger whenever district unemployment rates exceed standard deviation bands.
3. **Regional MSME Solvency & Stabilization Funds**:
   - Provide zero-interest collateral-free working capital lines to industrial hubs in Tamil Nadu, Maharashtra, and Karnataka, and establish agro-industrial clusters in labor-sending states like Bihar and Jharkhand.
4. **Post-Monsoon Rural Value Addition & Agro-Processing**:
   - Cushion rural seasonal volatility by financing Gram Panchayat cold-chain storage and Farmer Producer Organizations (FPOs).
5. **High-Frequency Real-Time Labor Market Intelligence**:
   - Upgrade from slow annual/quarterly surveys to weekly telemetry tracking EPFO payrolls, GST velocity, and digital labor indicators.

---

## 📁 Repository Structure

```
DATA SCIENTIST PROJECT 2/
├── Unemployment in India.csv              # Raw Dataset 1 (Rural vs Urban: May 2019 - Jun 2020)
├── Unemployment_Rate_upto_11_2020.csv     # Raw Dataset 2 (Macro Zonal: Jan 2020 - Oct 2020)
├── requirements.txt                      # Project dependencies
├── README.md                             # Comprehensive documentation
├── run_analysis.py                       # CLI runner for end-to-end data science pipeline
├── run_dashboard.py                      # Localhost Flask web server runner
├── generate_notebook.py                  # Jupyter notebook builder
├── data/
│   └── processed/
│       ├── df1_cleaned_rural_urban.csv   # Standardized clean dataset 1
│       └── df2_cleaned_zonal.csv         # Standardized clean dataset 2
├── src/
│   ├── data_preprocessing.py             # Data cleaning, header fixing, coordinate rectification
│   ├── eda_analysis.py                   # Statistical analysis, Covid shock metrics, rankings
│   ├── visualizations.py                 # Matplotlib & Seaborn publication figures
│   └── policy_insights.py                # Policy formulation module
├── notebooks/
│   └── unemployment_analysis.ipynb       # Interactive Jupyter Notebook
├── reports/
│   ├── Unemployment_Analysis_Report.md   # Executive markdown report
│   └── figures/                          # 9 high-resolution generated figures
│       ├── 01_national_unemployment_trend.png
│       ├── 02_covid_lockdown_shock_comparison.png
│       ├── 03_rural_vs_urban_unemployment.png
│       ├── 04_state_level_lockdown_shock.png
│       ├── 05_zonal_regional_impact.png
│       ├── 06_correlation_heatmap.png
│       ├── 07_labour_participation_drop.png
│       ├── 08_unemployment_distribution_boxplots.png
│       └── 09_seasonal_monthly_patterns.png
└── app/
    ├── app.py                            # Flask server with REST API endpoints
    └── templates/
        └── index.html                    # Responsive dashboard (Tailwind + Chart.js + Leaflet)
```

---

## 🚀 How to Run

### 1. Run the Complete Data Science Analysis Pipeline
```bash
python run_analysis.py
```
This cleans the data, calculates all statistical and shock metrics, generates all 9 publication figures in `reports/figures/`, and produces the executive report in `reports/Unemployment_Analysis_Report.md`.

### 2. Start the Localhost Interactive Web Dashboard
```bash
python run_dashboard.py
```
Open your browser and navigate to:
**`http://localhost:5005`** or **`http://127.0.0.1:5005`**

### 3. Run the Jupyter Notebook
```bash
jupyter notebook notebooks/unemployment_analysis.ipynb
```

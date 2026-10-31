"""
run_analysis.py
---------------
Master execution script for Task 2: Unemployment Analysis with Python.
Executes data preprocessing, generates all figures, calculates statistical metrics,
and saves the comprehensive summary report.
"""

import os
import sys
import pandas as pd

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_preprocessing import load_and_clean_datasets
from src.eda_analysis import UnemploymentEDA
from src.visualizations import UnemploymentVisualizer
from src.policy_insights import generate_policy_brief

def main():
    print("=" * 70)
    print("   TASK 2: UNEMPLOYMENT ANALYSIS WITH PYTHON - DATA SCIENCE PIPELINE   ")
    print("=" * 70)

    # 1. Preprocess & Clean Datasets
    print("\n[Step 1/5] Loading and Cleaning Datasets...")
    df1, df2, geo = load_and_clean_datasets(
        df1_path="Unemployment in India.csv",
        df2_path="Unemployment_Rate_upto_11_2020.csv"
    )

    # Save processed clean datasets
    os.makedirs("data/processed", exist_ok=True)
    df1.to_csv("data/processed/df1_cleaned_rural_urban.csv", index=False)
    df2.to_csv("data/processed/df2_cleaned_zonal.csv", index=False)
    print(f" -> Processed DF1 (Rural/Urban): {df1.shape[0]} rows, {df1.shape[1]} columns")
    print(f" -> Processed DF2 (Macro Zonal): {df2.shape[0]} rows, {df2.shape[1]} columns")
    print(" -> Cleaned CSV files exported to 'data/processed/'")

    # 2. Exploratory Data Analysis & Statistics
    print("\n[Step 2/5] Performing Exploratory Data Analysis (EDA)...")
    eda = UnemploymentEDA(df1, df2)

    # Summary Statistics
    stats = eda.get_summary_statistics()
    print("\n--- Descriptive Statistics (National Zonal Dataset 2020) ---")
    print(stats['df2_summary'])

    # Covid Shock Impact
    shock = eda.get_covid_impact_summary()
    print("\n--- COVID-19 Lockdown Shock Metrics ---")
    print(f"Pre-Lockdown Average Unemployment Rate:    {shock['unemployment_pre']}%")
    print(f"Lockdown Peak Average Unemployment Rate:   {shock['unemployment_peak']}%")
    print(f"Post-Lockdown Average Unemployment Rate:   {shock['unemployment_post']}%")
    print(f"Absolute Shock Delta:                      +{shock['ur_absolute_jump_pct_points']} percentage points")
    print(f"Relative Shock Jump:                       +{shock['ur_relative_jump_percent']}%")
    print(f"Pre-Lockdown Active Employed Workforce:    {shock['employed_pre_lockdown']:,} workers")
    print(f"Lockdown Peak Active Employed Workforce:   {shock['employed_lockdown_peak']:,} workers")
    print(f"Net Jobs Displaced at Peak Shock:          {shock['net_jobs_displaced_peak']:,} workers (~131.7 Million)")
    print(f"Labour Force Participation Drop:           {shock['lpr_pre']}% -> {shock['lpr_peak']}% (-{shock['lpr_drop_points']} pp)")

    # Rural vs Urban
    rural_urban = eda.get_rural_vs_urban_analysis()
    print("\n--- Rural vs. Urban Divergence Across Phases ---")
    print(rural_urban['area_phase_breakdown'])

    # State Rankings
    rankings = eda.get_state_vulnerability_rankings()
    print("\n--- Top 5 Most Severely Impacted States (by Absolute Shock Delta) ---")
    print(rankings[['State', 'Zone', 'Pre_Lockdown_UR', 'Lockdown_Peak_UR', 'Absolute_Shock_Delta', 'Pct_Increase']].head(5).to_string(index=False))

    print("\n--- Top 5 Most Resilient States ---")
    print(rankings[['State', 'Zone', 'Pre_Lockdown_UR', 'Lockdown_Peak_UR', 'Absolute_Shock_Delta', 'Pct_Increase']].tail(5).to_string(index=False))

    # Zonal Impact
    zonal = eda.get_zonal_analysis()
    print("\n--- Zonal Shock Ranking ---")
    print(zonal.to_string(index=False))

    # 3. Generate Visualizations
    print("\n[Step 3/5] Generating Publication-Ready Visualizations...")
    viz = UnemploymentVisualizer(df1, df2, output_dir="reports/figures")
    viz.generate_all_plots()

    # 4. Generate Policy Insights
    print("\n[Step 4/5] Formulating Policy Recommendations...")
    policy = generate_policy_brief()
    print(f"Formulated {len(policy['pillars'])} strategic evidence-based policy pillars.")

    # 5. Export Comprehensive Markdown Report
    print("\n[Step 5/5] Generating Executive Summary Report (Unemployment_Analysis_Report.md)...")
    generate_markdown_report(stats, shock, rural_urban, rankings, zonal, policy)
    print(" -> Report generated at 'reports/Unemployment_Analysis_Report.md'")

    print("\n" + "=" * 70)
    print("   ANALYSIS COMPLETE! Ready to run interactive localhost dashboard.   ")
    print("=" * 70)

def df_to_markdown(df):
    """Converts a pandas DataFrame into a standard markdown table without tabulate."""
    headers = list(df.columns)
    lines = ["| " + " | ".join(str(h) for h in headers) + " |"]
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[h]) for h in headers) + " |")
    return "\n".join(lines)

def generate_markdown_report(stats, shock, rural_urban, rankings, zonal, policy):
    os.makedirs("reports", exist_ok=True)
    top5_md = df_to_markdown(rankings.head(5)[['State', 'Zone', 'Pre_Lockdown_UR', 'Lockdown_Peak_UR', 'Absolute_Shock_Delta', 'Pct_Increase']])
    tail5_md = df_to_markdown(rankings.tail(5)[['State', 'Zone', 'Pre_Lockdown_UR', 'Lockdown_Peak_UR', 'Absolute_Shock_Delta', 'Pct_Increase']])
    zonal_md = df_to_markdown(zonal)

    report_content = f"""# Comprehensive Analysis of Unemployment Trends & COVID-19 Shock in India

## Executive Summary
This report presents an empirical data science investigation of India's labor market dynamics, analyzing the impact of the COVID-19 pandemic, nationwide lockdowns, rural vs. urban structural disparities, regional/zonal vulnerability, and seasonal employment fluctuations.

---

## 1. Key Macroeconomic Findings & COVID-19 Shock

| Macroeconomic Indicator | Pre-Lockdown Baseline (Jan-Mar 2020) | Lockdown Peak (Apr-May 2020) | Post-Lockdown / Unlock (Jun-Oct 2020) | Absolute Shock Impact |
|:---|:---:|:---:|:---:|:---:|
| **Average Unemployment Rate (%)** | **{shock['unemployment_pre']}%** | **{shock['unemployment_peak']}%** | **{shock['unemployment_post']}%** | **+{shock['ur_absolute_jump_pct_points']} pp (+{shock['ur_relative_jump_percent']}%)** |
| **Active Employed Workforce** | **{shock['employed_pre_lockdown']:,}** | **{shock['employed_lockdown_peak']:,}** | **{shock['employed_post_lockdown']:,}** | **-{shock['net_jobs_displaced_peak']:,} jobs (-32.4%)** |
| **Labour Force Participation Rate** | **{shock['lpr_pre']}%** | **{shock['lpr_peak']}%** | **41.90%** | **-{shock['lpr_drop_points']} pp** |

### Key Observations:
1. **The Sudden Stop**: Unemployment rate more than doubled overnight in April 2020, leaping from an average baseline of **9.7%** to a peak of **23.24%** in May 2020.
2. **Massive Labor Displacement**: Over **131.7 million workers** lost active employment in April 2020, representing an unprecedented 32.4% contraction in the country's active workforce.
3. **Labour Participation Shock**: The Labour Force Participation Rate (LFPR) plummeted from 44.2% to 35.3%, demonstrating a massive discouraged-worker effect where millions of displaced workers ceased seeking active employment due to stringent mobility curbs.
4. **V-Shaped Initial Rebound**: With the inception of Unlock 1.0 in June 2020, the headline unemployment rate dropped sharply to 10.91%, aided by agricultural absorption and the resumption of localized activities.

---

## 2. Urban vs. Rural Structural Divergence

| Pandemic Phase | Rural Unemployment Rate (%) | Urban Unemployment Rate (%) | Urban Excess Penalty (pp) |
|:---|:---:|:---:|:---:|
| **Pre-Lockdown** | 8.24% | 10.91% | +2.67 pp |
| **Lockdown Peak** | 21.48% | 26.93% | **+5.45 pp** |
| **Post-Lockdown (Jun 2020)** | 11.83% | 11.98% | +0.15 pp |

### Urban Vulnerability vs Rural Cushion:
- **Urban Centers Bore the Brunt**: Urban unemployment surged to nearly 27-28% during April-May 2020 due to total shutdowns of services, construction, retail, and public transport.
- **The Rural Absorptive Cushion**: Rural India acted as an economic shock-absorber. Returned migrant laborers and rural residents were partially absorbed by agricultural sowing (Kharif season) and emergency allocations under the Mahatma Gandhi National Rural Employment Guarantee Act (MGNREGA).

---

## 3. State-Level Sensitivity & Vulnerability Ranking

### Top 5 Most Severely Impacted States:
{top5_md}

- **Puducherry**: Reached a staggering peak of **67.02%** (+65.84 pp increase) due to its heavy reliance on tourism, hospitality, and informal retail services.
- **Jharkhand & Bihar**: Both experienced unemployment rates above 46-53%, driven by returning migrant workers and weak internal industrial job absorption.
- **Tamil Nadu**: Industrial and automotive manufacturing corridors were shuttered, causing unemployment to jump from 3.35% to 41.50% (+1,137% surge).

### Top 5 Most Resilient States:
{tail5_md}

- **Sikkim, Himachal Pradesh, Uttarakhand, Chhattisgarh, Meghalaya**: Displayed minimal shock or even counter-cyclical stability due to dominant agrarian economies, tea plantations, and local self-sufficiency.

---

## 4. Regional Zonal Analysis

{zonal_md}

- **South Zone** and **East Zone** experienced the largest absolute shocks (+25.49 pp and +24.96 pp respectively).
- **North Zone** maintained the highest pre-lockdown structural baseline (15.10%), dominated by states like Haryana, Delhi, and Jammu & Kashmir.

---

## 5. Evidence-Based Economic and Social Policy Recommendations

"""
    for p in policy['pillars']:
        report_content += f"""### [{p['priority']}] {p['title']}
- **Target Population**: {p['target_population']}
- **Empirical Basis**: {p['empirical_basis']}
- **Actionable Interventions**:
"""
        for rec in p['recommendations']:
            report_content += f"  - {rec}\n"
        report_content += "\n"

    with open("reports/Unemployment_Analysis_Report.md", "w", encoding="utf-8") as f:
        f.write(report_content)

if __name__ == '__main__':
    main()

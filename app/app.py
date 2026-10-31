"""
app.py
------
Flask Web Application & Interactive Localhost Dashboard
for India Unemployment Analysis & COVID-19 Shock Exploration.
"""

import os
import sys
import json
import pandas as pd
import numpy as np
from flask import Flask, render_template, jsonify, request, send_from_directory

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src.data_preprocessing import load_and_clean_datasets
from src.eda_analysis import UnemploymentEDA
from src.policy_insights import generate_policy_brief

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Load and prepare datasets in memory once on startup
print("Loading and preprocessing datasets for dashboard...")
df1, df2, geo = load_and_clean_datasets(
    df1_path=os.path.join(BASE_DIR, "Unemployment in India.csv"),
    df2_path=os.path.join(BASE_DIR, "Unemployment_Rate_upto_11_2020.csv")
)
eda = UnemploymentEDA(df1, df2)
policy_brief = generate_policy_brief()
print("Datasets loaded successfully!")

@app.route('/')
def index():
    """Serves the main interactive dashboard."""
    states = sorted(df2['State'].unique().tolist())
    zones = sorted(df2['Zone'].unique().tolist())
    return render_template('index.html', states=states, zones=zones)

@app.route('/api/kpi_metrics')
def api_kpi_metrics():
    """Returns high-level KPI cards metrics."""
    state_filter = request.args.get('state', 'All')
    zone_filter = request.args.get('zone', 'All')

    d = df2.copy()
    if zone_filter != 'All':
        d = d[d['Zone'] == zone_filter]
    if state_filter != 'All':
        d = d[d['State'] == state_filter]

    pre = d[d['Covid_Phase'] == 'Pre-Lockdown']
    peak = d[d['Covid_Phase'] == 'Lockdown Peak']
    post = d[d['Covid_Phase'] == 'Post-Lockdown / Unlock']

    pre_ur = round(float(pre['Unemployment_Rate'].mean()), 2) if len(pre) else 0.0
    peak_ur = round(float(peak['Unemployment_Rate'].mean()), 2) if len(peak) else 0.0
    post_ur = round(float(post['Unemployment_Rate'].mean()), 2) if len(post) else 0.0

    shock_delta = round(peak_ur - pre_ur, 2)
    shock_pct = round(((peak_ur - pre_ur) / pre_ur * 100), 2) if pre_ur > 0 else 0.0

    pre_emp = int(pre['Employed'].sum() / pre['Year_Month'].nunique()) if pre['Year_Month'].nunique() > 0 else 0
    peak_emp = int(peak['Employed'].sum() / peak['Year_Month'].nunique()) if peak['Year_Month'].nunique() > 0 else 0
    jobs_displaced = max(0, pre_emp - peak_emp)

    pre_lpr = round(float(pre['Labour_Participation_Rate'].mean()), 2) if len(pre) else 0.0
    peak_lpr = round(float(peak['Labour_Participation_Rate'].mean()), 2) if len(peak) else 0.0
    lpr_drop = round(pre_lpr - peak_lpr, 2)

    return jsonify({
        'pre_lockdown_ur': pre_ur,
        'peak_lockdown_ur': peak_ur,
        'post_lockdown_ur': post_ur,
        'shock_delta': shock_delta,
        'shock_pct': shock_pct,
        'pre_employed': pre_emp,
        'peak_employed': peak_emp,
        'jobs_displaced': jobs_displaced,
        'pre_lpr': pre_lpr,
        'peak_lpr': peak_lpr,
        'lpr_drop': lpr_drop,
        'total_records': len(d)
    })

@app.route('/api/monthly_trend')
def api_monthly_trend():
    """Returns monthly timeline of Unemployment Rate & Employed."""
    state_filter = request.args.get('state', 'All')
    zone_filter = request.args.get('zone', 'All')

    d = df2.copy()
    if zone_filter != 'All':
        d = d[d['Zone'] == zone_filter]
    if state_filter != 'All':
        d = d[d['State'] == state_filter]

    monthly = d.groupby('Year_Month').agg(
        UR=('Unemployment_Rate', 'mean'),
        LPR=('Labour_Participation_Rate', 'mean'),
        Employed=('Employed', 'sum')
    ).reset_index()

    monthly['UR'] = monthly['UR'].round(2)
    monthly['LPR'] = monthly['LPR'].round(2)
    monthly['Employed_M'] = (monthly['Employed'] / 1e6).round(2)

    return jsonify({
        'labels': monthly['Year_Month'].tolist(),
        'unemployment_rate': monthly['UR'].tolist(),
        'labour_participation': monthly['LPR'].tolist(),
        'employed_millions': monthly['Employed_M'].tolist()
    })

@app.route('/api/rural_urban_trend')
def api_rural_urban_trend():
    """Returns rural vs urban monthly unemployment rate comparison."""
    state_filter = request.args.get('state', 'All')
    d = df1.copy()
    if state_filter != 'All':
        d = d[d['State'] == state_filter]

    pivot = d.pivot_table(index='Year_Month', columns='Area', values='Unemployment_Rate', aggfunc='mean').round(2)
    labels = pivot.index.tolist()
    rural = pivot['Rural'].fillna(0).tolist() if 'Rural' in pivot else []
    urban = pivot['Urban'].fillna(0).tolist() if 'Urban' in pivot else []

    return jsonify({
        'labels': labels,
        'rural': rural,
        'urban': urban
    })

@app.route('/api/state_shock_rankings')
def api_state_shock_rankings():
    """Returns state rankings by shock delta."""
    zone_filter = request.args.get('zone', 'All')
    d = df2.copy()
    if zone_filter != 'All':
        d = d[d['Zone'] == zone_filter]

    pre = d[d['Covid_Phase'] == 'Pre-Lockdown'].groupby('State')['Unemployment_Rate'].mean()
    peak = d[d['Covid_Phase'] == 'Lockdown Peak'].groupby('State')['Unemployment_Rate'].mean()
    post = d[d['Covid_Phase'] == 'Post-Lockdown / Unlock'].groupby('State')['Unemployment_Rate'].mean()

    res = pd.DataFrame({'Pre': pre, 'Peak': peak, 'Post': post}).dropna()
    res['Delta'] = (res['Peak'] - res['Pre']).round(2)
    res['Pre'] = res['Pre'].round(2)
    res['Peak'] = res['Peak'].round(2)
    res['Post'] = res['Post'].round(2)
    res = res.sort_values(by='Delta', ascending=True)

    return jsonify({
        'states': res.index.tolist(),
        'pre': res['Pre'].tolist(),
        'peak': res['Peak'].tolist(),
        'post': res['Post'].tolist(),
        'delta': res['Delta'].tolist()
    })

@app.route('/api/zonal_comparison')
def api_zonal_comparison():
    """Returns comparison across 5 Indian Zones."""
    zonal_pivot = df2.pivot_table(
        index='Zone',
        columns='Covid_Phase',
        values='Unemployment_Rate',
        aggfunc='mean'
    )[['Pre-Lockdown', 'Lockdown Peak', 'Post-Lockdown / Unlock']].round(2)

    return jsonify({
        'zones': zonal_pivot.index.tolist(),
        'pre': zonal_pivot['Pre-Lockdown'].tolist(),
        'peak': zonal_pivot['Lockdown Peak'].tolist(),
        'post': zonal_pivot['Post-Lockdown / Unlock'].tolist()
    })

@app.route('/api/map_data')
def api_map_data():
    """Returns geospatial marker data for all Indian States."""
    states_data = []
    grouped = df2.groupby('State')
    for state_name, group in grouped:
        lat = float(group['Latitude'].iloc[0])
        lon = float(group['Longitude'].iloc[0])
        zone = str(group['Zone'].iloc[0])

        pre_val = group[group['Covid_Phase'] == 'Pre-Lockdown']['Unemployment_Rate'].mean()
        peak_val = group[group['Covid_Phase'] == 'Lockdown Peak']['Unemployment_Rate'].mean()
        post_val = group[group['Covid_Phase'] == 'Post-Lockdown / Unlock']['Unemployment_Rate'].mean()
        avg_employed = int(group['Employed'].mean())

        states_data.append({
            'state': state_name,
            'lat': lat,
            'lon': lon,
            'zone': zone,
            'pre_ur': round(float(pre_val), 2) if pd.notnull(pre_val) else 0.0,
            'peak_ur': round(float(peak_val), 2) if pd.notnull(peak_val) else 0.0,
            'post_ur': round(float(post_val), 2) if pd.notnull(post_val) else 0.0,
            'shock_delta': round(float(peak_val - pre_val), 2) if (pd.notnull(peak_val) and pd.notnull(pre_val)) else 0.0,
            'avg_employed': avg_employed
        })

    return jsonify(states_data)

@app.route('/api/policy_recommendations')
def api_policy():
    """Returns evidence-based policy recommendations."""
    return jsonify(policy_brief)

@app.route('/api/raw_data')
def api_raw_data():
    """Returns cleaned raw data records for table explorer."""
    state_filter = request.args.get('state', 'All')
    limit = int(request.args.get('limit', 100))

    d = df1.copy()
    if state_filter != 'All':
        d = d[d['State'] == state_filter]

    records = d[['State', 'Area', 'Date', 'Unemployment_Rate', 'Employed', 'Labour_Participation_Rate', 'Covid_Phase', 'Season']].head(limit).copy()
    records['Date'] = records['Date'].dt.strftime('%d-%m-%Y')
    return jsonify(records.to_dict(orient='records'))

@app.route('/static/reports/<path:filename>')
def serve_report_figures(filename):
    """Serves generated report figures."""
    return send_from_directory(os.path.join(BASE_DIR, 'reports', 'figures'), filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5005))
    print(f"Starting Unemployment Analysis Dashboard on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)

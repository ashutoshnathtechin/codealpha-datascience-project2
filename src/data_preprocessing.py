"""
data_preprocessing.py
---------------------
Data cleaning, validation, standardization, and feature engineering module
for India Unemployment Analysis (Task 2).
"""

import os
import pandas as pd
import numpy as np
from typing import Tuple, Dict

def load_and_clean_datasets(
    df1_path: str = "Unemployment in India.csv",
    df2_path: str = "Unemployment_Rate_upto_11_2020.csv"
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Loads raw datasets, handles whitespace, null values, standardizes column names,
    formats datetime, and builds an enriched merged dataset.
    
    Returns:
        df1_clean: Cleaned 'Unemployment in India' dataset (includes Area: Rural/Urban)
        df2_clean: Cleaned 'Unemployment_Rate_upto_11_2020' dataset (includes Zone, Lat/Lon)
        merged_df: Comprehensive integrated dataset with enriched features
    """
    # 1. Clean DF1 (Rural & Urban data: May 2019 - June 2020)
    df1 = pd.read_csv(df1_path)
    # Drop rows where all elements are NaN (e.g. trailing empty rows in raw CSV)
    df1_clean = df1.dropna(how='all').copy()
    # Strip whitespace from column names
    df1_clean.columns = df1_clean.columns.str.strip()
    # Standardize column names
    df1_clean.rename(columns={
        'Region': 'State',
        'Frequency': 'Frequency',
        'Estimated Unemployment Rate (%)': 'Unemployment_Rate',
        'Estimated Employed': 'Employed',
        'Estimated Labour Participation Rate (%)': 'Labour_Participation_Rate',
        'Area': 'Area'
    }, inplace=True)
    
    # Strip string fields
    df1_clean['State'] = df1_clean['State'].str.strip()
    df1_clean['Area'] = df1_clean['Area'].str.strip()
    df1_clean['Frequency'] = df1_clean['Frequency'].str.strip()
    df1_clean['Date'] = pd.to_datetime(df1_clean['Date'].str.strip(), format='%d-%m-%Y')
    
    # Feature engineering for DF1
    df1_clean['Year'] = df1_clean['Date'].dt.year
    df1_clean['Month'] = df1_clean['Date'].dt.month
    df1_clean['Month_Name'] = df1_clean['Date'].dt.strftime('%b')
    df1_clean['Year_Month'] = df1_clean['Date'].dt.strftime('%Y-%m')
    df1_clean['Covid_Phase'] = df1_clean['Date'].apply(categorize_covid_phase)
    df1_clean['Season'] = df1_clean['Month'].apply(get_season)

    # 2. Clean DF2 (Macro-zone and Lat/Long data: Jan 2020 - Oct 2020)
    df2 = pd.read_csv(df2_path)
    df2_clean = df2.dropna(how='all').copy()
    df2_clean.columns = df2_clean.columns.str.strip()
    
    # Clean column names
    col_names = []
    for c in df2_clean.columns:
        c_clean = c.strip()
        if c_clean == 'Region.1':
            col_names.append('Zone')
        elif c_clean == 'Region':
            col_names.append('State')
        elif 'unemployment' in c_clean.lower():
            col_names.append('Unemployment_Rate')
        elif 'employed' in c_clean.lower():
            col_names.append('Employed')
        elif 'labour' in c_clean.lower() or 'labor' in c_clean.lower():
            col_names.append('Labour_Participation_Rate')
        elif 'longitude' in c_clean.lower():
            # Note: In the raw CSV dataset, the 'longitude' column contains Latitude values (~15 to ~34)
            col_names.append('Latitude')
        elif 'latitude' in c_clean.lower():
            # And 'latitude' column contains Longitude values (~72 to ~94)
            col_names.append('Longitude')
        else:
            col_names.append(c_clean)
    df2_clean.columns = col_names

    df2_clean['State'] = df2_clean['State'].str.strip()
    df2_clean['Zone'] = df2_clean['Zone'].str.strip()
    df2_clean['Date'] = pd.to_datetime(df2_clean['Date'].str.strip(), format='%d-%m-%Y')
    
    # Feature engineering for DF2
    df2_clean['Year'] = df2_clean['Date'].dt.year
    df2_clean['Month'] = df2_clean['Date'].dt.month
    df2_clean['Month_Name'] = df2_clean['Date'].dt.strftime('%b')
    df2_clean['Year_Month'] = df2_clean['Date'].dt.strftime('%Y-%m')
    df2_clean['Covid_Phase'] = df2_clean['Date'].apply(categorize_covid_phase)
    df2_clean['Season'] = df2_clean['Month'].apply(get_season)

    # 3. Build Geolocation and Zone Lookup from DF2
    geo_lookup = df2_clean[['State', 'Zone', 'Latitude', 'Longitude']].drop_duplicates().set_index('State')
    # Chandigarh is present in DF1 but not DF2; assign North zone and approximate coords
    if 'Chandigarh' not in geo_lookup.index:
        geo_lookup.loc['Chandigarh'] = ['North', 30.7333, 76.7794]
    
    # Enrich DF1 with Zone and Geo coordinates
    df1_clean['Zone'] = df1_clean['State'].map(geo_lookup['Zone'])
    df1_clean['Latitude'] = df1_clean['State'].map(geo_lookup['Latitude'])
    df1_clean['Longitude'] = df1_clean['State'].map(geo_lookup['Longitude'])

    return df1_clean, df2_clean, geo_lookup

def categorize_covid_phase(date_val: pd.Timestamp) -> str:
    """
    Categorizes the timeline into three distinct macroeconomic periods:
    1. Pre-Lockdown: Before April 2020 (Normal economic operations)
    2. Lockdown Peak: April - May 2020 (Nationwide strict lockdowns, peak displacement)
    3. Post-Lockdown / Unlock: June 2020 onwards (Gradual phased unlocking)
    """
    if date_val < pd.Timestamp('2020-04-01'):
        return 'Pre-Lockdown'
    elif date_val <= pd.Timestamp('2020-05-31'):
        return 'Lockdown Peak'
    else:
        return 'Post-Lockdown / Unlock'

def get_season(month: int) -> str:
    """
    Maps month number to Indian macroeconomic agricultural season:
    - Winter (Dec - Feb): Rabi crop development
    - Summer / Pre-Monsoon (Mar - May): Rabi harvest, peak summer
    - Monsoon (Jun - Sep): Kharif sowing season
    - Post-Monsoon / Autumn (Oct - Nov): Kharif harvest
    """
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Summer'
    elif month in [6, 7, 8, 9]:
        return 'Monsoon'
    else:
        return 'Post-Monsoon'

if __name__ == '__main__':
    df1, df2, geo = load_and_clean_datasets()
    print(f"DF1 Cleaned: {df1.shape} records, {df1['State'].nunique()} States/UTs")
    print(f"DF2 Cleaned: {df2.shape} records, {df2['State'].nunique()} States/UTs")
    print("Geolocation lookup built for", len(geo), "regions.")

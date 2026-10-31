"""
eda_analysis.py
---------------
Exploratory Data Analysis (EDA) module for India Unemployment Rate dataset.
Provides statistical aggregations, Covid-19 impact metrics, rural/urban
divergence calculations, regional rankings, and seasonal analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any

class UnemploymentEDA:
    def __init__(self, df1: pd.DataFrame, df2: pd.DataFrame):
        self.df1 = df1.copy()  # Rural & Urban (May 2019 - Jun 2020)
        self.df2 = df2.copy()  # Macro Zonal (Jan 2020 - Oct 2020)

    def get_summary_statistics(self) -> Dict[str, pd.DataFrame]:
        """Calculates descriptive statistics for key macroeconomic indicators."""
        cols = ['Unemployment_Rate', 'Employed', 'Labour_Participation_Rate']
        return {
            'df1_summary': self.df1[cols].describe().round(2),
            'df2_summary': self.df2[cols].describe().round(2)
        }

    def get_national_monthly_trends(self) -> pd.DataFrame:
        """
        Computes monthly national aggregates for DF2 (Jan 2020 - Oct 2020),
        capturing the full trajectory of the pandemic.
        """
        monthly = self.df2.groupby('Year_Month').agg(
            Avg_Unemployment_Rate=('Unemployment_Rate', 'mean'),
            Median_Unemployment_Rate=('Unemployment_Rate', 'median'),
            Total_Employed=('Employed', 'sum'),
            Avg_Labour_Participation=('Labour_Participation_Rate', 'mean'),
            Record_Count=('State', 'count')
        ).reset_index()
        monthly['Avg_Unemployment_Rate'] = monthly['Avg_Unemployment_Rate'].round(2)
        monthly['Avg_Labour_Participation'] = monthly['Avg_Labour_Participation'].round(2)
        return monthly

    def get_covid_impact_summary(self) -> Dict[str, Any]:
        """
        Quantifies the macroeconomic shock across Pre-Lockdown, Lockdown Peak,
        and Post-Lockdown phases.
        """
        phase_stats = self.df2.groupby('Covid_Phase').agg(
            Mean_Unemployment=('Unemployment_Rate', 'mean'),
            Median_Unemployment=('Unemployment_Rate', 'median'),
            Std_Unemployment=('Unemployment_Rate', 'std'),
            Avg_Employed_Per_State=('Employed', 'mean'),
            Total_Employed_Monthly_Avg=('Employed', lambda s: s.sum() / self.df2.loc[s.index, 'Year_Month'].nunique()),
            Avg_Labour_Participation=('Labour_Participation_Rate', 'mean')
        ).loc[['Pre-Lockdown', 'Lockdown Peak', 'Post-Lockdown / Unlock']]

        pre_ur = phase_stats.loc['Pre-Lockdown', 'Mean_Unemployment']
        peak_ur = phase_stats.loc['Lockdown Peak', 'Mean_Unemployment']
        post_ur = phase_stats.loc['Post-Lockdown / Unlock', 'Mean_Unemployment']

        pre_emp = phase_stats.loc['Pre-Lockdown', 'Total_Employed_Monthly_Avg']
        peak_emp = phase_stats.loc['Lockdown Peak', 'Total_Employed_Monthly_Avg']
        post_emp = phase_stats.loc['Post-Lockdown / Unlock', 'Total_Employed_Monthly_Avg']

        pre_lpr = phase_stats.loc['Pre-Lockdown', 'Avg_Labour_Participation']
        peak_lpr = phase_stats.loc['Lockdown Peak', 'Avg_Labour_Participation']

        shock_metrics = {
            'phase_stats': phase_stats.round(2),
            'unemployment_pre': round(pre_ur, 2),
            'unemployment_peak': round(peak_ur, 2),
            'unemployment_post': round(post_ur, 2),
            'ur_absolute_jump_pct_points': round(peak_ur - pre_ur, 2),
            'ur_relative_jump_percent': round(((peak_ur - pre_ur) / pre_ur) * 100, 2),
            'employed_pre_lockdown': int(pre_emp),
            'employed_lockdown_peak': int(peak_emp),
            'employed_post_lockdown': int(post_emp),
            'net_jobs_displaced_peak': int(pre_emp - peak_emp),
            'lpr_pre': round(pre_lpr, 2),
            'lpr_peak': round(peak_lpr, 2),
            'lpr_drop_points': round(pre_lpr - peak_lpr, 2)
        }
        return shock_metrics

    def get_rural_vs_urban_analysis(self) -> Dict[str, Any]:
        """
        Analyzes the urban-rural divergence using DF1 (May 2019 - Jun 2020).
        """
        area_phase = self.df1.groupby(['Covid_Phase', 'Area']).agg(
            Avg_Unemployment_Rate=('Unemployment_Rate', 'mean'),
            Total_Employed_Monthly_Avg=('Employed', lambda s: s.sum() / self.df1.loc[s.index, 'Year_Month'].nunique()),
            Avg_Labour_Participation=('Labour_Participation_Rate', 'mean')
        ).round(2).reset_index()

        monthly_area = self.df1.pivot_table(
            index='Year_Month',
            columns='Area',
            values='Unemployment_Rate',
            aggfunc='mean'
        ).round(2).reset_index()

        monthly_employed = self.df1.pivot_table(
            index='Year_Month',
            columns='Area',
            values='Employed',
            aggfunc='sum'
        ).reset_index()

        return {
            'area_phase_breakdown': area_phase,
            'monthly_unemployment_by_area': monthly_area,
            'monthly_employed_by_area': monthly_employed
        }

    def get_state_vulnerability_rankings(self) -> pd.DataFrame:
        """
        Computes state-level sensitivity to the lockdown shock:
        Baseline vs Peak vs Unlock, Absolute Delta, and Resilience Category.
        """
        pre = self.df2[self.df2['Covid_Phase'] == 'Pre-Lockdown'].groupby('State')['Unemployment_Rate'].mean()
        peak = self.df2[self.df2['Covid_Phase'] == 'Lockdown Peak'].groupby('State')['Unemployment_Rate'].mean()
        post = self.df2[self.df2['Covid_Phase'] == 'Post-Lockdown / Unlock'].groupby('State')['Unemployment_Rate'].mean()
        zone = self.df2.groupby('State')['Zone'].first()

        state_df = pd.DataFrame({
            'Zone': zone,
            'Pre_Lockdown_UR': pre,
            'Lockdown_Peak_UR': peak,
            'Post_Lockdown_UR': post
        })

        state_df['Absolute_Shock_Delta'] = (state_df['Lockdown_Peak_UR'] - state_df['Pre_Lockdown_UR']).round(2)
        state_df['Pct_Increase'] = (((state_df['Lockdown_Peak_UR'] - state_df['Pre_Lockdown_UR']) / state_df['Pre_Lockdown_UR']) * 100).round(2)
        state_df['Recovery_Delta'] = (state_df['Post_Lockdown_UR'] - state_df['Pre_Lockdown_UR']).round(2)

        def assign_category(row):
            if row['Absolute_Shock_Delta'] >= 20:
                return 'Severely Impacted (Crisis)'
            elif row['Absolute_Shock_Delta'] >= 10:
                return 'Moderately Impacted'
            elif row['Absolute_Shock_Delta'] > 0:
                return 'Mildly Impacted'
            else:
                return 'Resilient / Inverted'

        state_df['Vulnerability_Category'] = state_df.apply(assign_category, axis=1)
        state_df = state_df.sort_values(by='Absolute_Shock_Delta', ascending=False)
        return state_df.round(2).reset_index()

    def get_zonal_analysis(self) -> pd.DataFrame:
        """
        Evaluates regional macroeconomic resilience across Indian Zones
        (South, East, West, North, Northeast).
        """
        zonal = self.df2.groupby(['Zone', 'Covid_Phase']).agg(
            Avg_Unemployment_Rate=('Unemployment_Rate', 'mean'),
            Avg_Employed=('Employed', 'mean'),
            Avg_Labour_Participation=('Labour_Participation_Rate', 'mean')
        ).round(2).reset_index()

        zonal_pivot = self.df2.pivot_table(
            index='Zone',
            columns='Covid_Phase',
            values='Unemployment_Rate',
            aggfunc='mean'
        )[['Pre-Lockdown', 'Lockdown Peak', 'Post-Lockdown / Unlock']]

        zonal_pivot['Shock_Delta'] = (zonal_pivot['Lockdown Peak'] - zonal_pivot['Pre-Lockdown']).round(2)
        zonal_pivot['Pct_Surge'] = (((zonal_pivot['Lockdown Peak'] - zonal_pivot['Pre-Lockdown']) / zonal_pivot['Pre-Lockdown']) * 100).round(2)
        zonal_pivot = zonal_pivot.sort_values(by='Shock_Delta', ascending=False)
        return zonal_pivot.round(2).reset_index()

    def get_seasonal_patterns(self) -> pd.DataFrame:
        """Examines seasonal shifts across agricultural and non-agricultural quarters."""
        season_stats = self.df1.groupby(['Season', 'Area']).agg(
            Mean_Unemployment_Rate=('Unemployment_Rate', 'mean'),
            Median_Unemployment_Rate=('Unemployment_Rate', 'median'),
            Mean_Labour_Participation=('Labour_Participation_Rate', 'mean')
        ).round(2).reset_index()
        return season_stats

    def get_correlations(self) -> pd.DataFrame:
        """Computes correlation coefficients between numeric indicators."""
        cols = ['Unemployment_Rate', 'Employed', 'Labour_Participation_Rate']
        return self.df2[cols].corr().round(4)

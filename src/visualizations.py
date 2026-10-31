"""
visualizations.py
-----------------
Publication-quality plotting module for Unemployment Analysis.
Generates and saves visual figures to reports/figures/.
"""

import os
import matplotlib
matplotlib.use('Agg')  # Headless backend for server and script runs
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Configure global aesthetic styling
sns.set(style="whitegrid", palette="muted")
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['figure.titlesize'] = 14
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['figure.autolayout'] = True

class UnemploymentVisualizer:
    def __init__(self, df1: pd.DataFrame, df2: pd.DataFrame, output_dir: str = "reports/figures"):
        self.df1 = df1
        self.df2 = df2
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_all_plots(self):
        """Executes full suite of figure generations."""
        print("Generating Figure 1: National Unemployment & Employment Trajectory...")
        self.plot_national_trend()

        print("Generating Figure 2: Covid-19 Lockdown Shock Phase Comparison...")
        self.plot_covid_shock_phases()

        print("Generating Figure 3: Urban vs Rural Divergence...")
        self.plot_rural_vs_urban()

        print("Generating Figure 4: State-Level Lockdown Shock Ranking...")
        self.plot_state_shock_ranking()

        print("Generating Figure 5: Macro-Zonal Impact...")
        self.plot_zonal_impact()

        print("Generating Figure 6: Indicator Correlation Heatmap...")
        self.plot_correlation_heatmap()

        print("Generating Figure 7: Labour Participation Rate Plunge...")
        self.plot_labour_participation_trend()

        print("Generating Figure 8: Unemployment Distribution Boxplots...")
        self.plot_distribution_boxplots()

        print("Generating Figure 9: Seasonal Patterns...")
        self.plot_seasonal_trends()

        print(f"All figures successfully generated in '{self.output_dir}/'")

    def plot_national_trend(self):
        """Plot national monthly unemployment rate vs employed count."""
        monthly = self.df2.groupby('Year_Month').agg(
            UR=('Unemployment_Rate', 'mean'),
            EE=('Employed', lambda s: s.sum() / 1e6)  # Millions
        ).reset_index()

        fig, ax1 = plt.subplots(figsize=(11, 6), dpi=300)

        # Unemployment Rate on Left Axis
        color1 = '#e63946'
        ax1.set_xlabel('Timeline (Year-Month)', fontweight='bold', labelpad=10)
        ax1.set_ylabel('Avg Unemployment Rate (%)', color=color1, fontweight='bold')
        line1 = ax1.plot(monthly['Year_Month'], monthly['UR'], color=color1, marker='o', linewidth=2.5, label='Unemployment Rate (%)')
        ax1.tick_params(axis='y', labelcolor=color1)
        ax1.set_ylim(0, 28)

        # Shading Lockdown Peak
        ax1.axvspan('2020-04', '2020-05', color='#f1faee', alpha=0.9, hatch='//', label='Strict Nationwide Lockdown')

        # Annotate peak
        peak_idx = monthly['UR'].idxmax()
        peak_val = monthly.loc[peak_idx, 'UR']
        peak_date = monthly.loc[peak_idx, 'Year_Month']
        ax1.annotate(f'Lockdown Peak\n{peak_val:.1f}%',
                     xy=(peak_idx, peak_val),
                     xytext=(peak_idx - 0.5, peak_val + 2),
                     arrowprops=dict(facecolor='#d90429', arrowstyle='->', lw=1.5),
                     fontweight='bold', color='#9b2226')

        # Employed Count on Right Axis
        ax2 = ax1.twinx()
        color2 = '#1d3557'
        ax2.set_ylabel('Total Employed Workforce (Millions)', color=color2, fontweight='bold')
        line2 = ax2.plot(monthly['Year_Month'], monthly['EE'], color=color2, marker='s', linestyle='--', linewidth=2.2, label='Employed (Millions)')
        ax2.tick_params(axis='y', labelcolor=color2)
        ax2.set_ylim(250, 430)

        plt.title('India National Unemployment Rate & Active Workforce (Jan 2020 - Oct 2020)', fontsize=13, fontweight='bold', pad=15)
        
        # Combined Legend
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper right', framealpha=0.9)

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "01_national_unemployment_trend.png"), dpi=300)
        plt.close()

    def plot_covid_shock_phases(self):
        """Bar comparison of Pre-Lockdown, Lockdown Peak, and Post-Lockdown phases."""
        phase_order = ['Pre-Lockdown', 'Lockdown Peak', 'Post-Lockdown / Unlock']
        stats = self.df2.groupby('Covid_Phase')[['Unemployment_Rate', 'Labour_Participation_Rate']].mean().reindex(phase_order).reset_index()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

        colors_ur = ['#457b9d', '#e63946', '#2a9d8f']
        bars1 = ax1.bar(stats['Covid_Phase'], stats['Unemployment_Rate'], color=colors_ur, width=0.55, edgecolor='black', linewidth=0.8)
        ax1.set_ylabel('Average Unemployment Rate (%)', fontweight='bold')
        ax1.set_title('Unemployment Rate Shock Across Pandemic Phases', fontweight='bold')
        ax1.set_ylim(0, 30)
        for bar in bars1:
            h = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., h + 0.7, f'{h:.2f}%', ha='center', va='bottom', fontweight='bold')

        colors_lpr = ['#457b9d', '#e76f51', '#2a9d8f']
        bars2 = ax2.bar(stats['Covid_Phase'], stats['Labour_Participation_Rate'], color=colors_lpr, width=0.55, edgecolor='black', linewidth=0.8)
        ax2.set_ylabel('Labour Force Participation Rate (%)', fontweight='bold')
        ax2.set_title('Labour Force Participation Contraction', fontweight='bold')
        ax2.set_ylim(0, 55)
        for bar in bars2:
            h = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., h + 0.8, f'{h:.2f}%', ha='center', va='bottom', fontweight='bold')

        plt.suptitle('Macroeconomic Impact of COVID-19 Lockdown in India', fontsize=14, fontweight='bold', y=1.03)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "02_covid_lockdown_shock_comparison.png"), dpi=300)
        plt.close()

    def plot_rural_vs_urban(self):
        """Dual area line chart for rural vs urban divergence."""
        monthly_area = self.df1.pivot_table(index='Year_Month', columns='Area', values='Unemployment_Rate', aggfunc='mean')

        fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
        ax.plot(monthly_area.index, monthly_area['Urban'], marker='o', color='#d62828', linewidth=2.5, label='Urban Unemployment Rate')
        ax.plot(monthly_area.index, monthly_area['Rural'], marker='^', color='#2a9d8f', linewidth=2.5, label='Rural Unemployment Rate')

        ax.fill_between(monthly_area.index, monthly_area['Rural'], monthly_area['Urban'], where=(monthly_area['Urban'] >= monthly_area['Rural']),
                        color='#e76f51', alpha=0.18, label='Urban Excess Penalty')

        ax.set_title('Urban vs. Rural Unemployment Rate Divergence (May 2019 - Jun 2020)', fontsize=13, fontweight='bold', pad=15)
        ax.set_xlabel('Timeline (Year-Month)', fontweight='bold')
        ax.set_ylabel('Estimated Unemployment Rate (%)', fontweight='bold')
        plt.xticks(rotation=45)
        ax.legend(frameon=True, facecolor='white', framealpha=0.9)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "03_rural_vs_urban_unemployment.png"), dpi=300)
        plt.close()

    def plot_state_shock_ranking(self):
        """Horizontal bar ranking of states by Lockdown absolute shock delta."""
        pre = self.df2[self.df2['Covid_Phase'] == 'Pre-Lockdown'].groupby('State')['Unemployment_Rate'].mean()
        peak = self.df2[self.df2['Covid_Phase'] == 'Lockdown Peak'].groupby('State')['Unemployment_Rate'].mean()
        delta = (peak - pre).sort_values(ascending=True)

        fig, ax = plt.subplots(figsize=(10, 11), dpi=300)
        colors = ['#2a9d8f' if x < 5 else ('#e76f51' if x < 20 else '#d62828') for x in delta.values]
        bars = ax.barh(delta.index, delta.values, color=colors, edgecolor='black', linewidth=0.5, height=0.65)

        ax.set_xlabel('Lockdown Unemployment Rate Spike (Percentage Points Delta)', fontweight='bold')
        ax.set_ylabel('State / Union Territory', fontweight='bold')
        ax.set_title('Lockdown Shock by State: Absolute Spike in Unemployment Rate (%)', fontsize=13, fontweight='bold', pad=15)

        for bar in bars:
            w = bar.get_width()
            if w >= 0:
                ax.text(w + 0.8, bar.get_y() + bar.get_height()/2., f"+{w:.1f}%", va='center', ha='left', fontsize=8.5, fontweight='bold')
            else:
                ax.text(w - 0.8, bar.get_y() + bar.get_height()/2., f"{w:.1f}%", va='center', ha='right', fontsize=8.5, fontweight='bold')

        ax.set_xlim(-15, 75)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "04_state_level_lockdown_shock.png"), dpi=300)
        plt.close()

    def plot_zonal_impact(self):
        """Grouped bar chart for 5 Macro Zones across pandemic phases."""
        zonal = self.df2.pivot_table(index='Zone', columns='Covid_Phase', values='Unemployment_Rate', aggfunc='mean')
        zonal = zonal[['Pre-Lockdown', 'Lockdown Peak', 'Post-Lockdown / Unlock']]
        zonal = zonal.sort_values(by='Lockdown Peak', ascending=False)

        ax = zonal.plot(kind='bar', figsize=(10, 6), color=['#457b9d', '#e63946', '#2a9d8f'], edgecolor='black', linewidth=0.7, width=0.75, rot=0)
        plt.title('Macro-Zonal Unemployment Comparison Across Phases', fontsize=13, fontweight='bold', pad=15)
        plt.xlabel('Geographical Zone', fontweight='bold')
        plt.ylabel('Average Unemployment Rate (%)', fontweight='bold')
        plt.legend(title='Pandemic Phase', frameon=True)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "05_zonal_regional_impact.png"), dpi=300)
        plt.close()

    def plot_correlation_heatmap(self):
        """Correlation heatmap for core macroeconomic metrics."""
        cols = ['Unemployment_Rate', 'Employed', 'Labour_Participation_Rate']
        corr = self.df2[cols].corr()
        labels = ['Unemployment Rate (%)', 'Employed Count', 'Labour Participation (%)']

        fig, ax = plt.subplots(figsize=(7, 6), dpi=300)
        sns.heatmap(corr, annot=True, fmt=".3f", cmap='coolwarm', cbar=True,
                    xticklabels=labels, yticklabels=labels, vmin=-1, vmax=1,
                    linewidths=1, linecolor='white', square=True, ax=ax)
        plt.title('Pearson Correlation Between Macroeconomic Indicators', fontsize=12, fontweight='bold', pad=12)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "06_correlation_heatmap.png"), dpi=300)
        plt.close()

    def plot_labour_participation_trend(self):
        """Monthly Labour Participation Rate trajectory."""
        lpr_trend = self.df2.groupby('Year_Month')['Labour_Participation_Rate'].mean().reset_index()

        fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
        ax.plot(lpr_trend['Year_Month'], lpr_trend['Labour_Participation_Rate'], marker='o', color='#3a86ff', linewidth=2.5)
        ax.fill_between(lpr_trend['Year_Month'], lpr_trend['Labour_Participation_Rate'], color='#3a86ff', alpha=0.15)
        ax.set_ylim(30, 50)
        ax.set_title('National Average Labour Participation Rate Trajectory (2020)', fontsize=13, fontweight='bold', pad=15)
        ax.set_xlabel('Timeline (Year-Month)', fontweight='bold')
        ax.set_ylabel('Labour Force Participation Rate (%)', fontweight='bold')

        # Annotate lowest point
        min_idx = lpr_trend['Labour_Participation_Rate'].idxmin()
        min_val = lpr_trend.loc[min_idx, 'Labour_Participation_Rate']
        ax.annotate(f'Lockdown Trough\n{min_val:.1f}%',
                    xy=(min_idx, min_val),
                    xytext=(min_idx, min_val - 4),
                    arrowprops=dict(facecolor='#d90429', arrowstyle='->', lw=1.5),
                    fontweight='bold', color='#9b2226', ha='center')

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "07_labour_participation_drop.png"), dpi=300)
        plt.close()

    def plot_distribution_boxplots(self):
        """Distribution boxplots across phases and area."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

        sns.boxplot(data=self.df2, x='Covid_Phase', y='Unemployment_Rate', palette=['#457b9d', '#e63946', '#2a9d8f'], ax=ax1, width=0.5)
        ax1.set_title('Unemployment Rate Dispersion by Phase', fontweight='bold')
        ax1.set_xlabel('Phase', fontweight='bold')
        ax1.set_ylabel('Unemployment Rate (%)', fontweight='bold')

        sns.boxplot(data=self.df1, x='Area', y='Unemployment_Rate', palette=['#2a9d8f', '#e76f51'], ax=ax2, width=0.45)
        ax2.set_title('Unemployment Rate Dispersion by Area (Rural vs Urban)', fontweight='bold')
        ax2.set_xlabel('Area', fontweight='bold')
        ax2.set_ylabel('Unemployment Rate (%)', fontweight='bold')

        plt.suptitle('Distributional Characteristics & Volatility Spread', fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "08_unemployment_distribution_boxplots.png"), dpi=300)
        plt.close()

    def plot_seasonal_trends(self):
        """Seasonal patterns across Agricultural Cycles."""
        season_df = self.df1.groupby(['Season', 'Area'])['Unemployment_Rate'].mean().unstack()
        order = ['Winter', 'Summer', 'Monsoon', 'Post-Monsoon']
        season_df = season_df.reindex(order)

        fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
        season_df.plot(kind='bar', ax=ax, color=['#2a9d8f', '#e76f51'], edgecolor='black', linewidth=0.7, width=0.6, rot=0)
        ax.set_title('Seasonal Unemployment Rate by Sector (Rural vs Urban)', fontsize=13, fontweight='bold', pad=15)
        ax.set_xlabel('Agricultural / Macro Season', fontweight='bold')
        ax.set_ylabel('Mean Unemployment Rate (%)', fontweight='bold')
        ax.legend(title='Area', frameon=True)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "09_seasonal_monthly_patterns.png"), dpi=300)
        plt.close()

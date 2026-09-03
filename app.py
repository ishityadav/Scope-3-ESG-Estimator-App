import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import config
from estimator import Scope3Model

# --- 1. Page Configuration ---
st.set_page_config(page_title="Scope 3 Estimator", page_icon="🌱", layout="wide")

st.title("🌱 Corporate Scope 3 Carbon Estimator")
st.markdown("An interactive spend-based emissions benchmarking tool aligned with the GHG Protocol.")

# --- 2. Sidebar Controls ---
st.sidebar.header("Configuration Panel")
st.sidebar.markdown("Adjust macroeconomic assumptions to see real-time impacts on estimated emissions.")

# Interactive sliders for macro assumptions
custom_gbp_rate = st.sidebar.slider("GBP to INR Exchange Rate", min_value=90.0, max_value=120.0, value=config.GBP_TO_INR, step=0.5)
st.sidebar.markdown(f"*Historical FY24 Average: ₹105.00*")

# Allow users to filter which companies to display
st.sidebar.markdown("---")
st.sidebar.header("Filter Data")
selected_companies = st.sidebar.multiselect(
    "Select Companies to Benchmark",
    ["ITC Limited", "HUL", "Britannia"],
    default=["ITC Limited", "HUL", "Britannia"]
)

# --- 3. Data Processing ---
@st.cache_data # Caches the data so it doesn't reload on every slider tweak
def load_and_process_data(gbp_rate):
    # Temporarily override the config rate for the simulation
    original_rate = config.GBP_TO_INR
    config.GBP_TO_INR = gbp_rate 
    
    model = Scope3Model().execute_pipeline()
    master_df = model.master_df
    benchmark = model.fetch_corporate_benchmark()
    
    # Restore original config just in case
    config.GBP_TO_INR = original_rate
    return master_df, benchmark

# Run the model with the slider's value
master_df, benchmark = load_and_process_data(custom_gbp_rate)

# Filter the dataframes based on user selection
filtered_benchmark = benchmark[benchmark['Company'].isin(selected_companies)]
filtered_master = master_df[master_df['Company'].isin(selected_companies)]


# --- 4. Dashboard Layout ---

# Top Row: High-Level Metrics
st.header("Executive Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Estimated Scope 3 (tCO2e)", value=f"{filtered_benchmark['Emissions_tCO2e'].sum():,.0f}")
with col2:
    avg_intensity = filtered_benchmark['Carbon_Intensity (tCO2e/Cr_Rev)'].mean()
    st.metric(label="Average Carbon Intensity", value=f"{avg_intensity:.2f}")
with col3:
    st.metric(label="Companies Analyzed", value=len(filtered_benchmark))

st.markdown("---")
st.header("Interactive Visualizations")

# Create a 2x2 grid layout using columns
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

# --- CHART 1: Scale vs Efficiency ---
with row1_col1:
    st.subheader("1. Scale vs Carbon Efficiency")
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    x = np.arange(len(filtered_benchmark['Company']))
    width = 0.4

    ax1.bar(x, filtered_benchmark['Emissions_tCO2e'] / 1e6, width, color='#2c3e50', label='Emissions')
    ax1.set_ylabel('Emissions (Million tCO2e)', color='#2c3e50')
    ax1.set_xticks(x)
    ax1.set_xticklabels(filtered_benchmark['Company'])

    ax2 = ax1.twinx()
    ax2.plot(x, filtered_benchmark['Carbon_Intensity (tCO2e/Cr_Rev)'], color='#e74c3c', marker='o', linewidth=3)
    ax2.set_ylabel('Intensity (tCO2e / ₹1 Cr Revenue)', color='#e74c3c')
    ax2.grid(False)
    st.pyplot(fig1)

# --- CHART 2: Category Breakdown ---
with row1_col2:
    st.subheader("2. Scope 3 Category Breakdown")
    if not filtered_master.empty:
        fig2, ax2_chart = plt.subplots(figsize=(8, 5))
        pivot_cat = filtered_master.pivot_table(
            index='Company', columns='GHG_Scope3_Category', values='Emissions_tCO2e', aggfunc='sum'
        ).fillna(0) / 1e3 
        
        pivot_cat.plot(kind='bar', stacked=True, ax=ax2_chart, colormap='Spectral', edgecolor='black')
        ax2_chart.set_ylabel('Emissions (Thousand tCO2e)')
        ax2_chart.set_xlabel('')
        plt.xticks(rotation=0)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        st.pyplot(fig2)

# --- CHART 3: Donut Chart (Footprint Share) ---
with row2_col1:
    st.subheader("3. Overall Footprint Share (%)")
    if not filtered_master.empty:
        fig3, ax3 = plt.subplots(figsize=(8, 5))
        agg_data = filtered_master.groupby('GHG_Scope3_Category')['Emissions_tCO2e'].sum()
        colors = sns.color_palette('pastel')[0:len(agg_data)]
        
        wedges, texts, autotexts = ax3.pie(
            agg_data, labels=None, autopct='%1.1f%%', pctdistance=0.75, colors=colors, startangle=140
        )
        centre_circle = plt.Circle((0, 0), 0.55, fc='white')
        ax3.add_artist(centre_circle)
        ax3.legend(wedges, agg_data.index, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=8)
        st.pyplot(fig3)

# --- CHART 4: Pareto Analysis (Spend vs Carbon) ---
with row2_col2:
    st.subheader("4. Spend vs Carbon Impact")
    if not filtered_master.empty:
        fig4, ax4 = plt.subplots(figsize=(8, 5))
        spend_vs_emit = filtered_master.groupby('Expense_Item')[['Spend_INR_Crores', 'Emissions_tCO2e']].sum().reset_index()
        spend_vs_emit['% Spend'] = (spend_vs_emit['Spend_INR_Crores'] / spend_vs_emit['Spend_INR_Crores'].sum()) * 100
        spend_vs_emit['% Emissions'] = (spend_vs_emit['Emissions_tCO2e'] / spend_vs_emit['Emissions_tCO2e'].sum()) * 100
        spend_vs_emit = spend_vs_emit.sort_values(by='% Emissions', ascending=False)

        y_pos = np.arange(len(spend_vs_emit))
        bar_h = 0.35

        ax4.barh(y_pos - bar_h/2, spend_vs_emit['% Spend'], bar_h, label='% Spend', color='#3498db')
        ax4.barh(y_pos + bar_h/2, spend_vs_emit['% Emissions'], bar_h, label='% Carbon', color='#e67e22')
        ax4.set_yticks(y_pos)
        ax4.set_yticklabels(spend_vs_emit['Expense_Item'], fontsize=8)
        ax4.set_xlabel('Share of Total (%)')
        ax4.legend(loc='lower right', fontsize=8)
        st.pyplot(fig4)

# --- 5. Data Table Viewer ---
st.markdown("---")
st.header("Raw Data Audit")
with st.expander("View Underlying Calculation Data"):
    st.dataframe(filtered_master[['Company', 'Expense_Item', 'GHG_Scope3_Category', 'Spend_INR_Crores', 'Spend_GBP', 'Emissions_tCO2e']].style.format({
        'Spend_INR_Crores': '₹{:,.2f}',
        'Spend_GBP': '£{:,.2f}',
        'Emissions_tCO2e': '{:,.0f}'
    }))
import os
import pandas as pd
import config

class Scope3Model:
    def __init__(self):
        self.expenses = pd.read_csv(config.EXPENSES_FILE)
        self.mapping = pd.read_csv(config.MAPPING_FILE)
        self.factors = pd.read_csv(config.FACTORS_FILE)
        
        # Clean any accidental whitespace in string columns
        for df in [self.expenses, self.mapping, self.factors]:
            for col in df.select_dtypes(include='object').columns:
                df[col] = df[col].astype(str).str.strip()
                
        self.master_df = None

    def execute_pipeline(self):
        # Merge datasets
        df = self.expenses.merge(self.mapping, on='Expense_Item', how='left')
        df = df.merge(self.factors, on='DEFRA_Category', how='left')
        
        # Fill missing multipliers with 0 to prevent NaN propagation
        df['kgCO2e_per_GBP'] = df['kgCO2e_per_GBP'].fillna(0.0)
        
        # Financial & Carbon calculations
        df['Spend_GBP'] = (df['Spend_INR_Crores'] * config.CRORES_TO_UNITS) / config.GBP_TO_INR
        df['Emissions_tCO2e'] = (df['Spend_GBP'] * df['kgCO2e_per_GBP']) / 1000
        
        self.master_df = df
        return self

    def fetch_corporate_benchmark(self):
        summary = self.master_df.groupby(['Company', 'Revenue_INR_Crores'], as_index=False)['Emissions_tCO2e'].sum()
        summary['Carbon_Intensity (tCO2e/Cr_Rev)'] = summary['Emissions_tCO2e'] / summary['Revenue_INR_Crores']
        return summary.sort_values(by='Carbon_Intensity (tCO2e/Cr_Rev)', ascending=True)

    def fetch_category_drilldown(self, company_name):
        df = self.master_df[self.master_df['Company'] == company_name]
        return df.groupby('GHG_Scope3_Category', as_index=False)['Emissions_tCO2e'].sum()

    def export_audit_reports(self, output_dir='results'):
        os.makedirs(output_dir, exist_ok=True)
        self.master_df.to_csv(f'{output_dir}/detailed_emissions_audit.csv', index=False)
        self.fetch_corporate_benchmark().to_csv(f'{output_dir}/corporate_benchmark_summary.csv', index=False)
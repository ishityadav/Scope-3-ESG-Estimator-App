from estimator import Scope3Model
from visualizer import generate_dashboard

def run():
    print("Initializing ESG Spend-Based Data Pipeline...\n")
    model = Scope3Model().execute_pipeline()
    
    benchmark = model.fetch_corporate_benchmark()
    
    print("=== FMCG INDUSTRY BENCHMARK ===")
    print(benchmark.to_string(index=False, float_format="{:,.2f}".format))
    print("\n")
    
    for company in ["ITC Limited", "HUL", "Britannia"]:
        print(f"--- {company} Breakdown ---")
        drilldown = model.fetch_category_drilldown(company)
        print(drilldown.to_string(index=False, float_format="{:,.2f}".format))
        print("")
        
    # Export reports and generate the complete 4-panel dashboard
    model.export_audit_reports()
    generate_dashboard(benchmark, model.master_df)

if __name__ == "__main__":
    run()
https://scope-3-estimator.streamlit.app
<img width="1470" height="956" alt="Screenshot 2026-09-04 at 2 12 36 AM" src="https://github.com/user-attachments/assets/8484de7d-8012-4191-a2fa-1c64477e86ab" />


<img width="1470" height="956" alt="Screenshot 2026-09-04 at 2 12 48 AM" src="https://github.com/user-attachments/assets/4e39aef4-ae61-4da2-98ad-34ea0f9ea589" />

# 🌱 Corporate Scope 3 Carbon Estimator & Benchmarker

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38.0-FF4B4B.svg)](https://streamlit.io/)
[![GHG Protocol](https://img.shields.io/badge/Standard-GHG_Protocol-00a651.svg)](https://ghgprotocol.org/)

An automated, interactive Python data pipeline and web application that calculates and benchmarks the Scope 3 greenhouse gas (GHG) emissions of major Indian FMCG conglomerates. 

This project implements the **GHG Protocol's Spend-Based Method**, utilizing UK DEFRA Environmentally-Extended Input-Output (EEIO) conversion factors to map highly consolidated corporate financial disclosures (operating and capital expenditures) into actionable carbon footprints.

## 📌 Project Overview

Measuring Scope 3 (value-chain) emissions is highly complex due to supplier data opacity. This tool bridges verified corporate accounting with environmental science by programmatically assigning financial ledger items to specific GHG boundaries (Categories 1, 6, and 9) to generate industry benchmarks.

### Key Features
* **Interactive Streamlit Dashboard:** A live web application allowing users to manipulate macro-economic assumptions (e.g., currency exchange rates) and see real-time footprint recalculations.
* **Multi-Company Benchmarking:** Compares FY24 audited spend data across ITC Limited, Hindustan Unilever (HUL), and Britannia.
* **Carbon Intensity Metric:** Evaluates carbon efficiency (tCO₂e per ₹1 Crore Revenue) to allow for equitable comparison across different market capitalizations.
* **Spend-to-Carbon Pareto Analysis:** Visualizes the disparity between financial spend share and environmental impact share, proving that specific procurement categories (like raw materials or marketing services) carry disproportionate carbon penalties.

## 🛠️ Methodology & Analytics Pipeline

1. **Data Ingestion:** Reads verified FY24 procurement data (in ₹ INR Crores).
2. **Economic Translation:** Converts INR to GBP using historical exchange rates (FY24 Average: 105.00) to align with global environmental input-output tables.
3. **Categorical Mapping:** Maps internal accounting terminology (e.g., "Outward freight and handling") to specific DEFRA economic sectors (e.g., "Road transport services") and assigns them to the correct GHG Protocol Scope 3 Category.
4. **Emissions Calculation:** Applies the exact EEIO multiplier (kgCO₂e per £) and converts the final output into metric tonnes of CO₂ equivalent (tCO₂e).

## 📁 Repository Structure

```text
├── data/
│   ├── industry_expenses.csv       # Verified FY24 financial spend across companies
│   ├── mapping_logic.csv           # Connects financial items to DEFRA & GHG Protocols
│   └── defra_factors.csv           # UK Gov spend-based emission multipliers
├── app.py                          # The Streamlit web application frontend
├── estimator.py                    # Core Pandas data engineering and math engine
├── config.py                       # Centralized macroeconomic assumptions
├── packages.txt                    # System-level dependencies for cloud deployment
├── requirements.txt                # Python package dependencies
└── README.md<img width="1436" height="745" alt="Screenshot 2026-09-03 at 5 36 02 PM" src="https://github.com/user-attachments/assets/bca5cc81-d80d-4807-b2fd-b6954e61b44e" />

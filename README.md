# ABC Retail Group — Enterprise Business Intelligence & Advanced Analytics

## Project Overview

This project demonstrates an end-to-end enterprise retail analytics workflow using **Python, SQL, Excel, and Power BI** to support data-driven business decisions.

The project uses a simulated retail dataset covering January 2021 to December 2025. It explores sales performance, profitability, customer segmentation, marketing effectiveness, inventory risks, customer service, and revenue forecasting.

> **Data Disclaimer:** All datasets and findings are simulated for educational and portfolio purposes. They do not represent actual ABC Retail Group business results.

## Business Objectives

- Evaluate revenue, profit, and profit margins.
- Identify high-performing product categories and retail locations.
- Segment customers using RFM analysis.
- Assess marketing campaign efficiency using ROAS.
- Identify inventory replenishment and stock-out risks.
- Analyse returns and customer service performance.
- Forecast revenue and compare forecasting approaches.
- Translate analytical findings into actionable business recommendations.

## Tools & Technologies

- **Python:** pandas, NumPy
- **Data Analysis:** Exploratory Data Analysis (EDA), data validation, aggregation, RFM segmentation
- **Forecasting:** Moving Average and Seasonal Naive models; backtesting with MAE and MAPE
- **Data Storage & Reporting:** CSV datasets and automated text reports
- **Planned / Further Development:** SQL, Excel, and Power BI integration

## Dataset Overview

The project contains 10 simulated datasets:

| Dataset | Records |
|---|---:|
| Customers | 5,000 |
| Products | 300 |
| Stores | 12 |
| Orders | 20,000 |
| Order Items | 50,000 |
| Returns | 1,500 |
| Inventory | 3,600 |
| Marketing Campaigns | 100 |
| Customer Interactions | 10,000 |
| Date Dimension | 1,826 |

**Total: 92,338 records**

## Key Analytical Findings

- **Revenue:** 1.866 billion in simulated currency units.
- **Profit:** 619.29 million in simulated currency units.
- **Profit Margin:** 33.19%.
- **Top Revenue Category:** Electronics.
- **Marketing ROAS:** 3.16x across the simulated campaigns.
- **Inventory Attention:** 636 records require replenishment attention or are out of stock.
- **Customer Service:** 74.36% of interactions are marked as resolved.
- **Customer Segmentation:** RFM analysis identifies high-value, loyal, at-risk, potential loyalist, and needs-review customer groups.
- **Revenue Forecasting:** The three-month moving average achieved a MAPE of 4.54% on the October–December 2025 test window, compared with 5.47% for the seasonal naive model.

These results describe the generated dataset only. Forecast performance is based on a short three-month test window and requires further validation.

## Project Structure

```text
ABC_Retail_Enterprise_Analytics/
├── data/
├── outputs/
├── reports/
├── generate_dataset.py
├── eda_analysis.py
├── business_insights_report.py
├── requirements.txt

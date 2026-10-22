
import pandas as pd
from pathlib import Path
from datetime import date

# Project folders
DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")
REPORT_DIR = Path("reports")

REPORT_DIR.mkdir(exist_ok=True)

# Load business datasets
orders = pd.read_csv(DATA_DIR / "orders.csv")
items = pd.read_csv(DATA_DIR / "order_items.csv")
customers = pd.read_csv(DATA_DIR / "customers.csv")
products = pd.read_csv(DATA_DIR / "products.csv")
campaigns = pd.read_csv(DATA_DIR / "marketing_campaigns.csv")
inventory = pd.read_csv(DATA_DIR / "inventory.csv")
returns = pd.read_csv(DATA_DIR / "returns.csv")
interactions = pd.read_csv(DATA_DIR / "customer_interactions.csv")

# Merge order information with sales items
sales = items.merge(
    orders[["Order_ID", "Customer_ID", "Store_ID",
            "Order_Date", "Order_Status"]],
    on="Order_ID",
    how="left",
    validate="many_to_one"
)

# Business KPIs
total_revenue = sales["Line_Revenue"].sum()
total_profit = sales["Line_Profit"].sum()
profit_margin = (
    total_profit / total_revenue * 100
    if total_revenue else 0
)

total_orders = sales["Order_ID"].nunique()
total_customers = customers["Customer_ID"].nunique()

active_customers = sales["Customer_ID"].nunique()

# Product category performance
product_sales = sales.merge(
    products[["Product_ID", "Category"]],
    on="Product_ID",
    how="left"
)

category_summary = (
    product_sales.groupby("Category", as_index=False)
    .agg(
        Revenue=("Line_Revenue", "sum"),
        Profit=("Line_Profit", "sum")
    )
    .sort_values("Revenue", ascending=False)
)

top_category = category_summary.iloc[0]

# Marketing performance
total_ad_spend = campaigns["Ad_Spend"].sum()
total_attributed_revenue = campaigns["Revenue_Attributed"].sum()

overall_roas = (
    total_attributed_revenue / total_ad_spend
    if total_ad_spend else 0
)

# Inventory risks
inventory_risks = inventory[
    inventory["Stock_Status"].isin(
        ["Reorder Required", "Out of Stock"]
    )
]

out_of_stock = (
    inventory["Stock_Status"] == "Out of Stock"
).sum()

# Returns and customer service
total_returns = len(returns)

resolved_count = (
    interactions["Status"] == "Resolved"
).sum()

resolution_rate = (
    resolved_count / len(interactions) * 100
    if len(interactions) else 0
)

avg_satisfaction = interactions[
    "Customer_Satisfaction"
].mean()

# Create management report
report = f"""
ABC RETAIL GROUP
ENTERPRISE BUSINESS INSIGHTS REPORT
===================================

Report Date: {date.today().isoformat()}
Data Type: Simulated business data
Historical Period: January 2021 - December 2025

1. EXECUTIVE SUMMARY
--------------------
Total Revenue: {total_revenue:,.2f}
Total Profit: {total_profit:,.2f}
Profit Margin: {profit_margin:.2f}%
Orders with Sales Items: {total_orders:,}
Total Customers in Dataset: {total_customers:,}
Customers with Sales: {active_customers:,}

2. PRODUCT CATEGORY PERFORMANCE
--------------------------------
Highest-Revenue Category: {top_category['Category']}
Category Revenue: {top_category['Revenue']:,.2f}
Category Profit: {top_category['Profit']:,.2f}

Full category results:
{category_summary.to_string(index=False, formatters={
    "Revenue": "{:,.2f}".format,
    "Profit": "{:,.2f}".format
})}

3. MARKETING PERFORMANCE
------------------------
Total Advertising Spend: {total_ad_spend:,.2f}
Attributed Revenue: {total_attributed_revenue:,.2f}
Overall ROAS: {overall_roas:.2f}x

Note: Attributed revenue is not necessarily incremental revenue
or profit. Campaign profitability requires additional analysis.


4. CUSTOMER SEGMENTATION
------------------------
At-Risk Customers: 1,937
High-Value Customers: 449
Loyal Customers: 114
Potential Loyalists: 249
Needs Review: 2,251

Business Recommendations:
1. Create targeted win-back campaigns for at-risk customers.
2. Offer relevant loyalty benefits to high-value customers.
3. Encourage potential loyalists to make repeat purchases.
4. Review the Needs Review segment to identify customers
   who may benefit from targeted engagement.

Note: These segments are based on simulated historical
customer data. Validate customer behaviour before applying
real-world marketing actions.

5. INVENTORY MANAGEMENT
-----------------------
Inventory Records Requiring Reorder or Out of Stock:
{len(inventory_risks):,}
Out-of-Stock Records: {out_of_stock:,}

Recommendation:
Prioritize stock-out products and review reorder quantities,
supplier lead times, and demand before replenishment.

6. RETURNS AND CUSTOMER SERVICE
--------------------------------
Return Records: {total_returns:,}
Resolved Customer Interactions: {resolved_count:,}
Interaction Resolution Rate: {resolution_rate:.2f}%
Average Customer Satisfaction: {avg_satisfaction:.2f}/5

Recommendation:
Investigate common return reasons and unresolved customer
interactions. Compare resolution times with internal service targets.


7. MANAGEMENT RECOMMENDATIONS
------------------------------

Recommendation 1: Protect Core Revenue Categories
Finding: Electronics is the highest-revenue category.
Evidence: Revenue is 987,053,658.84 and profit is
327,338,245.12.
Action: Monitor electronics stock availability, product-level
profit margins, returns, and demand before changing stock
or pricing decisions.

Recommendation 2: Improve Inventory Availability
Finding: 636 inventory records require replenishment attention
or are out of stock.
Evidence: 23 records are classified as Out of Stock.
Action: Prioritize high-demand products with low stock, verify
reorder levels, and consider supplier lead times before
placing replenishment orders.

Recommendation 3: Optimize Marketing Investment
Finding: Overall reported ROAS is 3.16x.
Evidence: Advertising spend is 21,479,733.99 and attributed
revenue is 67,805,247.59.
Action: Compare campaigns using cost per conversion, margins,
incremental impact, and campaign objectives before reallocating
marketing budgets.

Recommendation 4: Improve Customer Support
Finding: The interaction resolution rate is 74.36%.
Evidence: 7,436 out of 10,000 interactions are marked Resolved.
Action: Review pending and escalated cases, identify recurring
issues, and monitor resolution time and customer satisfaction.

Recommendation 5: Investigate Product Returns
Finding: There are 1,500 return records.
Evidence: Return reasons and product categories vary.
Action: Review return reasons by product and category to
identify possible quality, delivery, or product-description
issues before taking corrective action.

Recommendation 6: Use Forecasts Carefully
Finding: The 3-month moving average performed better than the
seasonal naive model in the current test.
Evidence: Moving average MAPE is 4.54%; seasonal naive MAPE
is 5.47% for October-December 2025.
Action: Treat moving average as a preliminary baseline and
test additional historical periods before using forecasts
for inventory or operational planning.


LIMITATIONS
-----------
This project uses simulated data. Findings describe the generated
dataset and should not be presented as actual ABC Retail Group results.
Marketing attribution does not establish causation.
"""

# Save report
report_path = REPORT_DIR / "business_insights_report.txt"
report_path.write_text(report, encoding="utf-8")

# Export category summary for further reporting
category_summary.to_csv(
    OUTPUT_DIR / "category_business_summary.csv",
    index=False
)

print("BUSINESS INSIGHTS REPORT GENERATED")
print(f"Report saved to: {report_path}")
print(f"Category summary saved to: {OUTPUT_DIR / 'category_business_summary.csv'}")

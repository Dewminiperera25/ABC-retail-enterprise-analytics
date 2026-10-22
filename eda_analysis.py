
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")

files = [
    "customers.csv",
    "products.csv",
    "stores.csv",
    "orders.csv",
    "order_items.csv",
    "returns.csv",
    "inventory.csv",
    "marketing_campaigns.csv",
    "customer_interactions.csv",
    "date_dimension.csv",
]

print("=" * 60)
print("ABC RETAIL GROUP - DATASET OVERVIEW")
print("=" * 60)

for file in files:
    df = pd.read_csv(DATA_DIR / file)

    print(f"\nDataset: {file}")
    print(f"Rows: {df.shape[0]:,}")
    print(f"Columns: {df.shape[1]}")
    print(f"Missing cells: {df.isnull().sum().sum():,}")
    print(f"Duplicate rows: {df.duplicated().sum():,}")
    print("-" * 40)

# BUSINESS PERFORMANCE ANALYSIS

orders = pd.read_csv(DATA_DIR / "orders.csv")
items = pd.read_csv(DATA_DIR / "order_items.csv")

# Combine order details with order status
sales = items.merge(
    orders[["Order_ID", "Order_Status", "Order_Date"]],
    on="Order_ID",
    how="left",
    validate="many_to_one"
)

total_revenue = sales["Line_Revenue"].sum()
total_cost = sales["Line_Cost"].sum()
total_profit = sales["Line_Profit"].sum()
profit_margin = (total_profit / total_revenue * 100) if total_revenue else 0

revenue_orders = sales["Order_ID"].nunique()

print("\n" + "=" * 60)
print("BUSINESS PERFORMANCE ANALYSIS")
print("=" * 60)

print(f"Total Revenue: {total_revenue:,.2f}")
print(f"Total Cost: {total_cost:,.2f}")
print(f"Total Profit: {total_profit:,.2f}")
print(f"Profit Margin: {profit_margin:.2f}%")
print(f"Orders with Sales Items: {revenue_orders:,}")

print("\nORDER STATUS SUMMARY")
print(orders["Order_Status"].value_counts().to_string())

print("\nREVENUE AND PROFIT BY ORDER STATUS")
status_summary = sales.groupby("Order_Status").agg(
    Revenue=("Line_Revenue", "sum"),
    Cost=("Line_Cost", "sum"),
    Profit=("Line_Profit", "sum"),
    Order_Count=("Order_ID", "nunique")
).sort_values("Revenue", ascending=False)

print(status_summary.round(2).to_string())

# MONTHLY REVENUE ANALYSIS

sales["Order_Date"] = pd.to_datetime(sales["Order_Date"])

sales["Year_Month"] = sales["Order_Date"].dt.to_period("M").astype(str)

monthly_revenue = (
    sales.groupby("Year_Month")
    .agg(
        Revenue=("Line_Revenue", "sum"),
        Profit=("Line_Profit", "sum"),
        Orders=("Order_ID", "nunique")
    )
    .reset_index()
)

monthly_revenue = monthly_revenue.sort_values("Year_Month")

print("\n" + "=" * 60)
print("MONTHLY REVENUE ANALYSIS")
print("=" * 60)

print(monthly_revenue.to_string(index=False))

print("\nTOP 5 MONTHS BY REVENUE")
print(
    monthly_revenue.nlargest(5, "Revenue")
    .round(2)
    .to_string(index=False)
)

# PRODUCT CATEGORY ANALYSIS

products = pd.read_csv(DATA_DIR / "products.csv")

product_sales = sales.merge(
    products[["Product_ID", "Product_Name", "Category"]],
    on="Product_ID",
    how="left",
    validate="many_to_one"
)

category_summary = (
    product_sales.groupby("Category")
    .agg(
        Revenue=("Line_Revenue", "sum"),
        Cost=("Line_Cost", "sum"),
        Profit=("Line_Profit", "sum"),
        Quantity_Sold=("Quantity", "sum"),
        Order_Count=("Order_ID", "nunique")
    )
    .reset_index()
)

category_summary["Profit_Margin_%"] = (
    category_summary["Profit"] /
    category_summary["Revenue"] * 100
)

category_summary = category_summary.sort_values(
    "Revenue", ascending=False
)

print("\n" + "=" * 60)
print("REVENUE AND PROFIT BY PRODUCT CATEGORY")
print("=" * 60)

print(category_summary.round(2).to_string(index=False))

print("\nTOP 10 PRODUCTS BY REVENUE")

top_products = (
    product_sales.groupby("Product_Name")
    .agg(
        Revenue=("Line_Revenue", "sum"),
        Profit=("Line_Profit", "sum"),
        Quantity_Sold=("Quantity", "sum")
    )
    .reset_index()
    .nlargest(10, "Revenue")
)

print(top_products.round(2).to_string(index=False))

# STORE PERFORMANCE ANALYSIS

stores = pd.read_csv(DATA_DIR / "stores.csv")

store_sales = sales.merge(
    orders[["Order_ID", "Store_ID"]],
    on="Order_ID",
    how="left",
    validate="many_to_one"
)

store_sales = store_sales.merge(
    stores[["Store_ID", "Store_Name", "City", "Region"]],
    on="Store_ID",
    how="left",
    validate="many_to_one"
)

store_summary = (
    store_sales.groupby(["Store_Name", "City", "Region"])
    .agg(
        Revenue=("Line_Revenue", "sum"),
        Profit=("Line_Profit", "sum"),
        Orders=("Order_ID", "nunique"),
        Quantity_Sold=("Quantity", "sum")
    )
    .reset_index()
    .sort_values("Revenue", ascending=False)
)

store_summary["Profit_Margin_%"] = (
    store_summary["Profit"] /
    store_summary["Revenue"] * 100
)

print("\n" + "=" * 60)
print("STORE PERFORMANCE ANALYSIS")
print("=" * 60)

print(store_summary.round(2).to_string(index=False))

print("\nTOP 5 STORES BY REVENUE")
print(store_summary.nlargest(5, "Revenue").round(2).to_string(index=False))

# CUSTOMER SEGMENT ANALYSIS

customers = pd.read_csv(DATA_DIR / "customers.csv")

customer_sales = sales.merge(
    orders[["Order_ID", "Customer_ID"]],
    on="Order_ID",
    how="left",
    validate="many_to_one"
)

customer_sales = customer_sales.merge(
    customers[["Customer_ID", "Customer_Segment"]],
    on="Customer_ID",
    how="left",
    validate="many_to_one"
)

segment_summary = (
    customer_sales.groupby("Customer_Segment")
    .agg(
        Revenue=("Line_Revenue", "sum"),
        Profit=("Line_Profit", "sum"),
        Orders=("Order_ID", "nunique"),
        Quantity_Sold=("Quantity", "sum"),
        Unique_Customers=("Customer_ID", "nunique")
    )
    .reset_index()
)

segment_summary["Profit_Margin_%"] = (
    segment_summary["Profit"] /
    segment_summary["Revenue"] * 100
)

segment_summary = segment_summary.sort_values(
    "Revenue", ascending=False
)

print("\n" + "=" * 60)
print("CUSTOMER SEGMENT ANALYSIS")
print("=" * 60)

print(segment_summary.round(2).to_string(index=False))

# INVENTORY AND STOCK RISK ANALYSIS

inventory = pd.read_csv(DATA_DIR / "inventory.csv")

products = pd.read_csv(DATA_DIR / "products.csv")
stores = pd.read_csv(DATA_DIR / "stores.csv")

inventory_analysis = inventory.merge(
    products[["Product_ID", "Product_Name", "Category"]],
    on="Product_ID",
    how="left",
    validate="many_to_one"
).merge(
    stores[["Store_ID", "Store_Name"]],
    on="Store_ID",
    how="left",
    validate="many_to_one"
)

print("\n" + "=" * 60)
print("INVENTORY STOCK STATUS")
print("=" * 60)

print(inventory_analysis["Stock_Status"].value_counts().to_string())

print("\nSTOCK STATUS BY CATEGORY")

stock_by_category = pd.crosstab(
    inventory_analysis["Category"],
    inventory_analysis["Stock_Status"]
)

print(stock_by_category.to_string())

print("\nLOW STOCK / OUT OF STOCK ITEMS")

risk_items = inventory_analysis[
    inventory_analysis["Stock_Status"].isin(
        ["Reorder Required", "Out of Stock"]
    )
]

print(f"Items requiring attention: {len(risk_items):,}")
print(
    risk_items[
        ["Product_ID", "Product_Name", "Category",
         "Store_Name", "Stock_On_Hand",
         "Reorder_Level", "Stock_Status"]
    ].head(15).to_string(index=False)
)

# MARKETING CAMPAIGN PERFORMANCE

campaigns = pd.read_csv(DATA_DIR / "marketing_campaigns.csv")

campaigns["Calculated_ROAS"] = (
    campaigns["Revenue_Attributed"] / campaigns["Ad_Spend"]
)

print("\n" + "=" * 60)
print("MARKETING CAMPAIGN PERFORMANCE")
print("=" * 60)

total_ad_spend = campaigns["Ad_Spend"].sum()
total_attributed_revenue = campaigns["Revenue_Attributed"].sum()

overall_roas = (
    total_attributed_revenue / total_ad_spend
    if total_ad_spend else 0
)

print(f"Total Ad Spend: {total_ad_spend:,.2f}")
print(f"Total Attributed Revenue: {total_attributed_revenue:,.2f}")
print(f"Overall ROAS: {overall_roas:.2f}x")

print("\nTOP 10 CAMPAIGNS BY ROAS")

top_campaigns = campaigns.nlargest(10, "Calculated_ROAS")[
    ["Campaign_Name", "Channel", "Ad_Spend",
     "Revenue_Attributed", "Calculated_ROAS",
     "Click_Through_Rate", "Conversion_Rate"]
]

print(top_campaigns.round(2).to_string(index=False))

print("\nPERFORMANCE BY MARKETING CHANNEL")

channel_summary = campaigns.groupby("Channel").agg(
    Campaigns=("Campaign_ID", "count"),
    Ad_Spend=("Ad_Spend", "sum"),
    Revenue_Attributed=("Revenue_Attributed", "sum"),
    Clicks=("Clicks", "sum"),
    Conversions=("Conversions", "sum")
).reset_index()

channel_summary["ROAS"] = (
    channel_summary["Revenue_Attributed"] /
    channel_summary["Ad_Spend"]
)

print(channel_summary.round(2).to_string(index=False))

# CUSTOMER SERVICE PERFORMANCE

interactions = pd.read_csv(
    DATA_DIR / "customer_interactions.csv"
)

total_interactions = len(interactions)
status_counts = interactions["Status"].value_counts()

resolved_count = (
    interactions["Status"].eq("Resolved").sum()
)

resolved_rate = (
    resolved_count / total_interactions * 100
    if total_interactions else 0
)

avg_satisfaction = interactions[
    "Customer_Satisfaction"
].mean()

avg_resolution_hours = interactions.loc[
    interactions["Status"].eq("Resolved"),
    "Resolution_Hours"
].mean()

print("\n" + "=" * 60)
print("CUSTOMER SERVICE PERFORMANCE")
print("=" * 60)

print(f"Total Interactions: {total_interactions:,}")
print(f"Resolved Interactions: {resolved_count:,}")
print(f"Resolution Rate: {resolved_rate:.2f}%")
print(f"Average Customer Satisfaction: {avg_satisfaction:.2f}/5")
print(f"Average Resolution Time (Resolved): {avg_resolution_hours:.2f} hours")

print("\nINTERACTIONS BY STATUS")
print(status_counts.to_string())

print("\nAVERAGE SATISFACTION BY STATUS")
print(
    interactions.groupby("Status")["Customer_Satisfaction"]
    .mean()
    .round(2)
    .to_string()
)

print("\nINTERACTIONS BY CHANNEL")
print(interactions["Channel"].value_counts().to_string())

# CUSTOMER BUYING BEHAVIOUR ANALYSIS

customer_orders = orders[
    ["Order_ID", "Customer_ID", "Order_Status", "Order_Date"]
].copy()

customer_orders["Order_Date"] = pd.to_datetime(
    customer_orders["Order_Date"]
)

# Count orders and calculate sales for each customer
customer_order_summary = (
    sales.merge(
        customer_orders[["Order_ID", "Customer_ID"]],
        on="Order_ID",
        how="left",
        validate="many_to_one"
    )
    .groupby("Customer_ID")
    .agg(
        Total_Revenue=("Line_Revenue", "sum"),
        Total_Profit=("Line_Profit", "sum"),
        Total_Orders=("Order_ID", "nunique"),
        Total_Quantity=("Quantity", "sum")
    )
    .reset_index()
)

# Include customers who have no sales
all_customers = pd.read_csv(DATA_DIR / "customers.csv")

customer_order_summary = all_customers[
    ["Customer_ID", "Customer_Name", "Customer_Segment", "Region"]
].merge(
    customer_order_summary,
    on="Customer_ID",
    how="left",
    validate="one_to_one"
)

customer_order_summary[
    ["Total_Revenue", "Total_Profit", "Total_Orders", "Total_Quantity"]
] = customer_order_summary[
    ["Total_Revenue", "Total_Profit", "Total_Orders", "Total_Quantity"]
].fillna(0)

repeat_customers = (
    customer_order_summary["Total_Orders"] > 1
).sum()

active_customers = (
    customer_order_summary["Total_Orders"] > 0
).sum()

repeat_customer_rate = (
    repeat_customers / active_customers * 100
    if active_customers else 0
)

avg_revenue_per_customer = (
    customer_order_summary["Total_Revenue"].sum() / active_customers
    if active_customers else 0
)

print("\n" + "=" * 60)
print("CUSTOMER BUYING BEHAVIOUR ANALYSIS")
print("=" * 60)

print(f"Total Customers: {len(customer_order_summary):,}")
print(f"Customers with Sales: {active_customers:,}")
print(f"Repeat Customers: {repeat_customers:,}")
print(f"Repeat Customer Rate: {repeat_customer_rate:.2f}%")
print(f"Average Revenue per Active Customer: {avg_revenue_per_customer:,.2f}")

print("\nTOP 10 CUSTOMERS BY REVENUE")

print(
    customer_order_summary.nlargest(10, "Total_Revenue")[
        ["Customer_ID", "Customer_Segment", "Region",
         "Total_Revenue", "Total_Profit", "Total_Orders"]
    ].round(2).to_string(index=False)
)

# CUSTOMER SEGMENT VALUE ANALYSIS

segment_value = (
    customer_order_summary
    .groupby("Customer_Segment")
    .agg(
        Total_Customers=("Customer_ID", "nunique"),
        Active_Customers=("Total_Orders", lambda x: (x > 0).sum()),
        Total_Revenue=("Total_Revenue", "sum"),
        Total_Profit=("Total_Profit", "sum")
    )
    .reset_index()
)

segment_value["Revenue_Per_Active_Customer"] = (
    segment_value["Total_Revenue"] /
    segment_value["Active_Customers"].replace(0, pd.NA)
)

segment_value["Profit_Per_Active_Customer"] = (
    segment_value["Total_Profit"] /
    segment_value["Active_Customers"].replace(0, pd.NA)
)

segment_value["Active_Customer_Rate_%"] = (
    segment_value["Active_Customers"] /
    segment_value["Total_Customers"] * 100
)

segment_value = segment_value.sort_values(
    "Revenue_Per_Active_Customer",
    ascending=False
)

print("\n" + "=" * 60)
print("CUSTOMER SEGMENT VALUE ANALYSIS")
print("=" * 60)

print(segment_value.round(2).to_string(index=False))

# CUSTOMER RECENCY ANALYSIS

# Use the latest date in the orders dataset
reference_date = orders["Order_Date"].max()
reference_date = pd.to_datetime(reference_date)

completed_orders = orders[
    orders["Order_Status"].isin(["Completed", "Returned"])
].copy()

completed_orders["Order_Date"] = pd.to_datetime(
    completed_orders["Order_Date"]
)

last_purchase = (
    completed_orders.groupby("Customer_ID")["Order_Date"]
    .max()
    .reset_index()
)

last_purchase.rename(
    columns={"Order_Date": "Last_Purchase_Date"},
    inplace=True
)

customer_recency = all_customers[
    ["Customer_ID", "Customer_Name", "Customer_Segment"]
].merge(
    last_purchase,
    on="Customer_ID",
    how="left"
)

customer_recency["Days_Since_Last_Purchase"] = (
    reference_date - customer_recency["Last_Purchase_Date"]
).dt.days

customer_recency["Recency_Group"] = pd.cut(
    customer_recency["Days_Since_Last_Purchase"],
    bins=[-1, 30, 90, 180, float("inf")],
    labels=["0-30 Days", "31-90 Days", "91-180 Days", "180+ Days"]
)

customer_recency["Recency_Group"] = (
    customer_recency["Recency_Group"]
    .cat.add_categories(["No Purchase"])
    .fillna("No Purchase")
)

print("\n" + "=" * 60)
print("CUSTOMER RECENCY ANALYSIS")
print("=" * 60)

print(f"Reference Date: {reference_date.date()}")

print("\nCUSTOMERS BY RECENCY GROUP")

print(
    customer_recency["Recency_Group"]
    .value_counts()
    .to_string()
)

print("\nRECENCY BY CUSTOMER SEGMENT")

print(
    pd.crosstab(
        customer_recency["Customer_Segment"],
        customer_recency["Recency_Group"]
    ).to_string()
)

# RFM CUSTOMER SEGMENTATION

rfm = customer_order_summary[
    ["Customer_ID", "Total_Orders", "Total_Revenue"]
].merge(
    customer_recency[
        ["Customer_ID", "Days_Since_Last_Purchase"]
    ],
    on="Customer_ID",
    how="left",
    validate="one_to_one"
)

# Calculate R, F, and M scores
# Higher Recency score = more recent purchase
rfm["R_Score"] = pd.cut(
    rfm["Days_Since_Last_Purchase"],
    bins=[-1, 30, 90, 180, float("inf")],
    labels=[4, 3, 2, 1]
).astype(float)

rfm["F_Score"] = (
    pd.qcut(
        rfm["Total_Orders"].rank(method="first"),
        q=4,
        labels=[1, 2, 3, 4]
    ).astype(float)
)

rfm["M_Score"] = (
    pd.qcut(
        rfm["Total_Revenue"].rank(method="first"),
        q=4,
        labels=[1, 2, 3, 4]
    ).astype(float)
)

# Assign simple business-friendly segments
rfm["RFM_Segment"] = "Needs Review"

rfm.loc[
    (rfm["R_Score"] >= 3) &
    (rfm["F_Score"] >= 3) &
    (rfm["M_Score"] >= 3),
    "RFM_Segment"
] = "High Value"

rfm.loc[
    (rfm["R_Score"] >= 3) &
    (rfm["F_Score"] >= 3) &
    (rfm["RFM_Segment"] != "High Value"),
    "RFM_Segment"
] = "Loyal Customers"

rfm.loc[
    (rfm["R_Score"] <= 2) &
    (rfm["F_Score"] >= 3),
    "RFM_Segment"
] = "At Risk"

rfm.loc[
    (rfm["R_Score"] >= 3) &
    (rfm["F_Score"] <= 2),
    "RFM_Segment"
] = "Potential Loyalists"

print("\n" + "=" * 60)
print("RFM CUSTOMER SEGMENTATION")
print("=" * 60)

print("\nCUSTOMERS BY RFM SEGMENT")

print(
    rfm["RFM_Segment"]
    .value_counts()
    .to_string()
)

print("\nAVERAGE REVENUE AND ORDERS BY RFM SEGMENT")

print(
    rfm.groupby("RFM_Segment", observed=True)
    .agg(
        Customers=("Customer_ID", "nunique"),
        Avg_Revenue=("Total_Revenue", "mean"),
        Avg_Orders=("Total_Orders", "mean")
    )
    .round(2)
    .to_string()
)
from pathlib import Path
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)
# Export customer-level RFM segmentation results
rfm.to_csv(
    output_dir / "rfm_customer_segments.csv",
    index=False
)

output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)
# Export customer-level RFM segmentation results
rfm.to_csv(
    output_dir / "rfm_customer_segments.csv",
    index=False
)
# Export RFM segment summary
rfm_summary = (
    rfm.groupby("RFM_Segment", observed=True)
    .agg(
        Customers=("Customer_ID", "nunique"),
        Avg_Revenue=("Total_Revenue", "mean"),
        Avg_Orders=("Total_Orders", "mean")
    )
    .round(2)
    .reset_index()
)

rfm_summary.to_csv(
    output_dir / "rfm_segment_summary.csv",
    index=False
)

print("\nRFM CSV FILES EXPORTED")
print("outputs/rfm_customer_segments.csv")
print("outputs/rfm_segment_summary.csv")
# MARKETING EFFICIENCY ANALYSIS

campaigns["Calculated_Conversion_Rate_%"] = (
    campaigns["Conversions"] /
    campaigns["Clicks"].replace(0, pd.NA) * 100
)

campaigns["Cost_Per_Conversion"] = (
    campaigns["Ad_Spend"] /
    campaigns["Conversions"].replace(0, pd.NA)
)

channel_efficiency = (
    campaigns.groupby("Channel")
    .agg(
        Campaigns=("Campaign_ID", "count"),
        Ad_Spend=("Ad_Spend", "sum"),
        Clicks=("Clicks", "sum"),
        Conversions=("Conversions", "sum"),
        Revenue=("Revenue_Attributed", "sum")
    )
    .reset_index()
)

channel_efficiency["Conversion_Rate_%"] = (
    channel_efficiency["Conversions"] /
    channel_efficiency["Clicks"].replace(0, pd.NA) * 100
)

channel_efficiency["Cost_Per_Conversion"] = (
    channel_efficiency["Ad_Spend"] /
    channel_efficiency["Conversions"].replace(0, pd.NA)
)

channel_efficiency["ROAS"] = (
    channel_efficiency["Revenue"] /
    channel_efficiency["Ad_Spend"].replace(0, pd.NA)
)

channel_efficiency = channel_efficiency.sort_values(
    "Cost_Per_Conversion"
)

print("\n" + "=" * 60)
print("MARKETING EFFICIENCY ANALYSIS")
print("=" * 60)

print(
    channel_efficiency.round(2).to_string(index=False)
)

# PRODUCT RETURNS ANALYSIS

returns = pd.read_csv(DATA_DIR / "returns.csv")
products = pd.read_csv(DATA_DIR / "products.csv")

returns_analysis = returns.merge(
    products[["Product_ID", "Product_Name", "Category"]],
    on="Product_ID",
    how="left",
    validate="many_to_one"
)

total_returns = len(returns_analysis)

print("\n" + "=" * 60)
print("PRODUCT RETURNS ANALYSIS")
print("=" * 60)

print(f"Total Return Records: {total_returns:,}")

print("\nRETURNS BY REASON")

print(
    returns_analysis["Return_Reason"]
    .value_counts()
    .to_string()
)

print("\nRETURNS BY PRODUCT CATEGORY")

print(
    returns_analysis.groupby("Category")
    .size()
    .sort_values(ascending=False)
    .to_string()
)

print("\nTOP 10 PRODUCTS BY RETURN COUNT")

top_returned_products = (
    returns_analysis.groupby(
        ["Product_ID", "Product_Name", "Category"]
    )
    .size()
    .reset_index(name="Return_Count")
    .sort_values("Return_Count", ascending=False)
    .head(10)
)

print(top_returned_products.to_string(index=False))

print("\nREFUND STATUS SUMMARY")

print(
    returns_analysis["Refund_Status"]
    .value_counts()
    .to_string()
)

# RETURN RATE BY PRODUCT CATEGORY

# Count sold quantities and unique orders by category
category_sales = (
    product_sales.groupby("Category")
    .agg(
        Units_Sold=("Quantity", "sum"),
        Sales_Orders=("Order_ID", "nunique"),
        Sales_Revenue=("Line_Revenue", "sum")
    )
    .reset_index()
)

# Count return records and returned quantities by category
# Each record in returns.csv represents one return record.
category_returns = (
    returns_analysis.groupby("Category")
    .agg(
        Return_Records=("Return_ID", "count"),
        Returned_Products=("Product_ID", "count")
    )
    .reset_index()
)

category_return_rate = category_sales.merge(
    category_returns,
    on="Category",
    how="left",
    validate="one_to_one"
)

category_return_rate[
    ["Return_Records", "Returned_Products"]
] = category_return_rate[
    ["Return_Records", "Returned_Products"]
].fillna(0)

category_return_rate["Return_Records_Per_1000_Units_Sold"] = (
    category_return_rate["Return_Records"] /
    category_return_rate["Units_Sold"].replace(0, pd.NA) * 1000
)

category_return_rate = category_return_rate.sort_values(
    "Return_Records_Per_1000_Units_Sold",
    ascending=False
)

print("\n" + "=" * 60)
print("RETURN RATE BY PRODUCT CATEGORY")
print("=" * 60)

print(
    category_return_rate.round(2).to_string(index=False)
)

# MONTHLY REVENUE FORECASTING - DATA PREPARATION

monthly_forecast_data = monthly_revenue.copy()

monthly_forecast_data["Year_Month"] = pd.to_datetime(
    monthly_forecast_data["Year_Month"]
)

monthly_forecast_data = (
    monthly_forecast_data
    .sort_values("Year_Month")
    .set_index("Year_Month")
    .asfreq("MS")
)

print("\n" + "=" * 60)
print("MONTHLY REVENUE FORECASTING - DATA CHECK")
print("=" * 60)

print(f"First Month: {monthly_forecast_data.index.min().date()}")
print(f"Last Month: {monthly_forecast_data.index.max().date()}")
print(f"Number of Months: {len(monthly_forecast_data)}")

print(
    f"Missing Monthly Revenue Values: "
    f"{monthly_forecast_data['Revenue'].isna().sum()}"
)

print("\nLATEST 6 MONTHS OF REVENUE")

print(
    monthly_forecast_data[["Revenue"]]
    .tail(6)
    .round(2)
    .to_string()
)

# BASELINE REVENUE FORECAST - 3 MONTH MOVING AVERAGE

recent_revenue = monthly_forecast_data["Revenue"].dropna()

# Forecast the next month using the latest 3 months
last_3_months_average = recent_revenue.tail(3).mean()

print("\n" + "=" * 60)
print("BASELINE REVENUE FORECAST")
print("=" * 60)

print("Method: 3-Month Moving Average")
print(f"Average Revenue of Latest 3 Months: {last_3_months_average:,.2f}")

# Generate 3 recursive monthly forecasts
forecast_values = []
history = recent_revenue.tolist()

for i in range(3):
    forecast_value = sum(history[-3:]) / 3
    forecast_values.append(forecast_value)
    history.append(forecast_value)

forecast_dates = pd.date_range(
    start=monthly_forecast_data.index.max() + pd.offsets.MonthBegin(1),
    periods=3,
    freq="MS"
)

forecast_df = pd.DataFrame({
    "Forecast_Month": forecast_dates,
    "Forecast_Revenue": forecast_values
})

print("\nNEXT 3 MONTHS REVENUE FORECAST")

print(
    forecast_df.to_string(
        index=False,
        formatters={"Forecast_Revenue": "{:,.2f}".format}
    )
)

# FORECAST ACCURACY BACKTEST

# Use data only up to September 2025
train_data = monthly_forecast_data.loc[
    :"2025-09-01", "Revenue"
].dropna()

# Actual revenue for October-December 2025
actual_data = monthly_forecast_data.loc[
    "2025-10-01":"2025-12-01", "Revenue"
]

# Generate recursive 3-month moving-average forecasts
history = train_data.tolist()
backtest_forecasts = []

for i in range(3):
    predicted_value = sum(history[-3:]) / 3
    backtest_forecasts.append(predicted_value)
    history.append(predicted_value)

backtest_df = pd.DataFrame({
    "Actual_Revenue": actual_data.to_numpy(),
    "Forecast_Revenue": backtest_forecasts
}, index=actual_data.index)

backtest_df["Absolute_Error"] = (
    backtest_df["Actual_Revenue"] -
    backtest_df["Forecast_Revenue"]
).abs()

backtest_df["Absolute_Percentage_Error_%"] = (
    backtest_df["Absolute_Error"] /
    backtest_df["Actual_Revenue"] * 100
)

mae = backtest_df["Absolute_Error"].mean()
mape = backtest_df["Absolute_Percentage_Error_%"].mean()

print("\n" + "=" * 60)
print("FORECAST ACCURACY BACKTEST")
print("=" * 60)

print(backtest_df.round(2).to_string())

print(f"\nMean Absolute Error (MAE): {mae:,.2f}")
print(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")

# SEASONAL NAIVE FORECAST ACCURACY BACKTEST

# Use data up to September 2025 for testing
actual_data = monthly_forecast_data.loc[
    "2025-10-01":"2025-12-01", "Revenue"
]

# Use the same months from the previous year as forecasts
seasonal_forecasts = monthly_forecast_data.loc[
    "2024-10-01":"2024-12-01", "Revenue"
].to_numpy()

seasonal_backtest_df = pd.DataFrame({
    "Actual_Revenue": actual_data.to_numpy(),
    "Forecast_Revenue": seasonal_forecasts
}, index=actual_data.index)

seasonal_backtest_df["Absolute_Error"] = (
    seasonal_backtest_df["Actual_Revenue"] -
    seasonal_backtest_df["Forecast_Revenue"]
).abs()

seasonal_backtest_df["Absolute_Percentage_Error_%"] = (
    seasonal_backtest_df["Absolute_Error"] /
    seasonal_backtest_df["Actual_Revenue"] * 100
)

seasonal_mae = seasonal_backtest_df["Absolute_Error"].mean()
seasonal_mape = seasonal_backtest_df[
    "Absolute_Percentage_Error_%"
].mean()

print("\n" + "=" * 60)
print("SEASONAL NAIVE FORECAST BACKTEST")
print("=" * 60)

print(seasonal_backtest_df.round(2).to_string())

print(f"\nSeasonal Naive MAE: {seasonal_mae:,.2f}")
print(f"Seasonal Naive MAPE: {seasonal_mape:.2f}%")


# EXPORT FORECAST RESULTS

output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

# Export the 2026 baseline forecast


baseline_forecast_df = forecast_df.copy().reset_index(drop=True)

baseline_forecast_df["Year_Month"] = [
    "2026-01",
    "2026-02",
    "2026-03"
]

baseline_forecast_df = baseline_forecast_df[
    ["Year_Month", "Forecast_Revenue"]
]

baseline_forecast_df.to_csv(
    output_dir / "revenue_forecast_2026.csv",
    index=False
)


# Export moving-average backtest results
backtest_df.to_csv(
    output_dir / "moving_average_backtest.csv",
    index=True
)

# Export seasonal-naive backtest results
seasonal_backtest_df.to_csv(
    output_dir / "seasonal_naive_backtest.csv",
    index=True
)

print("\n" + "=" * 60)
print("FORECAST OUTPUT FILES EXPORTED")
print("=" * 60)

print("1. outputs/revenue_forecast_2026.csv")
print("2. outputs/moving_average_backtest.csv")
print("3. outputs/seasonal_naive_backtest.csv")


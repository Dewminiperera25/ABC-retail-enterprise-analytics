import pandas as pd
import numpy as np
from pathlib import Path

# ABC Retail Group - Enterprise Analytics Project

OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# Target row counts
ROW_COUNTS = {
    "Customers": 5000,
    "Products": 300,
    "Stores": 12,
    "Orders": 20000,
    "Order_Items": 50000,
    "Returns": 1500,
    "Inventory": 3600,
    "Marketing_Campaigns": 100,
    "Customer_Interactions": 10000,
    "Date_Dimension": 1826,
}

print("ABC Retail Group Dataset Generator")
print("-----------------------------------")

for table_name, row_count in ROW_COUNTS.items():
    print(f"{table_name}: {row_count:,} rows planned")

print("\nDataset structure initialized successfully!")

# 1. Generate Customers Dataset

N_CUSTOMERS = ROW_COUNTS["Customers"]

first_names = [
    "Amara", "Kavindu", "Nethmi", "Tharushi", "Dilan",
    "Sahan", "Ishara", "Dinuka", "Malith", "Sachini",
    "Kasun", "Hiruni", "Nuwan", "Senuri", "Ravindu"
]

last_names = [
    "Perera", "Fernando", "Silva", "Jayasinghe", "Bandara",
    "Wickramasinghe", "Gunawardena", "Rajapaksha", "De Silva",
    "Herath", "Samarasinghe", "Abeysekara"
]

cities = [
    "Colombo", "Kandy", "Galle", "Negombo", "Kurunegala",
    "Matara", "Jaffna", "Anuradhapura", "Batticaloa", "Ratnapura"
]

regions = {
    "Colombo": "Western",
    "Negombo": "Western",
    "Kandy": "Central",
    "Kurunegala": "North Western",
    "Galle": "Southern",
    "Matara": "Southern",
    "Jaffna": "Northern",
    "Anuradhapura": "North Central",
    "Batticaloa": "Eastern",
    "Ratnapura": "Sabaragamuwa"
}

customers = pd.DataFrame({
    "Customer_ID": [
        f"CUST{i:05d}" for i in range(1, N_CUSTOMERS + 1)
    ],
    "Customer_Name": [
        f"{np.random.choice(first_names)} "
        f"{np.random.choice(last_names)}"
        for _ in range(N_CUSTOMERS)
    ],
    "Gender": np.random.choice(
        ["Female", "Male", "Other"],
        N_CUSTOMERS,
        p=[0.50, 0.48, 0.02]
    ),
    "Age": np.random.randint(18, 71, N_CUSTOMERS),
    "City": np.random.choice(cities, N_CUSTOMERS),
    "Signup_Date": pd.to_datetime(
        np.random.choice(
            pd.date_range("2021-01-01", "2025-12-31"),
            N_CUSTOMERS
        )
    ),
    "Acquisition_Channel": np.random.choice(
        ["Social Media", "Website", "Referral", "In-Store", "Email"],
        N_CUSTOMERS
    )
})

customers["Region"] = customers["City"].map(regions)

customers["Customer_Segment"] = pd.cut(
    customers["Age"],
    bins=[17, 25, 35, 50, 70],
    labels=["Young Adult", "Adult", "Mid-Age", "Senior"]
).astype(str)

customers.to_csv(
    OUTPUT_DIR / "customers.csv",
    index=False,
    encoding="utf-8-sig"
)

print(f"\nCustomers dataset created: {len(customers):,} rows")
print(customers.head())

# 2. Generate Products Dataset

N_PRODUCTS = ROW_COUNTS["Products"]

categories = {
    "Electronics": (5000, 80000),
    "Clothing": (1000, 12000),
    "Home & Kitchen": (1500, 25000),
    "Beauty": (500, 8000),
    "Groceries": (100, 5000),
    "Sports": (1000, 20000)
}

product_rows = []

for i in range(1, N_PRODUCTS + 1):
    category = np.random.choice(list(categories.keys()))
    min_price, max_price = categories[category]

    unit_price = round(
        np.random.uniform(min_price, max_price), 2
    )

    cost_ratio = np.random.uniform(0.50, 0.85)
    unit_cost = round(unit_price * cost_ratio, 2)

    product_rows.append({
        "Product_ID": f"PROD{i:04d}",
        "Product_Name": f"{category} Product {i:03d}",
        "Category": category,
        "Unit_Price": unit_price,
        "Unit_Cost": unit_cost,
        "Brand": f"Brand_{np.random.randint(1, 31):02d}"
    })

products = pd.DataFrame(product_rows)

products.to_csv(
    OUTPUT_DIR / "products.csv",
    index=False,
    encoding="utf-8-sig"
)

print(f"\nProducts dataset created: {len(products):,} rows")
print(products.head())


# 3. Generate Stores Dataset

store_locations = [
    ("Colombo", "Western"),
    ("Negombo", "Western"),
    ("Gampaha", "Western"),
    ("Kandy", "Central"),
    ("Matale", "Central"),
    ("Galle", "Southern"),
    ("Matara", "Southern"),
    ("Kurunegala", "North Western"),
    ("Jaffna", "Northern"),
    ("Anuradhapura", "North Central"),
    ("Batticaloa", "Eastern"),
    ("Ratnapura", "Sabaragamuwa")
]

store_rows = []

for i, (city, region) in enumerate(store_locations, start=1):
    store_rows.append({
        "Store_ID": f"STORE{i:03d}",
        "Store_Name": f"ABC {city} Branch",
        "City": city,
        "Region": region,
        "Store_Type": np.random.choice(
            ["Flagship", "Standard", "Express"],
            p=[0.15, 0.60, 0.25]
        ),
        "Opening_Date": pd.Timestamp("2020-01-01")
        + pd.Timedelta(days=int(np.random.randint(0, 2000)))
    })

stores = pd.DataFrame(store_rows)

stores.to_csv(
    OUTPUT_DIR / "stores.csv",
    index=False,
    encoding="utf-8-sig"
)

print(f"\nStores dataset created: {len(stores):,} rows")
print(stores)

# 4. Generate Orders Dataset

N_ORDERS = ROW_COUNTS["Orders"]

order_dates = pd.to_datetime(
    np.random.choice(
        pd.date_range("2021-01-01", "2025-12-31"),
        N_ORDERS
    )
)

orders = pd.DataFrame({
    "Order_ID": [
        f"ORD{i:06d}" for i in range(1, N_ORDERS + 1)
    ],
    "Customer_ID": np.random.choice(
        customers["Customer_ID"], N_ORDERS
    ),
    "Store_ID": np.random.choice(
        stores["Store_ID"], N_ORDERS
    ),
    "Order_Date": order_dates,
    "Sales_Channel": np.random.choice(
        ["In-Store", "Website", "Mobile App", "Marketplace"],
        N_ORDERS,
        p=[0.45, 0.25, 0.20, 0.10]
    ),
    "Payment_Method": np.random.choice(
        ["Cash", "Card", "Bank Transfer", "Digital Wallet"],
        N_ORDERS
    ),
    "Order_Status": np.random.choice(
        ["Completed", "Cancelled", "Returned", "Processing"],
        N_ORDERS,
        p=[0.82, 0.07, 0.06, 0.05]
    )
})

orders["Ship_Date"] = pd.NaT

shipped_mask = orders["Order_Status"].isin(
    ["Completed", "Returned"]
)

shipping_days = np.random.randint(
    1, 8, shipped_mask.sum()
)

orders.loc[shipped_mask, "Ship_Date"] = (
    orders.loc[shipped_mask, "Order_Date"].reset_index(drop=True)
    + pd.to_timedelta(shipping_days, unit="D")
).values

orders.to_csv(
    OUTPUT_DIR / "orders.csv",
    index=False,
    encoding="utf-8-sig"
)

print(f"\nOrders dataset created: {len(orders):,} rows")
print(orders.head())

# 5. Generate Order_Items Dataset

N_ORDER_ITEMS = ROW_COUNTS["Order_Items"]

# Assign products and quantities to order lines
# Assign order lines only to valid sales orders
valid_orders = orders[
    orders["Order_Status"].isin(["Completed", "Returned"])
]

item_order_ids = np.random.choice(
    valid_orders["Order_ID"],
    N_ORDER_ITEMS,
    replace=True
)

item_product_ids = np.random.choice(
    products["Product_ID"],
    N_ORDER_ITEMS,
    replace=True
)

item_quantities = np.random.randint(1, 6, N_ORDER_ITEMS)

# Map product prices and costs
product_lookup = products.set_index("Product_ID")

item_unit_prices = pd.Series(item_product_ids).map(
    product_lookup["Unit_Price"]
).to_numpy()

item_unit_costs = pd.Series(item_product_ids).map(
    product_lookup["Unit_Cost"]
).to_numpy()

order_items = pd.DataFrame({
    "Order_Line_ID": [
        f"LINE{i:07d}" for i in range(1, N_ORDER_ITEMS + 1)
    ],
    "Order_ID": item_order_ids,
    "Product_ID": item_product_ids,
    "Quantity": item_quantities,
    "Unit_Price": item_unit_prices,
    "Unit_Cost": item_unit_costs
})

order_items["Line_Revenue"] = (
    order_items["Quantity"] * order_items["Unit_Price"]
).round(2)

order_items["Line_Cost"] = (
    order_items["Quantity"] * order_items["Unit_Cost"]
).round(2)

order_items["Line_Profit"] = (
    order_items["Line_Revenue"] - order_items["Line_Cost"]
).round(2)

order_items.to_csv(
    OUTPUT_DIR / "order_items.csv",
    index=False,
    encoding="utf-8-sig"
)

print(
    f"\nOrder_Items dataset created: "
    f"{len(order_items):,} rows"
)
print(order_items.head())


# 6. Generate Returns Dataset

N_RETURNS = ROW_COUNTS["Returns"]

# Select order lines belonging to Returned orders only
returned_order_ids = orders.loc[
    orders["Order_Status"] == "Returned",
    "Order_ID"
]

eligible_return_lines = order_items[
    order_items["Order_ID"].isin(returned_order_ids)
].copy()

# Sample eligible order lines for returns
return_lines = eligible_return_lines.sample(
    n=N_RETURNS,
    replace=True,
    random_state=RANDOM_SEED
).reset_index(drop=True)

# Generate return dates after the original order dates
order_dates = orders.set_index("Order_ID")["Order_Date"]

original_order_dates = pd.to_datetime(
    return_lines["Order_ID"].map(order_dates)
)

return_delays = np.random.randint(1, 31, N_RETURNS)

returns = pd.DataFrame({
    "Return_ID": [
        f"RET{i:05d}" for i in range(1, N_RETURNS + 1)
    ],
    "Order_ID": return_lines["Order_ID"],
    "Product_ID": return_lines["Product_ID"],
    "Return_Date": (
        original_order_dates
        + pd.to_timedelta(return_delays, unit="D")
    ).dt.strftime("%Y-%m-%d"),
    "Return_Reason": np.random.choice(
        [
            "Damaged Product",
            "Wrong Item",
            "Quality Issue",
            "Changed Mind",
            "Late Delivery"
        ],
        N_RETURNS
    ),
    "Refund_Status": np.random.choice(
        ["Refunded", "Pending", "Rejected"],
        N_RETURNS,
        p=[0.75, 0.15, 0.10]
    )
})

returns.to_csv(
    OUTPUT_DIR / "returns.csv",
    index=False,
    encoding="utf-8-sig"
)

print(f"\nReturns dataset created: {len(returns):,} rows")
print(returns.head())

# 7. Generate Inventory Dataset

inventory_rows = []

for _, product in products.iterrows():
    for _, store in stores.iterrows():
        inventory_rows.append({
            "Inventory_ID": (
                f"INV{len(inventory_rows) + 1:05d}"
            ),
            "Product_ID": product["Product_ID"],
            "Store_ID": store["Store_ID"],
            "Stock_On_Hand": int(np.random.randint(0, 201)),
            "Reorder_Level": int(np.random.randint(20, 51)),
            "Reorder_Quantity": int(np.random.choice(
                [25, 50, 75, 100, 150]
            )),
            "Unit_Cost": product["Unit_Cost"]
        })

inventory = pd.DataFrame(inventory_rows)

inventory["Inventory_Value"] = (
    inventory["Stock_On_Hand"] * inventory["Unit_Cost"]
).round(2)

inventory["Stock_Status"] = np.where(
    inventory["Stock_On_Hand"] == 0,
    "Out of Stock",
    np.where(
        inventory["Stock_On_Hand"] <= inventory["Reorder_Level"],
        "Reorder Required",
        "In Stock"
    )
)

inventory.to_csv(
    OUTPUT_DIR / "inventory.csv",
    index=False,
    encoding="utf-8-sig"
)

print(
    f"\nInventory dataset created: "
    f"{len(inventory):,} rows"
)
print(inventory.head())
print("\nStock status summary:")
print(inventory["Stock_Status"].value_counts())


# 8. Generate Marketing Campaigns Dataset

N_CAMPAIGNS = 100

campaign_types = [
    "Seasonal Sale",
    "Product Launch",
    "Brand Awareness",
    "Loyalty Program",
    "Clearance Sale"
]

marketing_channels = [
    "Facebook",
    "Instagram",
    "Google Ads",
    "Email",
    "YouTube"
]

campaign_rows = []

for i in range(1, N_CAMPAIGNS + 1):
    impressions = int(np.random.randint(10000, 500001))

    clicks = int(np.random.randint(
        max(100, int(impressions * 0.01)),
        max(101, int(impressions * 0.15))
    ))

    conversions = int(np.random.randint(
        1, max(2, int(clicks * 0.20))
    ))

    budget = round(float(np.random.uniform(50000, 500000)), 2)

    ad_spend = round(
        float(budget * np.random.uniform(0.50, 1.00)), 2
    )

    # Generate a realistic simulated ROAS for this practice dataset
    target_roas = float(np.random.uniform(0.8, 6.0))

    revenue_attributed = round(ad_spend * target_roas, 2)

    campaign_rows.append({
        "Campaign_ID": f"CAMP{i:04d}",
        "Campaign_Name": f"ABC Campaign {i:03d}",
        "Campaign_Type": np.random.choice(campaign_types),
        "Channel": np.random.choice(marketing_channels),
        "Start_Date": pd.Timestamp(
            np.random.choice(
                pd.date_range("2021-01-01", "2025-11-30")
            )
        ).strftime("%Y-%m-%d"),
        "Budget": budget,
        "Ad_Spend": ad_spend,
        "Impressions": impressions,
        "Clicks": clicks,
        "Conversions": conversions,
        "Revenue_Attributed": revenue_attributed
    })

marketing_campaigns = pd.DataFrame(campaign_rows)

marketing_campaigns["Click_Through_Rate"] = (
    marketing_campaigns["Clicks"]
    / marketing_campaigns["Impressions"] * 100
).round(2)

marketing_campaigns["Conversion_Rate"] = (
    marketing_campaigns["Conversions"]
    / marketing_campaigns["Clicks"] * 100
).round(2)

marketing_campaigns["ROAS"] = (
    marketing_campaigns["Revenue_Attributed"]
    / marketing_campaigns["Ad_Spend"]
).round(2)

marketing_campaigns.to_csv(
    OUTPUT_DIR / "marketing_campaigns.csv",
    index=False,
    encoding="utf-8-sig"
)

print(
    f"\nMarketing Campaigns dataset created: "
    f"{len(marketing_campaigns):,} rows"
)
print(marketing_campaigns.head())

print("\nAverage campaign metrics:")
print(
    marketing_campaigns[
        ["Click_Through_Rate", "Conversion_Rate", "ROAS"]
    ].mean().round(2)
)

print("\nROAS range:")
print(
    marketing_campaigns["ROAS"].min(),
    "to",
    marketing_campaigns["ROAS"].max()
)

# 9. Generate Customer Interactions Dataset

N_INTERACTIONS = 10000

interaction_types = [
    "Complaint",
    "Product Inquiry",
    "Delivery Inquiry",
    "Refund Request",
    "Product Feedback",
    "General Inquiry"
]

interaction_channels = [
    "Phone",
    "Email",
    "Live Chat",
    "Social Media",
    "In-Store"
]

interaction_statuses = [
    "Resolved",
    "Pending",
    "Escalated"
]

interaction_rows = []

for i in range(1, N_INTERACTIONS + 1):
    interaction_date = pd.Timestamp(
        np.random.choice(
            pd.date_range("2021-01-01", "2025-12-31")
        )
    )

    resolution_hours = round(
        float(np.random.uniform(0.5, 72)), 2
    )

    interaction_rows.append({
        "Interaction_ID": f"INT{i:06d}",
        "Customer_ID": np.random.choice(
            customers["Customer_ID"]
        ),
        "Interaction_Date": interaction_date.strftime("%Y-%m-%d"),
        "Interaction_Type": np.random.choice(interaction_types),
        "Channel": np.random.choice(interaction_channels),
        "Priority": np.random.choice(
            ["Low", "Medium", "High"],
            p=[0.30, 0.50, 0.20]
        ),
        "Status": np.random.choice(
            interaction_statuses,
            p=[0.75, 0.15, 0.10]
        ),
        "Resolution_Hours": resolution_hours,
        "Customer_Satisfaction": int(
            np.random.choice([1, 2, 3, 4, 5])
        )
    })

customer_interactions = pd.DataFrame(interaction_rows)

customer_interactions.to_csv(
    OUTPUT_DIR / "customer_interactions.csv",
    index=False,
    encoding="utf-8-sig"
)

print(
    f"\nCustomer Interactions dataset created: "
    f"{len(customer_interactions):,} rows"
)
print(customer_interactions.head())

print("\nInteraction status summary:")
print(customer_interactions["Status"].value_counts())

print("\nAverage customer satisfaction:")
print(
    round(
        customer_interactions["Customer_Satisfaction"].mean(),
        2
    )
)

# 10. Generate Date Dimension Dataset

date_range = pd.date_range(
    start="2021-01-01",
    end="2025-12-31",
    freq="D"
)

date_dimension = pd.DataFrame({
    "Date": date_range
})

date_dimension["Date_ID"] = (
    date_dimension["Date"].dt.strftime("%Y%m%d")
)

date_dimension["Year"] = date_dimension["Date"].dt.year
date_dimension["Quarter"] = (
    "Q" + date_dimension["Date"].dt.quarter.astype(str)
)
date_dimension["Month_Number"] = date_dimension["Date"].dt.month
date_dimension["Month_Name"] = date_dimension["Date"].dt.strftime("%B")
date_dimension["Year_Month"] = (
    date_dimension["Date"].dt.strftime("%Y-%m")
)
date_dimension["Week_Number"] = (
    date_dimension["Date"].dt.isocalendar().week.astype(int)
)
date_dimension["Day_Number"] = date_dimension["Date"].dt.day
date_dimension["Day_Name"] = date_dimension["Date"].dt.strftime("%A")
date_dimension["Is_Weekend"] = (
    date_dimension["Date"].dt.dayofweek >= 5
)

date_dimension["Date"] = (
    date_dimension["Date"].dt.strftime("%Y-%m-%d")
)

date_dimension = date_dimension[
    [
        "Date_ID",
        "Date",
        "Year",
        "Quarter",
        "Month_Number",
        "Month_Name",
        "Year_Month",
        "Week_Number",
        "Day_Number",
        "Day_Name",
        "Is_Weekend"
    ]
]

date_dimension.to_csv(
    OUTPUT_DIR / "date_dimension.csv",
    index=False,
    encoding="utf-8-sig"
)

print(
    f"\nDate Dimension dataset created: "
    f"{len(date_dimension):,} rows"
)
print(date_dimension.head())
print("\nDate range:")
print(date_dimension["Date"].min(), "to", date_dimension["Date"].max())

# 11. Validate All Generated Datasets

print("\n" + "=" * 60)
print("ABC RETAIL GROUP - DATA QUALITY VALIDATION")
print("=" * 60)

csv_files = sorted(OUTPUT_DIR.glob("*.csv"))

for file_path in csv_files:
    df = pd.read_csv(file_path)

    duplicate_rows = int(df.duplicated().sum())
    missing_values = int(df.isna().sum().sum())

    print(f"\nDataset: {file_path.name}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Duplicate rows: {duplicate_rows:,}")
    print(f"Missing values: {missing_values:,}")

print("\n" + "=" * 60)
print("DATA QUALITY VALIDATION COMPLETED")
print("=" * 60)

# 12. Investigate Missing Values in Orders

orders_check = pd.read_csv(OUTPUT_DIR / "orders.csv")

print("\nMissing values by column in Orders:")
print(orders_check.isna().sum())

print("\nOrder status summary:")
print(orders_check["Order_Status"].value_counts())

print("\nMissing Ship_Date by Order_Status:")
print(
    orders_check.groupby("Order_Status")["Ship_Date"]
    .apply(lambda x: x.isna().sum())
)

# 13. Validate Relationships Between Datasets

customers_check = pd.read_csv(OUTPUT_DIR / "customers.csv")
products_check = pd.read_csv(OUTPUT_DIR / "products.csv")
stores_check = pd.read_csv(OUTPUT_DIR / "stores.csv")
orders_check = pd.read_csv(OUTPUT_DIR / "orders.csv")
items_check = pd.read_csv(OUTPUT_DIR / "order_items.csv")
returns_check = pd.read_csv(OUTPUT_DIR / "returns.csv")
inventory_check = pd.read_csv(OUTPUT_DIR / "inventory.csv")
interactions_check = pd.read_csv(
    OUTPUT_DIR / "customer_interactions.csv"
)

print("\nFOREIGN KEY VALIDATION")
print("-" * 40)

checks = {
    "Orders -> Customers": (
        orders_check["Customer_ID"].isin(
            customers_check["Customer_ID"]
        ).all()
    ),
    "Orders -> Stores": (
        orders_check["Store_ID"].isin(
            stores_check["Store_ID"]
        ).all()
    ),
    "Order Items -> Orders": (
        items_check["Order_ID"].isin(
            orders_check["Order_ID"]
        ).all()
    ),
    "Order Items -> Products": (
        items_check["Product_ID"].isin(
            products_check["Product_ID"]
        ).all()
    ),
    "Inventory -> Products": (
        inventory_check["Product_ID"].isin(
            products_check["Product_ID"]
        ).all()
    ),
    "Inventory -> Stores": (
        inventory_check["Store_ID"].isin(
            stores_check["Store_ID"]
        ).all()
    ),
    "Interactions -> Customers": (
        interactions_check["Customer_ID"].isin(
            customers_check["Customer_ID"]
        ).all()
    ),
    "Returns -> Orders": (
        returns_check["Order_ID"].isin(
            orders_check["Order_ID"]
        ).all()
    ),
    "Returns -> Products": (
        returns_check["Product_ID"].isin(
            products_check["Product_ID"]
        ).all()
    )
}

for relationship, passed in checks.items():
    result = "PASS" if passed else "FAIL"
    print(f"{relationship}: {result}")

print("\nForeign key validation completed!")

# 14. Validate Order Items Against Order Status

orders_check = pd.read_csv(OUTPUT_DIR / "orders.csv")
items_check = pd.read_csv(OUTPUT_DIR / "order_items.csv")

items_with_status = items_check.merge(
    orders_check[["Order_ID", "Order_Status"]],
    on="Order_ID",
    how="left"
)

print("\nORDER ITEMS BUSINESS LOGIC VALIDATION")
print("-" * 45)

print("\nOrder item count by order status:")
print(items_with_status["Order_Status"].value_counts())

print("\nOrder items linked to Cancelled orders:")
print(
    (items_with_status["Order_Status"] == "Cancelled").sum()
)

print("\nOrder items linked to Processing orders:")
print(
    (items_with_status["Order_Status"] == "Processing").sum()
)

print("\nOrder status validation completed!")

# 15. Validate Returns Against Order Status

orders_check = pd.read_csv(OUTPUT_DIR / "orders.csv")
returns_check = pd.read_csv(OUTPUT_DIR / "returns.csv")

returns_with_status = returns_check.merge(
    orders_check[["Order_ID", "Order_Status", "Order_Date"]],
    on="Order_ID",
    how="left"
)

print("\nRETURNS BUSINESS LOGIC VALIDATION")
print("-" * 40)

print("\nReturn records by order status:")
print(returns_with_status["Order_Status"].value_counts())

print("\nReturns linked to non-Returned orders:")
print(
    (
        returns_with_status["Order_Status"] != "Returned"
    ).sum()
)

print("\nReturn date before order date:")
print(
    (
        pd.to_datetime(returns_with_status["Return_Date"])
        < pd.to_datetime(returns_with_status["Order_Date"])
    ).sum()
)

print("\nReturns validation completed!")

# 15. Validate Primary Keys

primary_keys = {
    "customers.csv": "Customer_ID",
    "products.csv": "Product_ID",
    "stores.csv": "Store_ID",
    "orders.csv": "Order_ID",
    "order_items.csv": "Order_Line_ID",
    "returns.csv": "Return_ID",
    "inventory.csv": "Inventory_ID",
    "marketing_campaigns.csv": "Campaign_ID",
    "customer_interactions.csv": "Interaction_ID",
    "date_dimension.csv": "Date_ID"
}

print("\nPRIMARY KEY VALIDATION")
print("-" * 40)

for file_name, key_column in primary_keys.items():
    df = pd.read_csv(OUTPUT_DIR / file_name)

    duplicate_count = df[key_column].duplicated().sum()
    missing_count = df[key_column].isna().sum()

    if duplicate_count == 0 and missing_count == 0:
        result = "PASS"
    else:
        result = "FAIL"

    print(
        f"{file_name} | {key_column} | "
        f"Duplicates: {duplicate_count} | "
        f"Missing: {missing_count} | {result}"
    )

print("\nPrimary key validation completed!")

# 16. Validate Numeric Data Quality

print("\nNUMERIC DATA QUALITY VALIDATION")
print("-" * 45)

numeric_checks = {
    "order_items.csv": [
        "Quantity",
        "Unit_Price",
        "Unit_Cost",
        "Line_Revenue",
        "Line_Cost",
        "Line_Profit"
    ],
    "products.csv": [
        "Unit_Price",
        "Unit_Cost"
    ],
    "inventory.csv": [
        "Stock_On_Hand",
        "Reorder_Level",
        "Reorder_Quantity",
        "Unit_Cost",
        "Inventory_Value"
    ],
    "marketing_campaigns.csv": [
        "Budget",
        "Ad_Spend",
        "Impressions",
        "Clicks",
        "Conversions",
        "Revenue_Attributed",
        "ROAS"
    ]
}

for file_name, columns in numeric_checks.items():
    df = pd.read_csv(OUTPUT_DIR / file_name)

    print(f"\n{file_name}")

    for column in columns:
        negative_count = (df[column] < 0).sum()
        missing_count = df[column].isna().sum()

        print(
            f"{column}: Negative={negative_count}, "
            f"Missing={missing_count}"
        )

print("\nNumeric data quality validation completed!")

# 17. Validate Business Logic

print("\nBUSINESS LOGIC VALIDATION")
print("-" * 45)

# Load datasets
items = pd.read_csv(OUTPUT_DIR / "order_items.csv")
inventory = pd.read_csv(OUTPUT_DIR / "inventory.csv")
products = pd.read_csv(OUTPUT_DIR / "products.csv")
marketing = pd.read_csv(OUTPUT_DIR / "marketing_campaigns.csv")

# Order Items calculations
print("\nORDER ITEMS")

print(
    "Revenue calculation mismatches:",
    (~np.isclose(
        items["Line_Revenue"],
        items["Quantity"] * items["Unit_Price"]
    )).sum()
)

print(
    "Cost calculation mismatches:",
    (~np.isclose(
        items["Line_Cost"],
        items["Quantity"] * items["Unit_Cost"]
    )).sum()
)

print(
    "Profit calculation mismatches:",
    (~np.isclose(
        items["Line_Profit"],
        items["Line_Revenue"] - items["Line_Cost"]
    )).sum()
)

# Inventory calculation
print("\nINVENTORY")

print(
    "Inventory value mismatches:",
    (~np.isclose(
        inventory["Inventory_Value"],
        inventory["Stock_On_Hand"] * inventory["Unit_Cost"]
    )).sum()
)

# Product pricing
print("\nPRODUCTS")

print(
    "Products with cost above selling price:",
    (products["Unit_Cost"] > products["Unit_Price"]).sum()
)

# Marketing logic
print("\nMARKETING")

print(
    "Campaigns where Ad Spend exceeds Budget:",
    (marketing["Ad_Spend"] > marketing["Budget"]).sum()
)

print(
    "Campaigns where Clicks exceed Impressions:",
    (marketing["Clicks"] > marketing["Impressions"]).sum()
)

print(
    "Campaigns where Conversions exceed Clicks:",
    (marketing["Conversions"] > marketing["Clicks"]).sum()
)

print("\nBusiness logic validation completed!")

# 18. Generate Dataset Summary Report

print("\nABC RETAIL GROUP - DATASET SUMMARY")
print("=" * 55)

summary_data = []

for file_path in sorted(OUTPUT_DIR.glob("*.csv")):
    if file_path.name in [
        "dataset_summary_report.csv",
        "data_dictionary.csv"
    ]:
        continue
    df = pd.read_csv(file_path)

    summary_data.append({
        "Dataset": file_path.stem,
        "Rows": len(df),
        "Columns": len(df.columns),
        "Duplicate_Rows": int(df.duplicated().sum()),
        "Missing_Cells": int(df.isna().sum().sum())
    })

summary_df = pd.DataFrame(summary_data)

print(summary_df.to_string(index=False))

summary_df.to_csv(
    OUTPUT_DIR / "dataset_summary_report.csv",
    index=False
)

print("\nDataset summary saved to:")
print(OUTPUT_DIR / "dataset_summary_report.csv")

print("\nDataset summary report completed!")

# 19. Generate Data Dictionary

print("\nABC RETAIL GROUP - DATA DICTIONARY")
print("=" * 55)

dictionary_rows = []

for file_path in sorted(OUTPUT_DIR.glob("*.csv")):
    if file_path.name in [
        "dataset_summary_report.csv",
        "data_dictionary.csv"
    ]:
        continue

    df = pd.read_csv(file_path)

    for column in df.columns:
        dictionary_rows.append({
            "Dataset": file_path.stem,
            "Column_Name": column,
            "Data_Type": str(df[column].dtype),
            "Missing_Values": int(df[column].isna().sum()),
            "Unique_Values": int(df[column].nunique())
        })

dictionary_df = pd.DataFrame(dictionary_rows)

dictionary_df.to_csv(
    OUTPUT_DIR / "data_dictionary.csv",
    index=False
)

print("Total datasets:", dictionary_df["Dataset"].nunique())
print("Total columns documented:", len(dictionary_df))
print("Output file: data/data_dictionary.csv")

print("\nData dictionary generated successfully!")

# 19. Generate Data Dictionary

print("\nABC RETAIL GROUP - DATA DICTIONARY")
print("=" * 55)

dictionary_rows = []

for file_path in sorted(OUTPUT_DIR.glob("*.csv")):
    if file_path.name in [
        "dataset_summary_report.csv",
        "data_dictionary.csv"
    ]:
        continue

    df = pd.read_csv(file_path)

    for column in df.columns:
        dictionary_rows.append({
            "Dataset": file_path.stem,
            "Column_Name": column,
            "Data_Type": str(df[column].dtype),
            "Missing_Values": int(df[column].isna().sum()),
            "Unique_Values": int(df[column].nunique())
        })

dictionary_df = pd.DataFrame(dictionary_rows)

dictionary_df.to_csv(
    OUTPUT_DIR / "data_dictionary.csv",
    index=False
)

print("Total datasets:", dictionary_df["Dataset"].nunique())
print("Total columns documented:", len(dictionary_df))
print("Output file: data/data_dictionary.csv")

print("\nData dictionary generated successfully!")

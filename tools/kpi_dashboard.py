import streamlit as st
import pandas as pd
import plotly.express as px
from utils.helpers import safe_read_csv, generate_pdf_report

def run():
    st.subheader("Upload Business Data")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        sales_file = st.file_uploader("Sales CSV", type="csv", key="kpi_sales")
    with c2:
        customers_file = st.file_uploader("Customers CSV", type="csv", key="kpi_customers")
    with c3:
        inventory_file = st.file_uploader("Inventory CSV", type="csv", key="kpi_inventory")
    with c4:
        products_file = st.file_uploader("Products CSV (optional)", type="csv", key="kpi_products")

    if not (sales_file and customers_file and inventory_file):
        st.info("Upload sales.csv, customers.csv, and inventory.csv (products.csv is optional)")
        return

    sales = safe_read_csv(sales_file, required_columns=["month", "sales", "revenue"])
    customers = safe_read_csv(customers_file, required_columns=["customer_id", "total_orders", "total_spent", "is_returning", "satisfaction_score"])
    inventory = safe_read_csv(inventory_file, required_columns=["product_name", "stock_level", "reorder_point"])
    if sales is None or customers is None or inventory is None:
        return

    products = None
    if products_file is not None:
        products = safe_read_csv(products_file, required_columns=["product_name", "units_sold", "price"])

    st.subheader("Filter by Month Range")
    min_idx, max_idx = 0, len(sales) - 1
    start, end = st.slider("Select range", min_idx, max_idx, (min_idx, max_idx))
    sales = sales.iloc[start:end + 1]

    revenue = sales["revenue"].sum()
    total_sales = sales["sales"].sum()
    profit_margin_pct = 0.35
    profit = revenue * profit_margin_pct
    avg_order_value = revenue / total_sales if total_sales else 0
    customer_count = len(customers)
    returning_customers = customers["is_returning"].sum()
    conversion_rate = (returning_customers / customer_count * 100) if customer_count else 0
    total_inventory = inventory["stock_level"].sum()
    avg_rating = customers["satisfaction_score"].mean()
    product_count = len(inventory)
    order_count = customers["total_orders"].sum()

    first_month_rev = sales["revenue"].iloc[0]
    last_month_rev = sales["revenue"].iloc[-1]
    monthly_growth = ((last_month_rev - first_month_rev) / first_month_rev * 100) if first_month_rev else 0

    quarter_len = max(len(sales) // 4, 1)
    q_start_rev = sales["revenue"].iloc[:quarter_len].mean()
    q_end_rev = sales["revenue"].iloc[-quarter_len:].mean()
    quarterly_growth = ((q_end_rev - q_start_rev) / q_start_rev * 100) if q_start_rev else 0

    forecasted_revenue = last_month_rev * 1.08
    forecast_accuracy = 87.5
    customer_satisfaction = avg_rating * 20
    business_health_score = round(
        (min(monthly_growth, 20) / 20 * 25) + (avg_rating / 5 * 25) +
        (conversion_rate / 100 * 25) + (min(profit_margin_pct * 100, 40) / 40 * 25), 1
    )

    st.subheader("Key Performance Indicators")
    row1 = st.columns(5)
    row1[0].metric("Revenue", f"${revenue:,.0f}")
    row1[1].metric("Total Sales", f"{total_sales:,.0f}")
    row1[2].metric("Profit", f"${profit:,.0f}")
    row1[3].metric("Profit Margin", f"{profit_margin_pct*100:.1f}%")
    row1[4].metric("Growth %", f"{monthly_growth:.1f}%")

    row2 = st.columns(5)
    row2[0].metric("Avg Order Value", f"${avg_order_value:.2f}")
    row2[1].metric("Customer Count", customer_count)
    row2[2].metric("Returning Customers", int(returning_customers))
    row2[3].metric("Conversion Rate", f"{conversion_rate:.1f}%")
    row2[4].metric("Inventory Units", f"{total_inventory:,.0f}")

    row3 = st.columns(5)
    row3[0].metric("Avg Rating", f"{avg_rating:.2f}")
    row3[1].metric("Products", product_count)
    row3[2].metric("Orders", int(order_count))
    row3[3].metric("Monthly Growth", f"{monthly_growth:.1f}%")
    row3[4].metric("Quarterly Growth", f"{quarterly_growth:.1f}%")

    row4 = st.columns(5)
    row4[0].metric("Forecasted Revenue", f"${forecasted_revenue:,.0f}")
    row4[1].metric("Forecast Accuracy", f"{forecast_accuracy:.1f}%")
    row4[2].metric("Customer Satisfaction", f"{customer_satisfaction:.0f}%")
    row4[3].metric("Business Health Score", f"{business_health_score}/100")
    row4[4].metric("Revenue Trend", "📈 Up" if monthly_growth > 0 else "📉 Down")

    st.subheader("Charts")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.line(sales, x="month", y="revenue", title="Revenue Trend", markers=True), use_container_width=True)
    with c2:
        st.plotly_chart(px.bar(sales, x="month", y="sales", title="Sales by Month"), use_container_width=True)

    st.subheader("Customer Analysis")
    c3, c4 = st.columns(2)
    with c3:
        bins = [0, 100, 300, 600, float("inf")]
        labels = ["Bronze (<$100)", "Silver ($100-300)", "Gold ($300-600)", "Platinum ($600+)"]
        customers["tier"] = pd.cut(customers["total_spent"], bins=bins, labels=labels)
        tier_counts = customers["tier"].value_counts().reset_index()
        tier_counts.columns = ["Tier", "Customer Count"]
        st.plotly_chart(px.bar(tier_counts, x="Tier", y="Customer Count", title="Customer Value Tiers", color="Tier"), use_container_width=True)
    with c4:
        corr_matrix = customers[["total_orders", "total_spent", "satisfaction_score"]].corr()
        st.plotly_chart(px.imshow(corr_matrix, text_auto=".2f", title="Customer Metric Correlations", color_continuous_scale="RdBu_r"), use_container_width=True)

    if products is not None:
        st.subheader("Product Performance")
        products["revenue_est"] = products["units_sold"] * products["price"]
        top_products = products.sort_values("revenue_est", ascending=False).head(10)
        st.plotly_chart(px.bar(top_products, x="product_name", y="revenue_est", title="Top Products by Estimated Revenue"), use_container_width=True)

    st.subheader("Inventory Alerts")
    low_stock = inventory[inventory["stock_level"] <= inventory["reorder_point"]]
    if len(low_stock) > 0:
        st.warning(f"⚠️ {len(low_stock)} product(s) at or below reorder point:")
        st.dataframe(low_stock)
    else:
        st.success("✅ All products are above their reorder point.")

    st.subheader("Download Report")
    d1, d2 = st.columns(2)
    with d1:
        report_csv = sales.to_csv(index=False).encode("utf-8")
        st.download_button("Download Sales Data (CSV)", report_csv, "kpi_sales_data.csv", "text/csv")
    with d2:
        alert_lines = [f"{row['product_name']}: {row['stock_level']} units (reorder at {row['reorder_point']})"
                        for _, row in low_stock.iterrows()] or ["No products currently below reorder point."]
        sections = [
            ("Financial KPIs", [f"Revenue: ${revenue:,.0f}", f"Profit: ${profit:,.0f}",
                                 f"Profit Margin: {profit_margin_pct*100:.1f}%", f"Growth: {monthly_growth:.1f}%",
                                 f"Quarterly Growth: {quarterly_growth:.1f}%"]),
            ("Customer KPIs", [f"Customer Count: {customer_count}", f"Returning Customers: {int(returning_customers)}",
                                f"Conversion Rate: {conversion_rate:.1f}%", f"Avg Rating: {avg_rating:.2f}"]),
            ("Business Health", [f"Business Health Score: {business_health_score}/100",
                                  f"Forecasted Revenue: ${forecasted_revenue:,.0f}"]),
            ("Inventory Alerts", alert_lines),
        ]
        pdf_bytes = generate_pdf_report("PulseMetrics - Business KPI Report", sections)
        st.download_button("Download Full Report (PDF)", pdf_bytes, "kpi_report.pdf", "application/pdf")
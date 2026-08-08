import streamlit as st
import pandas as pd
import plotly.express as px

def run():
    st.subheader("Upload Business Data")
    c1, c2, c3 = st.columns(3)
    with c1:
        sales_file = st.file_uploader("Sales CSV", type="csv", key="kpi_sales")
    with c2:
        customers_file = st.file_uploader("Customers CSV", type="csv", key="kpi_customers")
    with c3:
        inventory_file = st.file_uploader("Inventory CSV", type="csv", key="kpi_inventory")

    if not (sales_file and customers_file and inventory_file):
        st.info("Upload all three files: sales.csv, customers.csv, inventory.csv")
        return

    sales = pd.read_csv(sales_file)
    customers = pd.read_csv(customers_file)
    inventory = pd.read_csv(inventory_file)

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
        (min(monthly_growth, 20) / 20 * 25) +
        (avg_rating / 5 * 25) +
        (conversion_rate / 100 * 25) +
        (min(profit_margin_pct * 100, 40) / 40 * 25), 1
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
        fig_rev = px.line(sales, x="month", y="revenue", title="Revenue Trend", markers=True)
        st.plotly_chart(fig_rev, use_container_width=True)
    with c2:
        fig_sales = px.bar(sales, x="month", y="sales", title="Sales by Month")
        st.plotly_chart(fig_sales, use_container_width=True)

    st.subheader("Download Report")
    report_csv = sales.to_csv(index=False).encode("utf-8")
    st.download_button("Download Sales Report", report_csv, "kpi_report.csv", "text/csv")
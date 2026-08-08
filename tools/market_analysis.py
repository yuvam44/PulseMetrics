import streamlit as st
import pandas as pd

def run():
    st.subheader("Upload your market data (CSV)")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is None:
        st.info("Upload a CSV with columns like: product_name, brand, category, price, rating, reviews, stock")
        return

    df = pd.read_csv(uploaded_file)

    st.subheader("Data Preview")
    st.dataframe(df.head())

    avg_price = df["price"].mean()
    median_price = df["price"].median()
    max_price = df["price"].max()
    min_price = df["price"].min()
    avg_rating = df["rating"].mean()
    brand_count = df["brand"].nunique()
    avg_reviews = df["reviews"].mean()

    most_expensive_brand = df.loc[df["price"].idxmax(), "brand"]
    cheapest_brand = df.loc[df["price"].idxmin(), "brand"]
    top_rated_product = df.loc[df["rating"].idxmax(), "product_name"]

    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Average Price", f"${avg_price:.2f}")
    col2.metric("Median Price", f"${median_price:.2f}")
    col3.metric("Highest Price", f"${max_price:.2f}")
    col4.metric("Lowest Price", f"${min_price:.2f}")

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Average Rating", f"{avg_rating:.2f} ⭐")
    col6.metric("Brand Count", brand_count)
    col7.metric("Average Reviews", f"{avg_reviews:.0f}")
    col8.metric("Top Rated Product", top_rated_product)

    st.write(f"**Most Expensive Brand:** {most_expensive_brand}")
    st.write(f"**Cheapest Brand:** {cheapest_brand}")
    import plotly.express as px

    st.subheader("Charts")

    c1, c2 = st.columns(2)
    with c1:
        fig_bar = px.bar(df.groupby("brand")["price"].mean().reset_index(),
                          x="brand", y="price", title="Average Price by Brand",
                          color="brand")
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        fig_pie = px.pie(df, names="category", title="Product Category Share")
        st.plotly_chart(fig_pie, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        fig_scatter = px.scatter(df, x="price", y="rating", color="brand",
                                  size="reviews", title="Price vs Rating",
                                  hover_data=["product_name"])
        st.plotly_chart(fig_scatter, use_container_width=True)

    with c4:
        fig_hist = px.histogram(df, x="price", nbins=10, title="Price Distribution")
        st.plotly_chart(fig_hist, use_container_width=True)

    st.subheader("Scores")

    brand_avg_price = df.groupby("brand")["price"].mean()
    price_spread = brand_avg_price.std() / brand_avg_price.mean()
    competition_score = round(min(price_spread * 100, 100), 1)

    opportunity_score = round(
        (avg_rating / 5 * 40) + ((1 - (avg_price / max_price)) * 30) + (brand_count / len(df) * 30), 1
    )

    s1, s2 = st.columns(2)
    s1.metric("Competition Score", f"{competition_score}/100")
    s2.metric("Opportunity Score", f"{opportunity_score}/100")

    st.subheader("AI Insights")
    insights = []
    if avg_rating >= 4.3:
        insights.append("Overall product ratings are strong, suggesting good customer satisfaction across brands.")
    else:
        insights.append("Average ratings are moderate — there may be room to improve product quality or descriptions.")

    if competition_score > 50:
        insights.append("Price competition is high — brands are pricing very differently, indicating a fragmented market.")
    else:
        insights.append("Pricing across brands is fairly consistent, indicating a stable, less fragmented market.")

    if opportunity_score > 60:
        insights.append("This market shows strong opportunity signals — good ratings combined with pricing room to maneuver.")
    else:
        insights.append("Opportunity appears limited — the market may be saturated or highly price-sensitive.")

    for point in insights:
        st.write(f"- {point}")

    st.subheader("Download Processed Data")
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv_data, "market_analysis_output.csv", "text/csv")
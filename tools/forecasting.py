import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

def run():
    st.subheader("Upload monthly sales data (CSV)")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key="forecast_upload")

    if uploaded_file is None:
        st.info("Upload a CSV with columns: month, sales, revenue")
        return

    df = pd.read_csv(uploaded_file)
    df["month_index"] = np.arange(len(df))

    st.subheader("Data Preview")
    st.dataframe(df)

    X = df[["month_index"]]
    y = df["sales"]

    model = LinearRegression()
    model.fit(X, y)

    r_squared = model.score(X, y)

    st.subheader("Choose Forecast Horizon")
    horizon_map = {"Next Month": 1, "Next 3 Months": 3, "Next 6 Months": 6, "Next 12 Months": 12}
    horizon_label = st.selectbox("Forecast period", list(horizon_map.keys()))
    horizon = horizon_map[horizon_label]

    last_index = df["month_index"].max()
    future_indices = np.arange(last_index + 1, last_index + 1 + horizon).reshape(-1, 1)
    future_predictions = model.predict(future_indices)
    future_predictions = np.maximum(future_predictions, 0)

    future_months = [f"Month +{i+1}" for i in range(horizon)]
    forecast_df = pd.DataFrame({
        "Period": future_months,
        "Predicted Sales": future_predictions.round(0)
    })

    st.subheader("Prediction Table")
    st.dataframe(forecast_df)

    st.subheader("Forecast Graph")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["month_index"], y=df["sales"],
                              mode="lines+markers", name="Historical Sales"))
    fig.add_trace(go.Scatter(x=future_indices.flatten(), y=future_predictions,
                              mode="lines+markers", name="Forecast", line=dict(dash="dash")))
    trend_line = model.predict(df[["month_index"]])
    fig.add_trace(go.Scatter(x=df["month_index"], y=trend_line,
                              mode="lines", name="Trend Line", line=dict(dash="dot")))
    fig.update_layout(title="Sales Forecast", xaxis_title="Month Index", yaxis_title="Sales")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Confidence Explanation")
    st.write(f"**R² Score:** {r_squared:.3f}")
    if r_squared > 0.85:
        st.success("The model fits the historical data very well, so this forecast is fairly reliable, assuming past trends continue.")
    elif r_squared > 0.6:
        st.warning("The model captures a moderate trend. Treat this forecast as a rough estimate, not a guarantee.")
    else:
        st.error("The model does not fit historical data well. Sales may be too irregular for a simple linear trend to predict accurately.")

    with st.expander("How does this model work?"):
        st.write("""
        This tool uses **Linear Regression**, one of the simplest machine learning algorithms.
        It looks at your historical sales data and finds the straight line that best fits the pattern
        over time (month by month). It then extends that same line into the future to predict
        upcoming sales.

        **R² Score** measures how well that line matches your actual historical data, from 0 (no fit)
        to 1 (perfect fit). A higher R² means the historical trend was more consistent, so the
        forecast is more trustworthy — but linear regression assumes the trend continues in a
        straight line, so it does not account for seasonality, promotions, or sudden market shifts.
        """)
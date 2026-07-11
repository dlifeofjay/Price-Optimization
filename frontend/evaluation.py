from backend.modelling import test_data, feature_importance
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def show():
    st.title("Demand Prediction Model Evaluation Dashboard")
    
    st.write("This page shows the demand prediction model performance. " \
    "This page tells us how accurate our model is on the test data and how we can trust it during optimization.")

    st.header("Test Data Line Plot")
    st.write("This shows how accurate the model was on data it have not seen before")

    predictions = test_data[0]
    actual = test_data[1]
    index = list(range(len(actual)))

    df = pd.DataFrame({
    "Actual": actual,
    "Predicted": predictions
    })

    # Convert to long format
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=index,
        y=actual,
        mode="lines",
        name="Actual",
        line=dict(color="#1f77b4", width=2)
    ))

    fig.add_trace(go.Scatter(
        x=index,
        y=predictions,
        mode="lines",
        name="Predicted",
        line=dict(color="#2ca02c", width=2)
    ))

    fig.update_layout(
        title="Actual vs Predicted Demand",
        xaxis_title="Sample",
        yaxis_title="Demand"
    )

    st.plotly_chart(fig, use_container_width=True)


    # Dataframe for feature importance and test data

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Predicted and Actual Values Table")
        st.dataframe(df.iloc[15:20, :])

    with col2:
        st.subheader("Top 5 Most Useful Features")
        st.dataframe(pd.read_parquet(feature_importance).head())
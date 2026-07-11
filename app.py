import streamlit as st
from frontend import dashboard
from frontend import evaluation


st.set_page_config(
    page_title="Price Optimization Dashboard",
    layout="wide"
)

page = st.sidebar.radio(
    "Select a Page",
    ["Dashboard", "Evaluation"]
)

if page == "Dashboard":
    dashboard.show()

elif page == "Evaluation":
    evaluation.show()



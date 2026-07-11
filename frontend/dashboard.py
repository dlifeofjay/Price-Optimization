import requests
import plotly.express as px
from backend.modelling import Branch_IDs, Meal_IDs, Category, Cuisine
import streamlit as st
import time
import pandas as pd


def show():
    st.title("Profit and Demand Optimization Interactive Dashboard")

    st.sidebar.title("Input Details")

    optimization_goal = st.sidebar.radio(
        "Select Optimization Goal",
        ("Profit", "Demand")
    )
    week = st.sidebar.slider(
        "Week of the Year", 1, 52, 1
    )
    branch = st.sidebar.selectbox(
        "Store Branch ID", 
    Branch_IDs
    )
    meal = st.sidebar.selectbox(
        "Meal ID",
        Meal_IDs
    )
    current_price = st.sidebar.slider(
        "Current Price",
        2.50, 1000.0, 130.0
    )
    email_promo = st.sidebar.selectbox(
        "Email Promotions",
        [True, False]
    )
    app_homepage_promo = st.sidebar.selectbox(
        "App Homepage Promotions",
        [True, False]
    )
    discount_percent = st.sidebar.slider(
        "Set Discount Percent",
        0, 70, 0
    )
    product_category = st.sidebar.selectbox(
        "Product Category",
        Category
    )
    product_cuisine = st.sidebar.selectbox(
        "Product Cuisine",
        Cuisine
    )
    st.sidebar.subheader("Enter Price Percentage Increase")
    percent_increase = st.sidebar.slider(
        "Increase Percentage",
        5, 50, 10
    )

    if st.sidebar.button("Run Optimization"):
        # Send the data to the FastAPI backend for processing
        try:
            response = requests.post(
            "http://127.0.0.1:8000/price_optim",
            json={
                "week": week,
                "branch": branch,
                "meal": meal,
                "current_price": current_price,
                "email_promo": email_promo,
                "app_homepage_promo": app_homepage_promo,
                "discount_percent": discount_percent,
                "product_category": product_category,
                "product_cuisine": product_cuisine,
                "percent_increase": percent_increase
            })

            response.raise_for_status()

            results = response.json()

            price_range = results["price_range"]
            demand_list = results["demand_list"]
            profit_list = results["profit_list"]
            init_demand = results["predicted_demand"]


            message = st.success("Response Received!")

            time.sleep(1)

            message.empty()

        except requests.exceptions.RequestException as e:
            st.error(f"Backend Error: {e}")

        # So what should we do with these data??

        ## Computing needed Calculations


        # For Profit Optimization
        max_profit = max(profit_list)
        max_idx = profit_list.index(max_profit)


        best_price = price_range[max_idx]
        best_demand = demand_list[max_idx]
        best_profit = profit_list[max_idx]


        # Get current profit and revenue
        cost_price = 0.7 * current_price
        current_profit = (current_price * init_demand) - (cost_price * init_demand)
        best_revenue = best_price * best_demand
        current_revenue = current_price * init_demand

        # Find price delta
        demand_delta = ((best_demand - init_demand) / init_demand) * 100
        price_delta = ((best_price - current_price) / current_price) * 100
        revenue_delta = ((best_revenue - current_revenue) / current_revenue) * 100
        profit_delta = ((best_profit - current_profit) / current_profit) * 100


        # For Demand Optimization
        max_demand = max(demand_list)
        dem_idx = demand_list.index(max_demand)

        dem_price = price_range[dem_idx]
        dem_demand = demand_list[dem_idx]
        dem_profit = profit_list[dem_idx]

        # Best Demand Revenue

        dem_revenue = dem_demand * dem_price

        # Find demand delta
        dem_delt = ((dem_demand - init_demand) / init_demand) * 100
        price_delt = ((dem_price - current_price) / current_price) * 100
        revenue_delt = ((dem_revenue - current_revenue) / current_revenue) * 100
        profit_delt = ((dem_profit - current_profit) / current_profit) * 100




        # First create 4 cards for tracking

        if optimization_goal == "Profit":

            col1, col2, col3, col4 = st.columns(4)


            with col1:
                st.metric("Best Demand", f"{best_demand:,}", delta=f"{demand_delta:.2f}%")

            with col2:
                st.metric("Optimal Price", f"{best_price:,.2f}", delta=f"{price_delta:.2f}%")
            
            with col3:
                st.metric("Expected Revenue", f"{best_revenue:,.2f}", delta=f"{revenue_delta:.2f}%")

            with col4:
                st.metric("Optimization Goal", optimization_goal, delta=f"{profit_delta:.2f}%")

            

            col_1, col_2 = st.columns(2, gap="large")


            with col_1:
                df_dem = pd.DataFrame({
                "Price": price_range,
                "Demand": demand_list
                })

                fig = px.scatter(
                    df_dem,
                    x="Price",
                    y="Demand",
                    title="Price vs Demand"
                )

                fig.add_scatter(
                    x=[best_price],
                    y=[best_demand],
                    mode="markers",
                    marker=dict(size=12, color="green"),
                    name="Optimal Price"
                )
                fig.add_scatter(
                    x=[current_price],
                    y=[init_demand],
                    mode="markers",
                    marker=dict(size=12, color="red"),
                    name="Current Price"
                )

                st.plotly_chart(fig, use_container_width=True)

            with col_2:
                df_pro = pd.DataFrame({
                    "Price": price_range,
                    "Profit": profit_list
                })

                fig = px.line(
                    df_pro,
                    x="Price",
                    y="Profit",
                    title="Price vs Profit"
                )

                # Highlight optimum

                fig.add_scatter(
                    x=[best_price],
                    y=[best_profit],
                    mode="markers",
                    marker=dict(size=12, color="green"),
                    name="Optimal Price"
                )

                fig.add_scatter(
                    x=[current_price],
                    y=[current_profit],
                    mode="markers",
                    marker=dict(size=12, color="red"),
                    name="Current Price"
                )

                st.plotly_chart(fig, use_container_width=True)



            summary, optim = st.columns(2)

            with summary:
                summary_df = pd.DataFrame({
                    "Metric": ["Current Price",
                               "Best Price",
                               "Price Change",
                               "Best Demand",
                               "Demand Change",
                               "Best Revenue",
                               "Revenue Change"
                    ],

                    "Value": [
                                f"{current_price:,.2f}",
                                f"{best_price:,.2f}",
                                f"+{price_delta:,.2f}" if price_delta > 0 else f"{price_delta:,.2f}",
                                f"{best_demand:,.0f}",
                                f"+{demand_delta:,.2f}" if demand_delta > 0 else f"{demand_delta:,.2f}",
                                f"{best_revenue:,.2f}",
                                f"+{revenue_delta:,.2f}" if revenue_delta > 0 else f"{revenue_delta:,.2f}"
                            ]
                })
                st.subheader("Scenerio Summary")
                st.dataframe(summary_df, use_container_width=True, hide_index=True)

            with optim:
                optim_df = pd.DataFrame({
                    "Metric": ["Optimal Price",
                               "Expected Demand",
                               "Expected Revenue",
                               "Expected Profit"
                               ],

                    "Profit Optimization": [f"{best_price:,.2f}",
                                            best_demand,
                                            f"{best_revenue:,.2f}",
                                            f"{best_profit:,.2f}"
                                            ],

                    "Demand Optimization": [f"{dem_price:,.2f}",
                                            dem_demand,
                                            f"{dem_revenue:,.2f}",
                                            f"{dem_profit:,.2f}"
                                            ]
                })
                st.subheader("Optimization Comparison")
                st.dataframe(optim_df, use_container_width=True, hide_index=True)



        if optimization_goal == "Demand":

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Best Demand", f"{dem_demand:,.2f}", delta=f"{dem_delt:.2f}%")

            with col2:
                st.metric("Optimal Price", f"{dem_price:,}", delta=f"{price_delt:.2f}%")
            
            with col3:
                st.metric("Expected Revenue", f"{dem_revenue:,.2f}", delta=f"{revenue_delt:.2f}%")

            with col4:
                st.metric("Optimization Goal", optimization_goal, delta=f"{dem_delt:.2f}%")



            col_1, col_2 = st.columns(2, gap="large")

            with col_1:
                df_dem = pd.DataFrame({
                "Price": price_range,
                "Demand": demand_list
                })

                fig = px.scatter(
                    df_dem,
                    x="Price",
                    y="Demand",
                    title="Price vs Demand"
                )

                fig.add_scatter(
                    x=[dem_price],
                    y=[dem_demand],
                    mode="markers",
                    marker=dict(size=12, color="green"),
                    name="Optimal Demand"
                )
                fig.add_scatter(
                    x=[current_price],
                    y=[init_demand],
                    mode="markers",
                    marker=dict(size=12, color="red"),
                    name="Current Demand"
                )

                st.plotly_chart(fig, use_container_width=True)

            with col_2:
                df_pro = pd.DataFrame({
                    "Price": price_range,
                    "Profit": profit_list
                })

                fig = px.line(
                    df_pro,
                    x="Price",
                    y="Profit",
                    title="Price vs Profit"
                )

                # Highlight optimum

                fig.add_scatter(
                    x=[dem_price],
                    y=[dem_profit],
                    mode="markers",
                    marker=dict(size=12, color="green"),
                    name="Optimal Price"
                )

                fig.add_scatter(
                    x=[current_price],
                    y=[current_profit],
                    mode="markers",
                    marker=dict(size=12, color="red"),
                    name="Current Price"
                )

                st.plotly_chart(fig, use_container_width=True)


            summary, optim = st.columns(2)

            with summary:
                summary_df = pd.DataFrame({
                    "Metric": ["Current Price",
                               "Best Price",
                               "Price Change",
                               "Best Demand",
                               "Demand Change",
                               "Best Revenue",
                               "Revenue Change"
                    ],

                    "Value": [
                                f"{current_price:,.2f}",
                                f"{dem_price:,.2f}",
                                f"+{price_delt:,.2f}" if price_delt > 0 else f"{price_delt:,.2f}",
                                f"{dem_demand:,.0f}",
                                f"+{dem_delt:,.2f}" if dem_delt > 0 else f"{dem_delt:,.2f}",
                                f"{dem_revenue:,.2f}",
                                f"+{revenue_delt:,.2f}" if revenue_delt > 0 else f"{revenue_delt:,.2f}"
                            ]
                })
                st.subheader("Scenerio Summary")
                st.dataframe(summary_df, use_container_width=True, hide_index=True)

            with optim:
                optim_df = pd.DataFrame({
                    "Metric": ["Optimal Price",
                               "Expected Demand",
                               "Expected Revenue",
                               "Expected Profit"
                               ],

                    "Profit Optimization": [f"{best_price:,.2f}",
                                            best_demand,
                                            f"{best_revenue:,.2f}",
                                            f"{best_profit:,.2f}"
                                            ],

                    "Demand Optimization": [f"{dem_price:,.2f}",
                                            dem_demand,
                                            f"{dem_revenue:,.2f}",
                                            f"{dem_profit:,.2f}"
                                            ]
                })
                st.subheader("Optimization Comparison")
                st.dataframe(optim_df, use_container_width=True, hide_index=True)


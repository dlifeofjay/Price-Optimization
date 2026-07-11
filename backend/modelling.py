import pandas as pd
from pathlib import Path
import joblib
import numpy as np
import os

# Store Unique Branch IDs
Branch_IDs = [ 55,  24,  11,  83,  32,  13, 109,  52,  93, 186, 146,  57, 149,
        89, 124, 152,  97,  74, 108,  99,  66,  94,  91,  20,  34, 137,
        92, 126,  36, 162,  75, 177,  27, 157, 106,  64, 129,  14,  17,
       153, 139, 161,  81,  26,  73,  50, 104,  42, 113, 145,  53,  72,
        67, 174,  29,  77,  41,  30,  76,  59,  88, 143,  58,  10, 101,
        80,  43,  65,  39, 102, 110, 132,  23,  86,  68,  51,  61]

Meal_IDs = [1885, 1993, 2539, 2139, 2631, 1248, 1778, 1062, 2707, 1207, 1230,
       2322, 2290, 1727, 1109, 2640, 2306, 2126, 2826, 1754, 1971, 1902,
       1311, 1803, 1558, 2581, 1962, 1445, 2444, 2867, 1525, 2704, 2304,
       2577, 1878, 1216, 1247, 1770, 1198, 1438, 2494, 1847, 2760, 2492,
       1543, 2664, 2569, 2490, 1571, 2956, 2104]

Category = ['Beverages', 'Rice Bowl', 'Starters', 'Pasta', 'Sandwich',
       'Biryani', 'Extras', 'Pizza', 'Seafood', 'Other Snacks', 'Desert',
       'Soup', 'Salad', 'Fish']

Cuisine = ['Thai', 'Indian', 'Italian', 'Continental']

columns = ['week', 'center_id', 'meal_id', 'checkout_price',
       'emailer_for_promotion', 'homepage_featured', 'Discount_percent',
       'category', 'cuisine']

# read files

BASE_DIR = Path(__file__).resolve().parent

preprocessor_path = BASE_DIR / "Artifacts" / "preprocessor.pkl"
model_path = BASE_DIR / "Artifacts" / "optim_model.pkl"
test_data_path = BASE_DIR / "Data" / "test_data.npy"

feature_importance = BASE_DIR / "Data" / "Feature_Imp.parquet"

preprocessor = joblib.load(preprocessor_path)
model = joblib.load(model_path)

# Define a function that takes data, preprocess it and produce an output and then return predicted demand in a list,
# tested prices in a list, and profits in a list

def price_optim(data: list) -> tuple[list, list, list, int]:
    """
    This function takes in a list of features, preprocess and predicts demand
    then create a price change scenerio for up to the percentage entered,
    then gives gives profit and demand for each price change scenerio and returns the results in a tuple of lists
    """
    # Concert main features to what preprocessor expects
    df = pd.DataFrame(columns=columns, data=[data[:-1]])

    # Put into modelling pipeline
    prep_data = preprocessor.transform(df)

    # Predict demand
    pred_demand = model.predict(prep_data)

    """
    I want to test different price to see how demand is affected
    if the remaining variables remain constant
    """

    # Get current price and the percentage increase to test
    # divide percentage increase by 100 and add 1 to get the multiplier for the current price
    # multiply to get target maximum price to test

    current_price = data[3]
    percent_increase = data[-1]
    
    max_price = current_price * (1 + (percent_increase / 100))

    # Create 10 range of floating point price between current and max price
    price_range = np.round(np.linspace(current_price * 0.9, max_price, 20), 2)

    # Try to predict demand for each of this prices

    demand_list = []
    profit_list = []
    for price in price_range:

        # Update dataframe with new price
        df["checkout_price"] = price
        # Preprocess and predict demand
        prep_data = preprocessor.transform(df)
        new_demand = model.predict(prep_data)

        # Calculate Profit = price * demand - cost
        # Assumption cost is 70% of price
        cost = price * 0.7
        profit = (price - cost) * new_demand
        demand_list.append(int(new_demand[0]))
        profit_list.append(profit[0])

    return price_range.tolist(), demand_list, profit_list, int(pred_demand[0])


test_data = np.load(test_data_path)

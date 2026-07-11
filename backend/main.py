# Deploying issues, using direct call now

from fastapi import FastAPI
from pydantic import BaseModel
from modelling import price_optim
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware to allow Streamlit requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request validation
class PriceOptimRequest(BaseModel):
    week: int
    branch: int
    meal: int
    current_price: float
    email_promo: bool
    app_homepage_promo: bool
    discount_percent: int
    product_category: str
    product_cuisine: str
    percent_increase: int

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Price optimization endpoint
@app.post("/price_optim")
def price_optimization(request: PriceOptimRequest):
    data = [
        request.week,
        request.branch,
        request.meal,
        request.current_price,
        request.email_promo,
        request.app_homepage_promo,
        request.discount_percent,
        request.product_category,
        request.product_cuisine,
        request.percent_increase
    ]
    
    price_range, demand_list, profit_list, pred_demand = price_optim(data)
    
    return {
        "price_range": price_range,
        "demand_list": demand_list,
        "profit_list": profit_list,
        "predicted_demand": pred_demand
    }
    price_range, demand_list, profit_list, pred_demand = price_optim(data)
    
    return {
        "price_range": price_range,
        "demand_list": demand_list,
        "profit_list": profit_list,
        "predicted_demand": pred_demand
    }


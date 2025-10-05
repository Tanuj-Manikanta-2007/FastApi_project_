from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from mangum import Mangum

# ---------------- Data Models ---------------- #
# Basic product info returned to clients
class Goods(BaseModel):
    id: int
    name: str
    price: float

# Full product/worker info stored in server
class Worker(BaseModel):
    id: int
    name: str
    price: float
    discounted_price: Optional[float] = None
    internal_retailers_details: str

# ---------------- In-Memory Storage ---------------- #
# Temporary storage for products and retailers
# NOTE: This resets on serverless cold starts
products: Dict[int, Worker] = {}
retails: Dict[int, Worker] = {}

# ---------------- Create FastAPI App ---------------- #
app = FastAPI(title="FastAPI on Vercel", version="1.0")

# ---------------- Root Endpoint ---------------- #
@app.get("/")
def root():
    """
    Simple root endpoint to verify the app is running.
    Prevents 500 errors on GET /
    """
    return {"message": "FastAPI app running on Vercel!"}

# ---------------- API Endpoints ---------------- #
@app.post("/products/", response_model=Goods)
def add_product_goods(work: Worker):
    """
    Add a new product.
    Returns basic product info (Goods) to the client.
    """
    try:
        if work.id in products:
            raise HTTPException(status_code=400, detail="Product with this id already exists")
        products[work.id] = work
        retails[work.id] = work
        return work
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.get("/products_details/{id}", response_model=Goods)
def get_details(id: int):
    """
    Get details of a product by its ID.
    Returns only the basic product info (Goods).
    """
    try:
        if id not in products:
            raise HTTPException(status_code=404, detail="Id not found in database")
        return products[id]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

# ---------------- Optional Favicon Endpoint ---------------- #
@app.get("/favicon.ico")
def favicon():
    """
    Prevent 500 errors for favicon requests.
    Returns an empty response.
    """
    return {}

# ---------------- Mangum Adapter for Vercel ---------------- #
# This allows FastAPI to run as a serverless function
handler = Mangum(app)

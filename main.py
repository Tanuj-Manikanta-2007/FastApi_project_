from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from mangum import Mangum

# ---------------- Data Models ---------------- #
# Basic product info
class Goods(BaseModel):
    id: int
    name: str
    price: float

# Full worker/product info
class Worker(BaseModel):
    id: int
    name: str
    price: float
    discounted_price: Optional[float] = None
    internal_retailers_details: str

# ---------------- In-Memory Storage ---------------- #
# Temporary storage for products and retailers
products: Dict[int, Worker] = {}
retails: Dict[int, Worker] = {}

# ---------------- Create FastAPI App ---------------- #
app = FastAPI(title="FastAPI on Vercel", version="1.0")

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

# ---------------- Mangum Adapter for Vercel ---------------- #
# This allows FastAPI to run as a serverless function
handler = Mangum(app)

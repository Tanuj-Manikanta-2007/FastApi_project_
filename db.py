from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

class Goods(BaseModel):
    id: int
    name: str
    price: float

class Worker(BaseModel):
    id: int
    name: str
    price: float
    discounted_price: Optional[float] = None
    internal_retailers_details: str

products: Dict[int, Worker] = {}
retails: Dict[int, Worker] = {}

app = FastAPI()

@app.post('/products/', response_model=Goods)
def add_product_goods(work: Worker):
    if work.id in products:
        raise HTTPException(status_code=400, detail="Product with this id already exists")
    products[work.id] = work
    retails[work.id] = work
    return work

@app.get('/products_details/{id}', response_model=Goods)
def get_details(id: int):
    if id not in products:
        raise HTTPException(status_code=404, detail="Id not found in database")
    return products[id]

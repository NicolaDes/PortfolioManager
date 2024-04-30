from fastapi import FastAPI
from redis import Redis
from .data_retriever import DataRetriever
from .market_data import MarketData

app = FastAPI()
redis = Redis(host='redis', port=6379)
dr = DataRetriever(redis=redis, tout=60.0)
market = MarketData(redis=redis)

@app.get("/{type}/{symbol}")
def token_info(type: str, symbol: str):
    global market
    
    if market.isNew(symbol):
        market.addSymbol(type, symbol)

    price = market.price(symbol)

    return {"price": price}

@app.get("/ohcl/{type}/{symbol}")
def token_ohcl(type: str, symbol: str):
    global market
    
    if market.isNew(symbol):
        market.addSymbol(type, symbol)

    price = market.ohlc(symbol)

    return {"ohcl": price}
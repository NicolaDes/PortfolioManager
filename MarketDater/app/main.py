from fastapi import FastAPI
from redis import Redis
from app.marketer.data_retriever import DataRetriever
from app.marketer.market_data import MarketData

app = FastAPI()
redis = Redis(host='redis', port=6379)
dr = DataRetriever(redis=redis)
market = MarketData(redis=redis, dr=dr)

@app.get("/price/{ticker}")
def token_info(ticker: str):
    global market

    price = market.price(ticker)

    return {"price": price}

@app.get("/ohlc/{ticker}")
def token_ohlc(ticker: str):
    global market

    ohlc = market.ohlc(ticker)

    return {"ohcl": ohlc}

@app.post("/refresh")
async def refresh():
    global dr

    dr.downloadAll()
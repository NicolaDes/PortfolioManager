from fastapi import FastAPI
from redis import Redis
from app.marketer.data_retriever import DataRetriever
from app.marketer.market_data import MarketData

app = FastAPI()
redis = Redis(host='redis', port=6379)
dr = DataRetriever(redis=redis)
market = MarketData(redis=redis, dr=dr)

@app.get("/{ticker}")
def token_info(ticker: str):
    global market

    price = market.price(ticker)
    alpha = market.alpha(ticker)
    beta = market.beta(ticker)

    return {"eur": price, "alpha": alpha, "beta": beta}

@app.get("/ohlc/{ticker}")
def token_ohlc(ticker: str):
    global market

    ohlc = market.ohlc(ticker)

    return {"ohlc": ohlc}

@app.post("/refresh")
async def refresh():
    global dr

    dr.downloadAll()
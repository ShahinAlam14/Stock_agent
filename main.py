from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yfinance as yf
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
import diskcache
import aiofiles  # For future async file handling

# Initialize FastAPI
app = FastAPI()

# CORS Middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend from "frontend" folder
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/")
async def root():
    return {"message": "Stock Market Agent is running 🚀"}

# Initialize cache
cache = diskcache.Cache("stock_cache")

# Request model
class StockRequest(BaseModel):
    tickers: list

# Async function to fetch stock data
async def get_stock_price_and_data(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.history(period="30d")

        if stock_info.empty:
            return None, None, None

        current_price = stock_info['Close'].iloc[-1]
        moving_average = stock_info['Close'].mean()
        volatility = stock_info['Close'].max() - stock_info['Close'].min()

        return current_price, moving_average, volatility
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None, None, None

# LangChain + Ollama setup
llm = OllamaLLM(model="llama3")  # Alternatives: "mistral", "gemma", etc.

# Define prompt template
template = """
You are an AI assistant providing stock market analysis.
Given the stock price of {ticker}, the 30-day moving average of {moving_average}, and volatility, give a recommendation:

- SELL if the price is >10% above the 30-day moving average.
- BUY if the price is >10% below the 30-day moving average.
- HOLD if within 5% of the moving average.
- If volatility is high, recommend caution.

Current Price: {current_price}
30-Day Moving Average: {moving_average}
Volatility: {volatility}
"""

prompt = PromptTemplate(
    input_variables=["ticker", "current_price", "moving_average", "volatility"],
    template=template
)

# LangChain chain
chain = prompt | llm

# API endpoint to fetch stock prices
@app.post("/get-stock-prices")
async def get_stock_prices(request: StockRequest):
    results = []

    for ticker in request.tickers:
        ticker = ticker.upper()
        cache_key = f"{ticker}_data"
        cached_data = cache.get(cache_key)

        if cached_data:
            current_price, moving_average, volatility = cached_data
        else:
            current_price, moving_average, volatility = await get_stock_price_and_data(ticker)
            if current_price is None:
                results.append({
                    "ticker": ticker,
                    "error": f"Stock data for {ticker} not found."
                })
                continue
            cache.set(cache_key, (current_price, moving_average, volatility), expire=600)

        inputs = {
            "ticker": ticker,
            "current_price": current_price,
            "moving_average": moving_average,
            "volatility": volatility
        }
        recommendation = await chain.ainvoke(inputs)

        results.append({
            "ticker": ticker,
            "current_price": current_price,
            "moving_average": moving_average,
            "volatility": volatility,
            "recommendation": recommendation
        })

    return {"results": results}

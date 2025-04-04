# 📈 Stock Market Agent

## 🚀 Overview
This project is an AI-powered stock market analysis agent built with **FastAPI**, **LangChain**, and **Ollama LLM**. It fetches real-time stock prices, analyzes trends, and provides **BUY/SELL/HOLD** recommendations based on a 30-day moving average.

## ✨ Features
- ✅ Fetches **real-time stock prices** using `yfinance`.
- ✅ Provides AI-generated **buy/sell/hold** recommendations.
- ✅ Offers a **FastAPI-powered API** for stock analysis.
- ✅ Simple **frontend UI** for user interaction.
- ✅ Implements **caching** to reduce redundant API calls.

---
## 🏗️ Tech Stack
- **Backend:** FastAPI, LangChain, Ollama (LLaMA 3 model)
- **Frontend:** HTML, Bootstrap, JavaScript (Vanilla)
- **Data Source:** Yahoo Finance API (`yfinance`)
- **Caching:** `diskcache`

---
## ⚡ Installation & Setup
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/ShahinAlam14/Stock_agent.git
cd Stock_agent
```

### 2️⃣ Create & Activate Virtual Environment
```sh
python3 -m venv stock_env
source stock_env/bin/activate  # On Windows: stock_env\Scripts\activate
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Run the FastAPI Server
```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5️⃣ Open Frontend
- Open `http://localhost:8000` in your browser.
- Enter stock ticker(s) and analyze results!

---
## 🎯 API Endpoints
### **1️⃣ Check API Status**
```sh
GET /
```
📌 **Response:** `{ "message": "Stock Market Agent is running 🚀" }`

### **2️⃣ Get Stock Prices & Recommendations**
```sh
POST /get-stock-prices
```
📌 **Body:**
```json
{
  "tickers": ["AAPL", "TSLA"]
}
```
📌 **Response:**
```json
{
  "results": [
    {
      "ticker": "AAPL",
      "current_price": 175.20,
      "moving_average": 170.50,
      "volatility": 5.30,
      "recommendation": "HOLD"
    }
  ]
}
```

---
## 🛠️ Deployment
To deploy on a public server:
1. Use a cloud provider like **AWS, Render, or Railway**.
2. Set up `uvicorn` to serve FastAPI.
3. Configure **CORS** settings if needed.

---
## 🔥 Challenges & Solutions
### ✅ **Challenge: Stock Price Fetching Delays**
✔️ **Solution:** Used `diskcache` to store stock data for **10 minutes**, reducing API calls.

### ✅ **Challenge: AI Model Response Time**
✔️ **Solution:** Used **LangChain + Ollama** for efficient LLM execution.

---
## 🤖 AI Usage & Thought Process
- AI was used for **analysis**, but rules for buy/sell/hold decisions were **manually defined**.
- Decision-making **is not fully AI-dependent**—the logic follows strict conditions.
- The project structure, API design, and caching strategy were planned manually.

---
## 📜 License
This project is open-source under the **MIT License**.

🚀 **Happy Trading!**


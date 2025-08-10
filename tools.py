from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import yfinance as yf

class StockInput(BaseModel):
    """
    The input schema for Stock Tools
    The input of this tool should a ticker, for example AAPL, NET, TSLA etc...
    """
    ticker: str = Field(..., description="The input of this tool should a ticker, for example AAPL, NET, TSLA etc...")

class StockPriceTool(BaseTool):
    name: str = "One month stock price history"
    description: str = "Useful to get a month's worth of stock price data as CSV."
    args_schema: Type[BaseModel] = StockInput

    def _run(self, ticker: str) -> str:
        stock = yf.Ticker(ticker)
        return stock.history(period="1mo").to_csv()

class StockNewsTool(BaseTool):
    name: str = "Stock news URLs"
    description: str = "Useful to get URLs of news articles related to a stock."
    args_schema: Type[BaseModel] = StockInput

    def _run(self, ticker: str) -> str:
        stock = yf.Ticker(ticker)
        news_urls = [article["link"] for article in stock.news]
        return "\n".join(news_urls)

class IncomeStmtTool(BaseTool):
    name: str = "Company's income statement"
    description: str = "Useful to get the income statement of a stock as CSV."
    args_schema: Type[BaseModel] = StockInput

    def _run(self, ticker: str) -> str:
        stock = yf.Ticker(ticker)
        return stock.income_stmt.to_csv()

class BalanceSheetTool(BaseTool):
    name: str = "Balance sheet"
    description: str = "Useful to get the balance sheet of a stock as CSV."
    args_schema: Type[BaseModel] = StockInput

    def _run(self, ticker: str) -> str:
        stock = yf.Ticker(ticker)
        return stock.balance_sheet.to_csv()

class InsiderTransactionsTool(BaseTool):
    name: str = "Get insider transactions"
    description: str = "Useful to get insider transactions of a stock as CSV."

    def _run(self, ticker: str) -> str:
        stock = yf.Ticker(ticker)
        return stock.insider_transactions.to_csv()

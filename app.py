import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Dashboard Title
st.title("Portfolio Risk Dashboard")
st.sidebar.header("User Input")

# User Input for Stock Symbols
stocks = st.sidebar.text_input(
    "Enter stock symbols separated by commas (e.g., TCS.NS, ITC.NS):", "TCS.NS, ITC.NS"
)

# Fetch Data Function
def fetch_stock_data(tickers):
    data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        data[ticker] = hist
    return data

# Display Equity Risk with Risk Meter
def display_equity_risk(data):
    st.subheader("Equity Risk (Stock Price Fluctuations)")
    for ticker, hist in data.items():
        st.write(f"**{ticker}**: Closing Prices (Last Year)")
        st.line_chart(hist["Close"])

        # Show volatility (standard deviation of daily returns)
        hist["Daily Returns"] = hist["Close"].pct_change()
        volatility = hist["Daily Returns"].std() * (252 ** 0.5)  # Annualized volatility
        st.write(f"Annualized Volatility for {ticker}: **{volatility:.2%}**")

        # Calculate risk score based on volatility (higher volatility = higher risk)
        risk_score = min(int(volatility * 100), 100)
        st.write(f"**Equity Risk Meter for {ticker}:**")
        st.progress(risk_score)

# Display Liquidity Risk with Risk Meter
def display_liquidity_risk(data):
    st.subheader("Liquidity Risk (Trading Volume Analysis)")
    for ticker, hist in data.items():
        st.write(f"**{ticker}**: Average Daily Volume (Last Year)")
        avg_volume = hist["Volume"].mean()
        st.write(f"Average Volume for {ticker}: **{avg_volume:,.0f}**")
        st.bar_chart(hist["Volume"])

        # Calculate risk score based on volume (lower volume = higher risk)
        volume_risk_score = min(int(100 - (avg_volume / hist["Volume"].max()) * 100), 100)
        st.write(f"**Liquidity Risk Meter for {ticker}:**")
        st.progress(volume_risk_score)

# Display Commodity Risk with Risk Meter
def display_commodity_risk():
    st.subheader("Commodity Risk (Gold and Crude Oil)")
    gold = yf.Ticker("GC=F").history(period="1y")
    crude = yf.Ticker("CL=F").history(period="1y")

    st.write("**Gold (GC=F): Closing Prices (Last Year)**")
    st.line_chart(gold["Close"])
    st.write("**Crude Oil (CL=F): Closing Prices (Last Year)**")
    st.line_chart(crude["Close"])

    # Calculate volatility for commodities
    gold_volatility = gold["Close"].pct_change().std() * (252 ** 0.5)
    crude_volatility = crude["Close"].pct_change().std() * (252 ** 0.5)

    # Calculate risk score based on volatility (higher volatility = higher risk)
    commodity_risk_score = min(int(max(gold_volatility, crude_volatility) * 100), 100)
    st.write(f"**Commodity Risk Meter:**")
    st.progress(commodity_risk_score)

# Display Interest Rate Risk with Risk Meter
def display_interest_rate_risk():
    st.subheader("Interest Rate Risk")
    rates = {
        "Date": [
            "10-Jan-25",
            "03-Jan-25",
            "27-Dec-24",
            "20-Dec-24",
            "13-Dec-24",
            "06-Dec-24",
        ],
        "91-Day T-Bill (%)": [6.59, 6.6, 6.55, 6.47, 6.45, 6.43],
        "182-Day T-Bill (%)": [6.7, 6.72, 6.7, 6.64, 6.61, 6.54],
        "364-Day T-Bill (%)": [6.69, 6.7, 6.69, 6.63, 6.58, 6.53],
    }
    rates_df = pd.DataFrame(rates)
    rates_df["Date"] = pd.to_datetime(rates_df["Date"], format="%d-%b-%y")
    st.write("Treasury Bill Yields Over Time")
    st.line_chart(rates_df.set_index("Date"))

    # Calculate risk score for interest rate risk based on changes in T-Bill rates
    rate_changes = rates_df.diff().dropna()
    interest_rate_risk_score = min(int(rate_changes.max().max() * 10), 100)
    st.write(f"**Interest Rate Risk Meter:**")
    st.progress(interest_rate_risk_score)

# Display Currency Risk with Risk Meter
def display_currency_risk():
    st.subheader("Currency Risk (INR/USD Exchange Rate)")
    inr = yf.Ticker("INR=X").history(period="1y")
    st.write("**INR/USD Exchange Rate (Last Year)**")
    st.line_chart(inr["Close"])

    # Calculate risk score based on exchange rate fluctuations (higher fluctuations = higher risk)
    currency_volatility = inr["Close"].pct_change().std() * (252 ** 0.5)
    currency_risk_score = min(int(currency_volatility * 100), 100)
    st.write(f"**Currency Risk Meter:**")
    st.progress(currency_risk_score)

# Main App Logic
if stocks:
    tickers = [s.strip() for s in stocks.split(",")]
    stock_data = fetch_stock_data(tickers)

    # Display different risk categories
    display_equity_risk(stock_data)
    display_liquidity_risk(stock_data)
    display_commodity_risk()
    display_interest_rate_risk()
    display_currency_risk()

st.sidebar.markdown("**Portfolio Risk Dashboard** © 2025")

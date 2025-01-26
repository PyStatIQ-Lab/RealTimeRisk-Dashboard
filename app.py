import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Fetch stock data for TCS and ITC
def get_stock_data(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    data = stock.history(period="1y")  # Get the last year of stock data
    return data

# Calculate volatility
def calculate_volatility(stock_data):
    stock_data['returns'] = stock_data['Close'].pct_change()
    volatility = stock_data['returns'].std() * np.sqrt(252)  # Annualized volatility
    return volatility

# Market Risk Assessment
def market_risk(volatility):
    if volatility > 0.5:
        return "High Risk"
    elif 0.2 < volatility <= 0.5:
        return "Medium Risk"
    else:
        return "Low Risk"

# Liquidity Risk
def liquidity_risk(stock_symbol):
    stock_data = get_stock_data(stock_symbol)
    liquidity = stock_data['Volume'].mean()
    if liquidity < 1000000:  # Volume threshold can be adjusted
        return "High Risk"
    elif liquidity < 5000000:
        return "Medium Risk"
    else:
        return "Low Risk"

# Credit Risk
def credit_risk(stock_symbol):
    # Placeholder for credit risk based on company fundamentals (P/E ratio, Debt-to-Equity, etc.)
    if stock_symbol == 'TCS.NS':
        return "Low Risk"  # TCS is considered a low-risk company with strong fundamentals
    else:
        return "Medium Risk"  # ITC, while strong, might face medium credit risk due to its exposure to FMCG and tobacco

# Liquidity Risk visualization
def liquidity_visualization():
    stock_symbols = ['TCS.NS', 'ITC.NS']
    liquidity_dict = {}
    
    for symbol in stock_symbols:
        liquidity_dict[symbol] = liquidity_risk(symbol)
    
    liquidity_df = pd.DataFrame(list(liquidity_dict.items()), columns=['Stock', 'Liquidity Risk'])
    st.write("Liquidity Risk Assessment")
    st.dataframe(liquidity_df)

# Volatility Visualization
def volatility_visualization():
    stock_symbols = ['TCS.NS', 'ITC.NS']
    volatility_dict = {}
    
    for symbol in stock_symbols:
        stock_data = get_stock_data(symbol)
        volatility = calculate_volatility(stock_data)
        risk_level = market_risk(volatility)
        volatility_dict[symbol] = risk_level
    
    volatility_df = pd.DataFrame(list(volatility_dict.items()), columns=['Stock', 'Market Risk'])
    st.write("Market Risk Assessment")
    st.dataframe(volatility_df)

# Main function for Streamlit Dashboard
def main():
    st.title("Portfolio Risk Management Dashboard")
    
    st.sidebar.header("Select Stock Symbols:")
    selected_stocks = st.sidebar.multiselect("Choose Stocks", ['TCS.NS', 'ITC.NS'])
    
    if selected_stocks:
        for stock in selected_stocks:
            st.subheader(f"Risk Assessment for {stock}")
            # Market Risk (Volatility)
            stock_data = get_stock_data(stock)
            volatility = calculate_volatility(stock_data)
            market_risk_level = market_risk(volatility)
            st.write(f"Market Risk (Volatility): {market_risk_level}")
            
            # Liquidity Risk
            liquidity_level = liquidity_risk(stock)
            st.write(f"Liquidity Risk: {liquidity_level}")
            
            # Credit Risk
            credit_level = credit_risk(stock)
            st.write(f"Credit Risk: {credit_level}")
    
    # Show visualizations
    if st.button('Show Liquidity Risk Table'):
        liquidity_visualization()
    
    if st.button('Show Volatility Risk Table'):
        volatility_visualization()

# Run the Streamlit app
if __name__ == "__main__":
    main()

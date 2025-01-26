import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Function to fetch stock data for a selected stock symbol
def get_stock_data(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    data = stock.history(period="1y")  # Get the last year of stock data
    return data

# Calculate volatility
def calculate_volatility(stock_data):
    stock_data['returns'] = stock_data['Close'].pct_change()
    volatility = stock_data['returns'].std() * np.sqrt(252)  # Annualized volatility
    return volatility

# Calculate Beta (against the market, e.g., Nifty 50)
def calculate_beta(stock_data, market_data):
    # Calculate stock and market returns
    stock_data['returns'] = stock_data['Close'].pct_change()
    market_data['returns'] = market_data['Close'].pct_change()
    
    # Perform a linear regression to calculate Beta
    covariance = np.cov(stock_data['returns'].dropna(), market_data['returns'].dropna())[0, 1]
    market_variance = market_data['returns'].var()
    beta = covariance / market_variance
    return beta

# Value at Risk (VaR)
def calculate_var(stock_data, confidence_level=0.95):
    stock_data['returns'] = stock_data['Close'].pct_change()
    var = stock_data['returns'].quantile(1 - confidence_level)
    return var

# Sharpe Ratio
def calculate_sharpe_ratio(stock_data, risk_free_rate=0.04):
    stock_data['returns'] = stock_data['Close'].pct_change()
    excess_returns = stock_data['returns'] - risk_free_rate / 252
    sharpe_ratio = excess_returns.mean() / excess_returns.std() * np.sqrt(252)  # Annualized
    return sharpe_ratio

# Maximum Drawdown
def calculate_max_drawdown(stock_data):
    stock_data['cumulative_returns'] = (1 + stock_data['returns']).cumprod()
    stock_data['drawdown'] = stock_data['cumulative_returns'] / stock_data['cumulative_returns'].cummax() - 1
    max_drawdown = stock_data['drawdown'].min()
    return max_drawdown

# Sortino Ratio
def calculate_sortino_ratio(stock_data, risk_free_rate=0.04):
    stock_data['returns'] = stock_data['Close'].pct_change()
    downside_returns = stock_data['returns'][stock_data['returns'] < 0]
    excess_returns = stock_data['returns'] - risk_free_rate / 252
    downside_deviation = downside_returns.std()
    sortino_ratio = excess_returns.mean() / downside_deviation * np.sqrt(252)  # Annualized
    return sortino_ratio

# Treynor Ratio
def calculate_treynor_ratio(stock_data, beta, risk_free_rate=0.04):
    stock_data['returns'] = stock_data['Close'].pct_change()
    excess_returns = stock_data['returns'] - risk_free_rate / 252
    treynor_ratio = excess_returns.mean() / beta * np.sqrt(252)  # Annualized
    return treynor_ratio

# R-Squared (R²)
def calculate_r_squared(stock_data, market_data):
    stock_data['returns'] = stock_data['Close'].pct_change()
    market_data['returns'] = market_data['Close'].pct_change()
    correlation = np.corrcoef(stock_data['returns'].dropna(), market_data['returns'].dropna())[0, 1]
    r_squared = correlation**2
    return r_squared

# Tracking Error
def calculate_tracking_error(stock_data, benchmark_data):
    stock_data['returns'] = stock_data['Close'].pct_change()
    benchmark_data['returns'] = benchmark_data['Close'].pct_change()
    tracking_error = np.std(stock_data['returns'] - benchmark_data['returns'])
    return tracking_error

# Downside Deviation
def calculate_downside_deviation(stock_data, threshold=0):
    stock_data['returns'] = stock_data['Close'].pct_change()
    downside_returns = stock_data['returns'][stock_data['returns'] < threshold]
    downside_deviation = downside_returns.std() * np.sqrt(252)  # Annualized
    return downside_deviation

# Normalize Risk Metrics
def normalize_risk_metric(metric, min_value, max_value):
    return (metric - min_value) / (max_value - min_value)

# Plot interactive bar chart using Plotly
def plot_risk_metrics(risk_metrics, stock_symbols):
    fig = go.Figure()

    # Add data for each stock
    for stock in stock_symbols:
        fig.add_trace(go.Bar(
            x=risk_metrics[stock].keys(),
            y=risk_metrics[stock].values(),
            name=stock
        ))

    # Update layout for better visualization
    fig.update_layout(
        title="Risk Metrics Comparison",
        barmode='group',
        xaxis_title="Risk Metrics",
        yaxis_title="Risk Value",
        template="plotly_dark",
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig)

# Main function for Streamlit Dashboard
def main():
    st.title("Enhanced Equity Portfolio Risk Dashboard")

    st.sidebar.header("Select Stock Symbols:")
    selected_stocks = st.sidebar.text_input("Enter Stock Symbols (comma separated)", "TCS.NS,ITC.NS")
    
    stock_symbols = [symbol.strip() for symbol in selected_stocks.split(",")]
    
    # Fetch market data (e.g., Nifty 50 Index)
    nifty = yf.Ticker("^NSEI")
    market_data = nifty.history(period="1y")
    
    risk_metrics = {}
    
    if stock_symbols:
        for stock in stock_symbols:
            st.subheader(f"Risk Assessment for {stock}")
            # Fetch stock data
            stock_data = get_stock_data(stock)
            
            # Calculate individual risk metrics
            volatility = calculate_volatility(stock_data)
            beta = calculate_beta(stock_data, market_data)
            var = calculate_var(stock_data)
            sharpe_ratio = calculate_sharpe_ratio(stock_data)
            max_drawdown = calculate_max_drawdown(stock_data)
            sortino_ratio = calculate_sortino_ratio(stock_data)
            treynor_ratio = calculate_treynor_ratio(stock_data, beta)
            r_squared = calculate_r_squared(stock_data, market_data)
            tracking_error = calculate_tracking_error(stock_data, market_data)
            downside_deviation = calculate_downside_deviation(stock_data)
            
            # Store risk metrics in a dictionary
            risk_metrics[stock] = {
                'Volatility': volatility,
                'Beta': beta,
                'VaR': var,
                'Sharpe Ratio': sharpe_ratio,
                'Max Drawdown': max_drawdown,
                'Sortino Ratio': sortino_ratio,
                'Treynor Ratio': treynor_ratio,
                'R-Squared': r_squared,
                'Tracking Error': tracking_error,
                'Downside Deviation': downside_deviation
            }
            
            # Display individual metrics for the stock
            st.write(pd.DataFrame(risk_metrics[stock], index=[0]))
        
       # Plot interactive bar chart using Plotly
def plot_risk_metrics(risk_metrics, stock_symbols):
    fig = go.Figure()

    # Add data for each stock
    for stock in stock_symbols:
        # Ensure the data is in list form
        metrics = list(risk_metrics[stock].keys())  # risk metrics (e.g., Volatility, Beta, etc.)
        values = list(risk_metrics[stock].values())  # corresponding values for each risk metric

        # Add each stock's risk metrics to the plot
        fig.add_trace(go.Bar(
            x=metrics,
            y=values,
            name=stock
        ))

    # Update layout for better visualization
    fig.update_layout(
        title="Risk Metrics Comparison",
        barmode='group',
        xaxis_title="Risk Metrics",
        yaxis_title="Risk Value",
        template="plotly_dark",
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig)


if __name__ == "__main__":
    main()

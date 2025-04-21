# FuturePulse

**FuturePulse** is a Python library for backtesting price action trading strategies on financial time series data, such as 5-minute ES (E-mini S&P 500) futures. It provides tools to load market data, define trading strategies (e.g., wedge breakouts), simulate trades, and visualize results using interactive candlestick charts. Built with modularity and extensibility in mind, FuturePulse is ideal for traders and quantitative researchers looking to systematize and evaluate trading ideas.

## Features

- **Data Loading**: Load and resample OHLC (Open, High, Low, Close) data from CSV files (e.g., 1-minute to 5-minute intervals).
- **Strategy Development**: Define custom trading strategies with a flexible `BaseStrategy` class (e.g., `WedgeBreakoutStrategy`).
- **Backtesting**: Simulate trades and compute performance metrics.
- **Visualization**: Generate interactive candlestick charts with trade signals using Plotly.
- **Automation**: Streamline setup, testing, and execution with a `Makefile`.
- **Testing**: Ensure reliability with unit tests via `pytest`.
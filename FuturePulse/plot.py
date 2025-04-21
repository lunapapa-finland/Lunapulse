import plotly.graph_objects as go
import pandas as pd

class Plot:
    def plot_trades(self, data: pd.DataFrame, trades: list) -> str:
        """Generate a candlestick chart with trade signals."""
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='OHLC'
        )])

        # Add trade signals
        buy_signals = [t for t in trades if t['type'] == 'buy']
        sell_signals = [t for t in trades if t['type'] == 'sell']

        if buy_signals:
            fig.add_trace(go.Scatter(
                x=[t['timestamp'] for t in buy_signals],
                y=[t['price'] for t in buy_signals],
                mode='markers',
                name='Buy',
                marker=dict(symbol='triangle-up', size=10, color='green')
            ))

        if sell_signals:
            fig.add_trace(go.Scatter(
                x=[t['timestamp'] for t in sell_signals],
                y=[t['price'] for t in sell_signals],
                mode='markers',
                name='Sell',
                marker=dict(symbol='triangle-down', size=10, color='red')
            ))

        fig.update_layout(title='Wedge Breakout Trades', xaxis_title='Time', yaxis_title='Price')
        return fig.to_html(full_html=False)
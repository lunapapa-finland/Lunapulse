import plotly.graph_objects as go
import pandas as pd

class Plot:
    def plot_trades(self, data: pd.DataFrame, trades: list) -> str:
        """Generate a candlestick chart with trade signals, connecting bars regardless of gaps."""
        # Create a continuous integer index for x-axis
        continuous_index = list(range(len(data)))
        
        # Format hovertext for candlesticks
        hovertext = [f"Time: {t.strftime('%Y-%m-%d %H:%M')}<br>Open: {o}<br>High: {h}<br>Low: {l}<br>Close: {c}"
                     for t, o, h, l, c in zip(data.index, data['Open'], data['High'], data['Low'], data['Close'])]
        
        fig = go.Figure(data=[go.Candlestick(
            x=continuous_index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='OHLC',
            hovertext=hovertext,
            hoverinfo='text'
        )])

        # Add trade signals
        buy_signals = [t for t in trades if t['type'] == 'buy']
        sell_signals = [t for t in trades if t['type'] == 'sell']

        if buy_signals:
            # Map trade timestamps to continuous index
            buy_indices = [data.index.get_loc(t['timestamp']) for t in buy_signals]
            fig.add_trace(go.Scatter(
                x=buy_indices,
                y=[t['price'] for t in buy_signals],
                mode='markers',
                name='Buy',
                marker=dict(symbol='triangle-up', size=10, color='green'),
                customdata=[t['timestamp'] for t in buy_signals],
                hovertemplate='Time: %{customdata|%Y-%m-%d %H:%M}<br>Price: %{y}<extra>Buy</extra>'
            ))

        if sell_signals:
            sell_indices = [data.index.get_loc(t['timestamp']) for t in sell_signals]
            fig.add_trace(go.Scatter(
                x=sell_indices,
                y=[t['price'] for t in sell_signals],
                mode='markers',
                name='Sell',
                marker=dict(symbol='triangle-down', size=10, color='red'),
                customdata=[t['timestamp'] for t in sell_signals],
                hovertemplate='Time: %{customdata|%Y-%m-%d %H:%M}<br>Price: %{y}<extra>Sell</extra>'
            ))

        # Update x-axis to show timestamps at regular intervals
        tick_indices = continuous_index[::len(data)//10]  # Show ~10 ticks
        tick_timestamps = data.index[::len(data)//10].strftime('%Y-%m-%d %H:%M')
        fig.update_layout(
            title='Wedge Breakout Trades',
            xaxis_title='Time',
            yaxis_title='Price',
            xaxis=dict(
                tickmode='array',
                tickvals=tick_indices,
                ticktext=tick_timestamps
            )
        )
        
        return fig.to_html(full_html=False)
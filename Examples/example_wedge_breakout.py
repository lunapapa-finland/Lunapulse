from FuturePulse.data_loader import DataLoader
from FuturePulse.strategy import WedgeBreakoutStrategy
from FuturePulse.backtester import Backtester
from FuturePulse.plot import Plot

loader = DataLoader()
data = loader.load_data("Examples/MES.csv")
strategy = WedgeBreakoutStrategy(lookback=20)
backtester = Backtester()
results = backtester.run(data, strategy)
plot = Plot()
html = plot.plot_trades(data, results["trades"])
with open("Examples/trade_plot.html", "w") as f:
    f.write(html)
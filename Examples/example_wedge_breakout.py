from FuturePulse.data_loader import DataLoader
from FuturePulse.strategy import WedgeBreakoutStrategy
from FuturePulse.backtester import Backtester
from FuturePulse.plot import Plot

loader = DataLoader()
data = loader.load_data("Examples/MES_1min_data_2024-12-24_H25.CME.csv", resample=True)
strategy = WedgeBreakoutStrategy(lookback=20)
backtester = Backtester()
results = backtester.run(data, strategy)
plot = Plot()
html = plot.plot_trades(data, results["trades"])
with open("Examples/trade_plot.html", "w") as f:
    f.write(html)
import pandas
import sys
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings


warnings.filterwarnings("ignore")
sys.path.append('src/analysis')
import graphs

stock_prices = pandas.read_csv('src/data/TESLA_CLEANED.csv', parse_dates=True, index_col='date')
stock_prices = stock_prices['2015-01-01':'2024-12-09']

# Use 70% for training, 30% for testing (standard)
test_amt = int(len(stock_prices) * 0.30)-1
test = stock_prices[:test_amt]
train = stock_prices[test_amt:]

# Model
model = SARIMAX(train['adj_close'], order=(1, 1, 1), seasonal_order=(0, 1, 1, 12))
result = model.fit()

forecast_steps = 365
predictions = result.get_forecast(steps=forecast_steps).predicted_mean.rename("Predictions")

start_date = pandas.to_datetime('2025-01-01')
predicted_dates = pandas.date_range(start=start_date, periods=forecast_steps, freq='D')
predictions_with_dates = pandas.DataFrame({
    'date': predicted_dates,
    'adj_close': predictions.values
})

# convert to appropriate format
predictions_with_dates = [{'date': date, 'adj_close': adj_close} for date, adj_close in zip(predictions_with_dates['date'], predictions_with_dates['adj_close']) if date.month == 1]
graphs.graph_stock_over_time(predictions_with_dates, 'predictions_2025_tesla_janvier')

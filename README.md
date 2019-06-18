# AlphaQuery

* This script accesses the AlphaVantage API at alphavantage.co to retrieve historical price and volume data for US
equities.
* Outputs pandas DataFrame tables.
* Must input your personal API key by one of the following means:
    * Paste your API key surrounded by quotes `" "` into KEY_STRING within key.py
    * Input your API key surrounded by quotes `" "` when creating an instance of AlphaQuery with 
    `query = AlphaQuery(apikey=)`
* Initialize AlphaQuery with `query = AlphaQuery()`.
* Commands are executed from the `query` instance with `query.`command.

## Commands

* `get_quote(symbol=)` retrieves the most recent price data for the chosen symbol.
* `get_timeseries(symbol=, barsize=)` retrieves the 100 most recent bars of the chosen symbol and barsize
    * `barsize = 1min, 5min, 15min, 30min, 60min, day, week, month`
    * additional argument `adjusted=True` also retrieves split-adjusted prices
* `get_indicator(indicator=, symbol=, barsize=, period=)` retrieves the full indicator data for the chosen symbol
and barsize
    * `AlphaQuery.get_indicator_list()` displays list of available indicators
    * `barsize = 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly`
    * additional argument `price = open, high, low, close` chooses which price to calculate indicator
    * some `indicator`s receive additional arguments
    
## Examples

```python
# Initialize script
query = AlphaQuery()

# Retrieve last price data for Microsoft
query.get_quote(symbol='MSFT')

# Retrieve last 100 5-min price datapoints for General Electric
query.get_timeseries(symbol='GE', barsize='5min')

# Retrieve last 100 daily price datapoints for AT&T
query.get_timeseries(symbol='T', barsize='day', adjusted=True)

# Retrieve 12-day rolling Exponential Moving Average for Amazon
query.get_indicator(indicator='ema',
                    symbol='AMZN',
                    barsize='daily',
                    period=12)
```
import requests
from .formattable import FormatTable

try:
    from .key import KEY_STRING
except ModuleNotFoundError:
    pass


class AlphaQuery(object):
    """Base class to access the AlphaVantage API
    Tries to access the AlphaVantage API key in key.py
    If this file does not exist, key must be provided manually when creating instance
    """
    try:
        KEY = KEY_STRING
    except NameError:
        KEY = None

    URL = 'https://www.alphavantage.co/query?'

    INDICATOR_LIST = ['sma', 'ema', 'wma', 'dema', 'tema', 'trima', 't3', 'kama', 'mama', 'vwap',
                      'macd', 'macdext', 'stoch', 'stochf', 'rsi', 'stochrsi', 'willr', 'adx',
                      'adxr', 'apo', 'ppo', 'mom', 'bop', 'cci', 'cmo', 'roc', 'rocr', 'aroon',
                      'aroonosc', 'mfi', 'trix', 'ultosc', 'dx', 'minus_di', 'plus_di', 'minus_dm',
                      'plus_dm', 'brands', 'midpoint', 'midprice', 'sar', 'trange', 'atr', 'natr',
                      'ad', 'adosc', 'obv', 'ht_trendline', 'htsine', 'ht_trendmode', 'ht_dcperiod',
                      'ht_dcphase', 'ht_phasor']

    @classmethod
    def get_indicator_list(cls):
        """Access list of available technical indicators
        """
        return cls.INDICATOR_LIST

    def __init__(self, apikey=KEY):
        """Initialize AlphaQuery class

        Keyword arguments:
            apikey: AlphaVantage API key (default tries to find key in key.py)
        """
        self.key = apikey

    def _get_key(self):
        """Internal method to access key
        """
        return self.key

    def get_quote(self, *args, symbol=None, **kwargs):
        """Return GLOBAL_QUOTE request as pandas dataFrame

        Keyword arguments:
            symbol: stock ticker
        """
        parameters = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': self._get_key()
        }
        parameters.update(kwargs)

        response = requests.get(AlphaQuery.URL, params=parameters)

        table = FormatTable.make_table(response.content)

        table = FormatTable.clean_rows(table)
        table = FormatTable.first_row_as_header(table)

        return table

    def get_timeseries(self, *args, symbol=None, barsize=None, adjusted=False, **kwargs):
        """Return TIME_SERIES request as pandas dataFrame

        Keyword arguments:
            symbol: stock ticker
            barsize: interval (1min, 5min, 15min, 30min, 60min, day, week, month)
            adjusted: bool for including the adjusted close (default False)
        """
        parameters = {
            'function': 'TIME_SERIES',
            'symbol': symbol,
            'apikey': self._get_key()
        }

        if barsize == 'day':
            bar = '_DAILY'
        elif barsize == 'week':
            bar = '_WEEKLY'
        elif barsize == 'month':
            bar = '_MONTHLY'
        else:
            bar = '_INTRADAY'
            parameters['interval'] = barsize

        parameters.update(kwargs)

        adj = '_ADJUSTED' if adjusted else ''
        parameters['function'] += (bar + adj)

        response = requests.get(AlphaQuery.URL, params=parameters)

        table = FormatTable.make_table(response.content)

        table = FormatTable.unpack_series(table)
        table = FormatTable.clear_nan(table)
        table = FormatTable.clean_columns(table)

        return table

    def get_indicator(self, *args, indicator=None, symbol=None, barsize=None, price='close', period=10, **kwargs):
        """Return technical indicator request as pandas dataFrame

        Keyword arguments:
            indicator: technical indicator abbreviation
            symbol: stock ticker
            barsize: interval (1min, 5min, 15min, 30min, 60min, daily, weekly, monthly)
            price: price type for calculating indicator (open, high, low, default close)
            period: rolling data window for calculating indicator (default 10 bars)
            **Some indicators use additional arguments**
        """
        parameters = {
            'function': indicator,
            'symbol': symbol,
            'interval': barsize,
            'series_type': price,
            'time_period': period,
            'apikey': self._get_key()
        }
        parameters.update(kwargs)

        if indicator.lower() not in AlphaQuery.get_indicator_list():
            raise ValueError('indicator cannot be {}. Call {} for a list of available indicators'.format(
                indicator,
                AlphaQuery.get_indicator_list.__name__
            ))

        response = requests.get(AlphaQuery.URL, params=parameters)

        table = FormatTable.make_table(response.content)

        table = FormatTable.unpack_series(table)
        table = FormatTable.clear_nan(table)

        return table

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return str(self)

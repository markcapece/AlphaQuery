from alphaquery.alphaquery import AlphaQuery

if __name__ == '__main__':
    query = AlphaQuery()

    a = query.get_quote(symbol='MSFT')
    print(a.tail())

    b = query.get_timeseries(symbol='GE', barsize='5min')
    print(b.tail())

    c = query.get_timeseries(symbol='T', barsize='day', adjusted=True)
    print(c.tail())

    d = query.get_indicator(indicator='ema',
                            symbol='AMZN',
                            barsize='daily',
                            period=12)
    print(d.tail())

import requests
from saturn_key import crypto_compare_key
from datetime import datetime
import numpy as np
from mpl_finance import candlestick_ohlc
import matplotlib as mpl
import matplotlib.gridspec as gs
import matplotlib.pyplot as plt
from number_cleanup import *


def candlestick_chart_import(ticker, time_frame, candles, reference):
    """ Crypto candlestick chart.

    Arguments:
        :ticker: The desired ticker.
        :time_frame: 1d 1h 1m.
        :candles: The number of candles.
        :reference: the crypto or fiat to reference against.
    """

    print('----candlestick_chart----')
    print(str(datetime.now())[:19])

    ohlc_request = requests.get(
        f'https://min-api.cryptocompare.com/data/histo{time_frame}?fsym={ticker}&tsym={reference}&limit={candles}')

    if ticker == 'BTC'.upper():
        if reference == 'BTC':
            reference = 'USD'
        ohlc_request = requests.get(
            f'https://min-api.cryptocompare.com/data/histo{time_frame}?fsym=BTC&tsym={reference}&limit={candles}')

    if ticker == 'XBT'.upper():
        if reference == 'BTC':
            reference = 'USD'
        ohlc_request = requests.get(
            f'https://min-api.cryptocompare.com/data/histo{time_frame}?fsym=XBT&tsym={reference}&limit={candles}')

    print(f'Response: {ohlc_request}')

    ohlc_info = ohlc_request.json()

    # Manage error.
    if ohlc_info['Response'] == 'Error':
        return 'error'

    candlestick_chart = []

    for data in ohlc_info['Data']:
        time = datetime.fromtimestamp(
            data['time']).strftime('%H:%M:%S %Y-%m-%d')
        o = np.float(data['open'])
        h = np.float(data['high'])
        l = np.float(data['low'])
        c = np.float(data['close'])

        time_num = mpl.dates.datestr2num(time)

        candlestick_chart.append((time_num, o, h, l, c))
    
    # Final open and close value.
    ticker_close = candlestick_chart[-1][4]
    ticker_open = candlestick_chart[-1][1]
    
    # Format ticker close for title.
    if ticker_close < 1:
        ticker_close_str = str(ticker_close)
        ticker_close_str = number_format(ticker_close_str)
    else:
        ticker_close_str = str(round(ticker_close, 2))
    
    # Create the chart.
    mpl.style.use('dark_background')

    fig = plt.figure()
    gs1 = gs.GridSpec(nrows=1, ncols=10)
    ax1 = plt.subplot(gs1[0:1, 0:10])
    
    # If ticker is BTC price is in USD, otherwise price is in BTC.
    if ticker == 'BTC':
        plt.title(
            f'{ticker}: {candles} Candles @ 1 {time_frame}\nCurrent Price: {ticker_close_str} {reference}')
    elif ticker != 'BTC':
        plt.title(
            f'{ticker}: {candles} Candles @ 1 {time_frame}\nCurrent Price: {ticker_close_str} {reference}')

    # Size the candles for the time frame.
    if time_frame == 'minute':
        candlestick_ohlc(ax1, candlestick_chart, width=0.000283,
                         colorup='#00FF00', colordown='#FF00FF', alpha=1)
    elif time_frame == 'hour':
        candlestick_ohlc(ax1, candlestick_chart, width=0.017,
                         colorup='#00FF00', colordown='#FF00FF', alpha=1)
    else:
        candlestick_ohlc(ax1, candlestick_chart, width=0.408,
                         colorup='#00FF00', colordown='#FF00FF', alpha=1)

    ax1.xaxis.set_major_formatter(mpl.dates.DateFormatter('%d/%m/%y\n%H:%M'))

    ax1.spines['bottom'].set_color('#FF00FF')
    ax1.spines['top'].set_color('#FF00FF')
    ax1.spines['right'].set_color('#FF00FF')
    ax1.spines['left'].set_color('#FF00FF')

    # Amount of dates and price range displayed.
    ax1.xaxis.set_major_locator(mpl.ticker.MaxNLocator(7))
    ax1.yaxis.set_major_locator(mpl.ticker.MaxNLocator(10))
    
    # Brand the chart.

    ax1.text(0.14, 0.966, '@SaturnDAOBot',
            style='italic', size='large', color='#FF00FF', alpha=1,
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax1.transAxes)
    ax1.text(0.142, 0.908, 't.me/phoenixcrypto',
            style='italic', size='medium', color='#00FF00', alpha=1,
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax1.transAxes)
    ax1.text(0.14, 0.853, 'ObsessiveScript.com',
            style='italic', size='small', color='white', alpha=1,
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax1.transAxes)

    # Set line indicator green or red.
    if ticker_close > ticker_open:
        mpl.axes.Axes.axhline(ax1, y=ticker_close, xmin=0, xmax=1, color='#00FF00',
                              linestyle='dashed', linewidth=0.7, alpha=0.8)
    else:
        mpl.axes.Axes.axhline(ax1, y=ticker_close, xmin=0, xmax=1, color='#FF00FF',
                              linestyle='dashed', linewidth=0.7, alpha=0.8)
    plt.xticks(rotation=40)
    plt.grid(linestyle='dotted', color="grey")
    plt.tight_layout()

    plt.savefig(f'chart_crypto_{ticker}.png')
    plt.clf()
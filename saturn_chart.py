import requests
from datetime import datetime
import numpy as np
from mpl_finance import candlestick_ohlc
import matplotlib as mpl
import matplotlib.gridspec as gs
import matplotlib.pyplot as plt
from statistics import median


def saturn_chart_import(ticker):
    """ Display a 24 hour candlestick chart of Saturn Network coin. """

    # Retrieve ETC or ETH address from ticker.

    print('----saturn_chart----')
    print(str(datetime.now())[:19])
    if ticker == 'SATURN':
        return 'saturn'
    
    saturn_request = requests.get('https://ticker.saturn.network/returnTicker.json')
    result = saturn_request.json()
    
    print(f'Response: {saturn_request}')

    coin_value = []
    ticker_key = []
    ticker_key_upper = []

    for data in result:
        coin_value.append(data)
    for coin in coin_value:
        ticker_key.append(result[coin]['symbol'])
    for coin in ticker_key:
        ticker_key_upper.append(coin.upper())

    saturn_api = dict(zip(ticker_key_upper, coin_value))
        
    if ticker == 'SATURNETH':
        coin = 'ETH_0xb9440022a095343b440d590fcd2d7a3794bd76c8'
    elif ticker == 'SATURNETC':
        coin = 'ETC_0xac55641cbb734bdf6510d1bbd62e240c2409040f'
    
    if ticker != 'SATURNETH' and ticker != 'SATURNETC':
        try:
            coin = saturn_api[ticker]
        except KeyError:
            return 'error'
            print('--------ERROR RETURN')
            
    coin_base = coin[0:3]
    chart_address = coin[4:]

    #------------------------------------------------------------------------------------------------------------------#
    
    # Use ETC or ETH address to generate candlestick chart.

    chart_url = requests.get(f'https://ticker.saturn.network/api/v2/tokens/ohlcv/{coin_base}/{chart_address}/24h.json')
    chart_data = chart_url.json()
    
    chart_array = []
    high_list = []
    low_list = []
    high_num = 1.5

    for data in chart_data:
        high_list.append(float(data['high']))

    for data in chart_data:
        low_list.append(float(data['low']))

    high_mean = median(high_list)
    low_mean = median(low_list)

    for data in chart_data:
        time = datetime.utcfromtimestamp(
            data['time']).strftime('%H:%M:%S %Y-%m-%d')
        o = float(data['open'])
        if o >= high_mean * high_num:
            o = high_mean
        
        h = float(data['high'])
        if h >= high_mean * high_num:
            h = high_mean
        
            
        l = float(data['low'])
        if l >= high_mean * high_num:
            l = high_mean
        
        c = float(data['close'])
        if c >= high_mean * high_num:
            c = high_mean

        time_num = mpl.dates.datestr2num(time)
        chart_array.append((time_num, o, h, l, c))

    len_title = (len(chart_array))
    
    mpl.style.use('dark_background')

    # Final open and close value.
    ticker_close = chart_array[-1][4]
    ticker_open = chart_array[-1][1]
    
    fig = plt.figure()
    gs1 = gs.GridSpec(nrows=1, ncols=10)
    ax1 = plt.subplot(gs1[0:1, 0:10])

    ################### Reserved for when 5m and 1h have less volatility #################
    # if timeframe == '5m':                                                              #
    #     candlestick_ohlc(ax1, chart_array, width=0.2,                                  #
    #                         colorup='#00FF00', colordown='#FF00FF', alpha=1)           #
    # elif timeframe == '1h':                                                            # 
    #     candlestick_ohlc(ax1, chart_array, width=0.2,                                  #
    #                     colorup='#00FF00', colordown='#FF00FF', alpha=1)               #
    # elif timeframe == '24h':                                                           #
    #     candlestick_ohlc(ax1, chart_array, width=0.50,                                 #
    #                         colorup='#00FF00', colordown='#FF00FF', alpha=1)           #
    ######################################################################################

    candlestick_ohlc(ax1, chart_array, width=0.50,
                            colorup='#00FF00', colordown='#FF00FF', alpha=1)

    ax1.xaxis.set_major_formatter(mpl.dates.DateFormatter('%d/%m/%y'))

    ax1.spines['bottom'].set_color('#FF00FF')
    ax1.spines['top'].set_color('#FF00FF')
    ax1.spines['right'].set_color('#FF00FF')
    ax1.spines['left'].set_color('#FF00FF')

    # Amount of dates and price range displayed.
    ax1.xaxis.set_major_locator(mpl.ticker.MaxNLocator(7))
    ax1.yaxis.set_major_locator(mpl.ticker.MaxNLocator(10))

    plt.title(f'{ticker}: 24 Hours @ {len_title} Candles')
    plt.ylabel(f'{coin_base}')
    
    # Brand the chart.

    ax1.text(0.147, 0.968, 'Saturn.Network',
            style='normal', size='large', color='#FF00FF', alpha=1,
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax1.transAxes)
    ax1.text(0.149, 0.910, 'Saturn.Tools',
            style='normal', size='medium', color='#00FF00', alpha=1,
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax1.transAxes)
    ax1.text(0.149, 0.855, 't.me/phoenixcrypto',
            style='normal', size='medium', color='#00FF00', alpha=1,
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax1.transAxes)
    ax1.text(0.147, 0.800, 'ObsessiveScript.com',
            style='italic', size='small', color='white', alpha=1,
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax1.transAxes)
    
    ################### Reserved for when Saturn Network has less volatility #################
    # Set line indicator green or red.                                                       #
    # if ticker_close > ticker_open:                                                         #
    #     mpl.axes.Axes.axhline(ax1, y=ticker_close, xmin=0, xmax=1, color='#00FF00',        #
    #                           linestyle='dashed', linewidth=0.7, alpha=0.8)                #
    # elif ticker_close < ticker_open:                                                       #
    #     mpl.axes.Axes.axhline(ax1, y=ticker_close, xmin=0, xmax=1, color='#FF00FF',        #
    #                           linestyle='dashed', linewidth=0.7, alpha=0.8)                #
    # elif ticker_close == ticker_open:                                                      #
    #     mpl.axes.Axes.axhline(ax1, y=ticker_close, xmin=0, xmax=1, color='#000000',        # 
    #                           linestyle='dashed', linewidth=0.7, alpha=0.8)                #
    ##########################################################################################

    plt.xticks(rotation=40)
    plt.grid(linestyle='dotted', color="grey")
    plt.tight_layout()
    
    plt.savefig(f'chart_saturn_{ticker}.png')
    plt.clf ()  
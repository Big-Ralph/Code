import requests
import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import datetime
from number_cleanup import *
import matplotlib.ticker as ticker

def trade_stats_import(ticker, time_frame):
    """ Displays multiple stats for either ETC or ETH with a bar chart. """
  
    print('----trade_stats----')
    print(str(datetime.now())[:19])

    # Parse trade and mining data from Saturn API.
    
    url = requests.get('http://ticker.saturn.network/api/v2/stats/exchange.json')
    result = url.json()

    print(f'Response: {url}')

    total_trades = result[ticker]['total_trades']
    total_orders = result[ticker]['total_orders']
    token_count = result[ticker]['token_count']
    tokens_mined = result[ticker]['tokens_mined']
    total_volume = number_cleanup(result[ticker]['total_volume'])
    total_users = result[ticker]['total_users']
    volume24hr = number_cleanup(result[ticker]['volume24hr'])
    volume7d = number_cleanup(result[ticker]['volume7d'])
    chart_data = result[ticker]['charts']['volume']

    value_list = []
    time_list = []

    for data in chart_data:
        time = datetime.fromtimestamp(data['time']).strftime('%Y-%m-%d')
        time = mpl.dates.datestr2num(time)
        time_list.append(time)
    
        value = data['value']
        value_list.append(float(value))
        
        if len(time_list) >= time_frame:
                break

    reversed_time_list = time_list[::-1]
    reversed_value_list = value_list[::-1]

    # Add data to chart

    mpl.style.use('dark_background')
    fig, ax  = plt.subplots()
    plt.bar(reversed_time_list, reversed_value_list, color='#00FF00')  

    ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%d/%m/%Y'))
    ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(5))
    #plt.xticks(rotation=90)

    ax.text(0.138, 0.968, 'Saturn.Network',
            style='normal', size='large', color='#FF00FF', alpha=1,
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes)
    ax.text(0.140, 0.900, 'Saturn.Tools',
            style='normal', size='medium', color='#00FF00', alpha=1,
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes)
    ax.text(0.138, 0.832, 't.me/phoenixcrypto',
            style='normal', size='medium', color='#00FF00', alpha=1,
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes)

    ax.text(0.138, 0.764, 'ObsessiveScript.com',
            style='italic', size='small', color='white', alpha=1,
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes)

    plt.title(f'''Total Trades:   {total_trades} \nTotal Orders:   {total_orders} 
Token Count:   {token_count} \nTokens Mined: {tokens_mined}
Total Volume:  {total_volume} \nTotal Users:     {total_users} \nVolume 24hr:   {volume24hr}
Volume 7d:      {volume7d}''', loc='left')

    plt.ylabel(f'Trade Volume {ticker}')
    
    ax.spines['bottom'].set_color('#FF00FF')
    ax.spines['top'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.spines['left'].set_color('#FF00FF')

    ax.yaxis.grid(linestyle='dotted', color="grey")
    plt.tight_layout()
    plt.savefig(f'chart_trade_stats_{ticker}.png')
    plt.clf()
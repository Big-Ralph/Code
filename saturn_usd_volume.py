import requests
from datetime import datetime
import matplotlib as mpl 
import matplotlib.pyplot as plt

def saturn_usd_import(time_frame):
    print('----saturn_usd----')
    print(str(datetime.now())[:19])
        
    result = requests.get('http://ticker.saturn.network/api/v2/stats/exchange.json').json()

    eth = []
    saturn_eth = []
    etc = []
    saturn_etc = []
    time_list = []
    
    for data in result['ETH']['charts']['volume']:
        saturn_eth.append(float(data['value']))
        if len(saturn_eth) >= time_frame:
            break
    
    for data in result['ETC']['charts']['volume']:
        saturn_etc.append(float(data['value']))
        time = datetime.fromtimestamp(data['time']).strftime('%Y-%m-%d')
        time = mpl.dates.datestr2num(time)
        time_list.append(time)
        if len(saturn_etc) == len(saturn_eth):
            break

    usd_limit = len(saturn_eth) + 1

    eth_value = requests.get(f'https://min-api.cryptocompare.com/data/histoday?fsym=ETH&tsym=USD&limit={usd_limit}').json()
    etc_value = requests.get(f'https://min-api.cryptocompare.com/data/histoday?fsym=ETC&tsym=USD&limit={usd_limit}').json()

    for data in eth_value['Data']:
        eth.append(float(data['close']))
        if len(eth) == len(saturn_eth):
                break

    for data in etc_value['Data']:
        etc.append(float(data['close']))
        if len(etc) >= len(saturn_eth):
                break
                    
    time_list = time_list[::-1]

    total_eth = [x * y for x, y in zip(eth, saturn_eth)]
    total_etc = [x * y for x, y in zip(etc, saturn_etc)]
    total_usd = [x + y for x, y in zip(total_eth, total_etc)][::-1]

    mpl.style.use('dark_background')
    fig, ax = plt.subplots()
    plt.bar(time_list, total_usd, color='#00FF00')
    ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%d/%m/%Y'))
    ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(5))
    
    ax.text(0.150, 0.968, 'Saturn.Network',
            style='normal', size='large', color='#FF00FF', alpha=1,
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes)
    ax.text(0.147, 0.917, 'Saturn.Tools',
            style='normal', size='medium', color='#00FF00', alpha=1,
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes)
    ax.text(0.147, 0.866, 't.me/phoenixcrypto',
            style='normal', size='medium', color='#00FF00', alpha=1,
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes)
    ax.text(0.145, 0.815, 'ObsessiveScript.com',
            style='italic', size='small', color='white', alpha=1,
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes)

    plt.title('Saturn Network Daily Trading Volume', loc='left')
    plt.ylabel('Volume USD')

    ax.spines['bottom'].set_color('#FF00FF')
    ax.spines['top'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.spines['left'].set_color('#FF00FF')

    ax.yaxis.grid(linestyle='dotted', color="grey")
    plt.tight_layout()
    plt.savefig('saturn_usd_trade_stats.png')
    plt.clf()
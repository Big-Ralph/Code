import requests
from datetime import datetime
from number_cleanup import *
    
def saturn_ticker_import(ticker):
    """ Display an asset snapshot of Saturn Network coin. """
    
    print('----saturn_ticker----')
    print(str(datetime.now())[:19])

    saturn_request = requests.get(
        'https://ticker.saturn.network/returnTicker.json')
    result = saturn_request.json()
    print(f'Response: {saturn_request}')

    coin_value = []
    ticker_key = []
    ticker_key_upper = []
    list_dict = {}
    
    for data in result:
        coin_value.append(data)
    for coin in coin_value:
        ticker_key.append(result[coin]['symbol'])
    for coin in ticker_key:
        ticker_key_upper.append(coin.upper())

    saturn_api = dict(zip(ticker_key_upper, coin_value))
    
    if ticker == 'SATURN':
        return 'saturn'

    if ticker == 'SATURNETH':
        coin = 'ETH_0xb9440022a095343b440d590fcd2d7a3794bd76c8'
    elif ticker == 'SATURNETC':
        coin = 'ETC_0xac55641cbb734bdf6510d1bbd62e240c2409040f'


    if ticker != 'SATURNETH' and ticker != 'SATURNETC':
        try:
            coin = saturn_api[ticker]
        except:
            KeyError
            return 'error'

    if ticker == 'BCT':
        coin = 'ETC_0x1be6d61b1103d91f7f86d47e6ca0429259a15ff0'
    if ticker == 'LCT':
        coin = 'ETC_0xca68fe57a0e9987f940ebcc65fe5f96e7bc30128'
        
    coin_base = coin[0:3]
    coin_addy = coin[4:]
    
    detailed_request = requests.get(
        f'https://ticker.saturn.network/api/v2/tokens/summary/{coin_base}/{coin_addy}.json')
    detailed_result = detailed_request.json()
    
    for data in result:
        name = result[coin]['name']
        symbol = result[coin]['symbol']
        volume = result[coin]['quoteVolume']
        basevolume = result[coin]['baseVolume']
        high = result[coin]['highestBid']
        low = result[coin]['lowestAsk']
        change = result[coin]['percentChange']
    
    for data in detailed_result:
        price = detailed_result['token']['price24hr']
        buy_link = detailed_result['token']['best_buy_order_tx']
        sell_link = detailed_result['token']['best_sell_order_tx']
        ether_liq = detailed_result['token']['liquidity_depth']['ether']
        token_liq = detailed_result['token']['liquidity_depth']['tokens']
    
    volume_format = number_cleanup(volume)
    basevolume_format = number_cleanup(basevolume)
    high_format = number_cleanup(high)
    low_format = number_cleanup(low)
    ether_format = number_cleanup(ether_liq)
    token_format = number_cleanup(token_liq)
    
    if  coin_base == 'ETH':
        L5link_addy = (f'https://www.saturn.network/orders/{coin_base}/{buy_link}')
        L6link_addy = (f'https://www.saturn.network/orders/{coin_base}/{sell_link}')
    elif coin_base =='ETC':
        L5link_addy = (f'https://www.saturn.network/orders/{coin_base}/{buy_link}')
        L6link_addy = (f'https://www.saturn.network/orders/{coin_base}/{sell_link}')
    
    if change == '' or change == None:
        change = '0'
    if price == '' or price == None:
        price = '0'
    
    indicator_num = float(change) * 100

    price = number_cleanup(price)
    
    if float(change) < 0:
        change = change[1:]
        change_sign = '-'
    else:
        change_sign = ''
    
    change_percent_float = float(change) * 100
    change_percent = number_cleanup(str(change_percent_float))
    change_final = (f'{change_sign}{change_percent}')
    
    change_symbol = indicator(indicator_num)
    
    L1 = (f"〽️ <b>{name} ({symbol}) 〽️</b>\n\n")
    L2 = (f"💰 Price 24h:          <b>{price} {coin_base}</b>\n\n")
    L3 = (f"📊 Volume:             <b>{volume_format}</b>\n")
    L4 = (f"📶 Volume (<b>{coin_base}</b>):  <b>{basevolume_format}</b>\n\n")
    L5 = (f"🚀 <a href='{L5link_addy}'>Highest Bid:</a>      <b>{high_format}</b>\n")
    L6 = (f"📉 <a href='{L6link_addy}'>Lowest Ask:</a>      <b>{low_format}</b>\n\n")
    L7 = (f"{change_symbol} Change 24h:     <b>{change_final} %</b>\n\n")
    liq = (f"💧 <b>Liquidity</b> 💧\n        Ether:      <b>{ether_format}</b>\n        Tokens:  <b>{token_format}</b>\n\n")
    saturn_network = "<a href='Saturn.network'>Saturn.Network</a>\n"
    saturn_tools = "<a href='SATURN.tools'>Saturn.Tools</a>\n"
    phoenix = "<a href='https://t.me/phoenixcrypto'>Join Phoenix on Telegram</a>"
    
    
    return L1 + L2 + L3 + L4 + L5 + L6 + L7 + liq + saturn_network + saturn_tools + phoenix 
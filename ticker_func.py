from saturn_key import crypto_compare_key
from datetime import datetime
import requests
from number_cleanup import *

def coin_info_import(ticker_1, ticker_2):
    """ Return comparison on tickers.

    Arguments:
        :ticker_1: The main ticker.
        :ticker_2: The conversion.
    """

    print('----coin_info----')
    print(datetime.now())

    # Retrieve and parse data from cryptocompare.
    listing_url = (f'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={ticker_1}') + \
                  (f'&tsyms={ticker_2}&api_key={crypto_compare_key}')

    listing_response = requests.get(listing_url)
    print(f'Response: {listing_response}') 

    listing_result = requests.get(listing_url).json()[
        'RAW'][ticker_1][ticker_2]

    # Clean up results for bot display.
    price_float = listing_result['PRICE']
    price_str = str(price_float)

    market_cap = '{:,}'.format(round(listing_result['MKTCAP'], 2))
    volume_24h = '{:,}'.format(round(listing_result['TOTALVOLUME24HTO'], 2))

    change_24h = '{:,}'.format(round(listing_result['CHANGEPCT24HOUR'], 2))
    change_24h_float = listing_result['CHANGEPCT24HOUR']
    display_pic = indicator(change_24h_float)

    if price_float >= 1:
        # Round to 2 decimal places.
        price_str = '{:,}'.format(round(price_float, 2))
    else:
        # Call number_format function.
        price_str = number_format(price_str)

    # Retrieve data for all time high.
    all_time_high = requests.get(
        f'https://min-api.cryptocompare.com/data/histoday?fsym={ticker_1}&tsym={ticker_2}&limit=1000').json()

    # Clean up results for bot display.
    ath_list = []
    for data in all_time_high['Data']:
        ath = data['high']
        ath_list.append(ath)

    ath_float = float(max(ath_list))
    ath_string = str(max(ath_list))

    if ath_float >= 1:
        ath_string = '{:,}'.format(round(ath_float, 2))
    else:
        ath_string = number_format(ath_string)

    # Format final strings.
    string_1 = (f"<b>〽️ {ticker_1} : {ticker_2} 〽️</b>")
    string_2 = (f"📈 MK Cap:  <b>{market_cap}</b>")
    string_3 = (f"📊 Volume:  <b>{volume_24h}</b>")
    string_4 = (f"💰 Price:       <b>{price_str}</b>")
    string_5 = (f"{indicator(change_24h_float)} 24 hr:       <b>{change_24h} %</b>")
    string_6 = (f"🚀 ATH:        <b>{ath_string}</b>")
    string_7 = ("<a href='https://obsessivescript.com/'>Obsessive Script</a>")
    phoenix = "<a href='https://t.me/phoenixcrypto'>Join us on Telegram</a>\n\n"

    return (f'{string_1}\n\n{string_2}\n\n{string_3}\n\n{string_4}\n{string_5}\n\n{string_6}\n\n{phoenix}')
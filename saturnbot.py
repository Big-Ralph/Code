from telegram.ext import CommandHandler, Updater, Filters
from saturn_key import telegram_key
from functools import wraps
from telegram import ChatAction
from restart import *

# To Do:

#   - Saturn network vs BTC and USD comparison.
#   - Error message for sac and sp command.

updater = Updater(token=telegram_key)
dispatcher = updater.dispatcher
queue = updater.job_queue


def send_action(action):
    """ Sends `action` while processing func command. """

    def decorator(func):
        @wraps(func)
        def command_func(*args, **kwargs):
            bot, update = args
            bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(bot, update, **kwargs)
        return command_func
    
    return decorator


@send_action(ChatAction.TYPING)
def saturn_ticker(bot, update, args):
    # User input - ticker.
    # Asset snapshot for Saturn Network Coin.

    from saturn_ticker_func import saturn_ticker_import

    ticker = args[0].upper()
    
    return_data = saturn_ticker_import(ticker)
    
    if return_data == 'saturn':
        bot.send_message(chat_id=update.message.chat_id,
                        text='*Please choose SaturnETC or SaturnETH*',
                        parse_mode='markdown')
        print('--------SATURN CHOSEN')

    elif return_data == 'error':
        bot.send_message(chat_id=update.message.chat_id,
                                    text='*Sorry this coin is not on Saturn Network 😅*',
                                    parse_mode='markdown')
        print('--------ERROR RETURN')

    else:
        bot.send_message(chat_id=update.message.chat_id,
                        text=return_data,
                        parse_mode='HTML',
                        disable_web_page_preview=True)
        print('--------RUN FUNCTION')


@send_action(ChatAction.UPLOAD_PHOTO)
def saturn_chart(bot, update, args):
    # User input - ticker.
    # Candlestick chart for Saturn Network Coin.

    from saturn_chart import saturn_chart_import
    
    ticker = args[0].upper()

    ####################### Reserved for use of 5m and 1h charts ###########
    # timeframe = args[1]                                                  #
    #                                                                      #
    # if timeframe == 'd':                                                 #
    #     timeframe = '24h'                                                #
    # if timeframe == 'h':                                                 #
    #     timeframe = '1h'                                                 #
    # if timeframe == 'm':                                                 #
    #     timeframe = '5m'                                                 #
    ########################################################################
    
    response = saturn_chart_import(ticker)
    
    if response == 'saturn':
        bot.send_message(chat_id=update.message.chat_id,
                        text='*Please choose SaturnETC or SaturnETH*',
                        parse_mode='markdown')
        print('--------SATURN CHOSEN')
    elif response == 'error':
        bot.send_message(chat_id=update.message.chat_id,
                        text='*Sorry this coin is not on Saturn Network 😅*',
                        parse_mode='markdown')
        print('--------ERROR RETURN')
    else:
        bot.send_photo(chat_id=update.message.chat_id,
                       photo=open(f'chart_saturn_{ticker}.png', 'rb'))
        print('--------RUN FUNCTION')


@send_action(ChatAction.UPLOAD_PHOTO)
def trade_stat(bot, update, args):
    # User input - eth or etc.
    
    from trade_stats import trade_stats_import
    
    ticker = args[0].upper()
    time_frame = 30

    try:
        time_frame = args[1]
        if time_frame == 'max'.lower():
            time_frame = 10000
        else:
            time_frame = int(time_frame)
    except:
        Exception

    if ticker != 'ETH' and ticker != 'ETC':
        bot.send_message(chat_id=update.message.chat_id,
                        text='*Please choose etc or eth*',
                        parse_mode='markdown')
        print('--------ERROR RETURN')

    trade_stats_import(ticker, time_frame)
    
    if ticker == 'ETC' or ticker == 'ETH':
        bot.send_photo(chat_id=update.message.chat_id,
                    photo=open(f'chart_trade_stats_{ticker}.png', 'rb'))
        print('--------RUN FUNCTION')


@send_action(ChatAction.UPLOAD_PHOTO)
def saturn_usd(bot, update, args):

    from saturn_usd_volume import saturn_usd_import
    
    time_frame = 30

    try:
        time_frame = args[0]
        if time_frame == 'max'.lower():
            time_frame = 10000
        else:
            time_frame = int(time_frame)
    except:
        Exception

    saturn_usd_import(time_frame)

    bot.send_photo(chat_id=update.message.chat_id,
                photo=open('saturn_usd_trade_stats.png', 'rb'))
    print('--------RUN FUNCTION')


@send_action(ChatAction.TYPING)
def coin_info(bot, update, args):
    # User input - ticker_1, ticker_2.
    # Asset snapshot from CryptoCompare API.
    
    from ticker_func import coin_info_import

    ticker_1 = args[0].upper()
    ticker_2 = 'USD'

    try:
        ticker_2 = args[1].upper()
    except:
        Exception

    return_data = coin_info_import(ticker_1, ticker_2)

    bot.send_message(chat_id=update.message.chat_id,
                     text=return_data,
                     parse_mode='HTML', disable_web_page_preview=True)
    print("--------RUN FUNCTION")


@send_action(ChatAction.UPLOAD_PHOTO)
def candlestick_chart(bot, update, args):
    # User input - ticker, time_frame, candles.
    # Candlestick chart from CryptoCompare API.

    from crypto_chart import candlestick_chart_import

    ticker = args[0].upper()
    
    time_frame = 'hour'

    try:
        if args[1] == 'm'.lower():
            time_frame = 'minute'
        elif args[1] == 'h'.lower():
            time_frame = 'hour'
        elif args[1] == 'd'.lower():
            time_frame = 'day'
    except:
        Exception

    candles = '100'
    
    try:
        candles = args[2]
    except:
        Exception

    reference = 'BTC'

    try:
        reference = args[3].upper()
    except:
        Exception

    response = candlestick_chart_import(ticker, time_frame, candles, reference)

    if response == 'error':
        bot.send_message(chat_id=update.message.chat_id,
                    text="*Sorry this is not in my database 😅*", parse_mode='Markdown')
        print("--------ERROR RETURN")
    else:
        bot.send_photo(chat_id=update.message.chat_id,
                photo=open(f'chart_crypto_{ticker}.png', 'rb'))
        print("--------RUN FUNCTION")


def wake_up(bot, job):
    # Prevent bot from sleeping.

    bot.send_message(chat_id='-381741044',
                     text='️️----- Saturn Ping -----')


def main():
    updater.dispatcher.add_handler(CommandHandler('sa', saturn_ticker, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('sch', saturn_chart, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('st', trade_stat, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('susd', saturn_usd, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('sp', coin_info, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('sac', candlestick_chart, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('r', restart, filters=Filters.user(
                                                    username=['BigRalph', 'NeuronOfRados', 'OldCryptoGeek', 
                                                              'WizardsOrb'])))
    

def poll():
    updater.start_polling()
    updater.idle()


ping = queue.run_repeating(wake_up, interval=300, first=0)

if __name__ == '__main__':
    main()
    poll()
    ping
from decimal import Decimal

def number_format(number):
    """ Returns a float with 3 digits at the end of the string of zero's. """

    # Separate the integers from the zero's.
    number_tuple = Decimal(number).as_tuple()
    
    # Join the tuple in a string.
    ints = (str(number_tuple[1][:3]))[1:8:3]

    # Get number of zero's and create string.
    zeros = (-(number_tuple[2])) - (len(number_tuple[1]))
    zeros_string = ''.join(['0' for x in range(zeros)])
    final_num = (f'.{zeros_string}{ints}')
    if final_num == '.0':
        return '0'
    else:
        return final_num



def number_cleanup(number):
    if number == '' or number == None:
        number = '0'

    number_float = float(number)

    if number_float < 1:
        return number_format(number)
    elif number_float >= 1:
        return '{:,}'.format(round(number_float, 2))


def indicator(change):
    """ Displays different images based on percent gained above or below zero. """

    if change == 0:
        return '⚪️'
    elif change > 0:
        return '✅'
    elif change < 0:
        return '❌'
import calendar
from datetime import datetime


# Function to get pay period (start date and end date) based on a date
def get_pay_period(date):

    # Parse the date string to a datetime object
    date = datetime.strptime(date, '%d/%m/%Y')

    if date.day <= 15:
        start_date = date.replace(day=1)
        end_date = date.replace(day=15)
    else:
        start_date = date.replace(day=16)
        last_day = calendar.monthrange(date.year, date.month)[1]
        end_date = date.replace(day=last_day)

    return {'startDate': start_date.strftime('%Y-%m-%d'), 'endDate': end_date.strftime('%Y-%m-%d')}



# Function to remove item if amountPaid is 0 and to format it (convert float to string prefixed with $)
def format_amount_paid(data):

    for key, value in data.items():
        amount_paid = value['amountPaid']
        amount = float(amount_paid)
        formatted_amount = format_currency(amount)
        value['amountPaid'] = formatted_amount


#Function to format the currency by prefixing with $ and appending zeroes
def format_currency(value):
    if '.' in str(value):
        integer_part, decimal_part = str(value).split('.')
        if len(decimal_part) == 0:
            formatted_value = f"{integer_part}.00"
        elif len(decimal_part) == 1:
            formatted_value = f"{integer_part}.{decimal_part}0"
        else:
            formatted_value = f"{integer_part}.{decimal_part[:2]}"
    else:
        formatted_value = f"{value}.00"

    # Return the formatted value prefixed with $
    return f"${formatted_value}"
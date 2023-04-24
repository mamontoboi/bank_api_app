"""The module includes several views that are responsible for handling
HTTP requests and processing data received from the NBP API.
"""

import json
import re
from xml.etree import ElementTree as ET
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response


# http://localhost:8000/api/v1/average/usd/2023-03-01/
@api_view(['GET'])
def rate_per_date(request, code, date):
    """The rate_per_date view receives a GET request with two
    parameters: code and date. It returns a JSON response with the average
    exchange rate for the given currency 'code' and 'date'.
    """

    if not validate_code(code, LIST_OF_CODES):
        return Response({"Error": "Please provide a standard abbreviation. "
                                  "The list of codes can be found at "
                                  "'https://nbp.pl/en/statistic-and-financial-reporting/rates/table-a/'"})

    if not validate_date(date):
        return Response({"Error": "Please provide date in YYYY-MM-DD format"})

    try:
        data = fetch_data(f"http://api.nbp.pl/api/exchangerates/rates/a/{code}/{date}/?format=json")
        avg_rate = data['rates'][0]['mid']
    except json.decoder.JSONDecodeError:
        return Response({"Error": "Unfortunately, NBP does not "
                                  "provide the data for weekends or holidays."})
    return Response({"average rate": avg_rate})


# http://localhost:8000/api/v1/minimax/usd/255/
@api_view(['GET'])
def minimax_per_period(request, code, number):
    """The minimax_per_period view receives a GET request with
    two parameters: code and number. It calculates the minimum and maximum average
    exchange rate for the given 'number' of days for the given currency 'code'.
    """

    if not validate_code(code, LIST_OF_CODES):
        return Response({"Error": "Please provide a standard abbreviation. "
                                  "The list of codes can be found at "
                                  "'https://nbp.pl/en/statistic-and-financial-reporting/rates/table-a/'"})

    if not validate_period(number):
        return Response({"Error": "The number of requested records "
                                  "should be within the range from 1 to 255."})

    if data := fetch_data(f"http://api.nbp.pl/api/exchangerates/rates/a/{code}/last/{number}/?format=json"):
        rates = [record['mid'] for record in data['rates']]
        return Response({"minimum average value": min(rates), "maximum average value": max(rates)})
    return Response({"Error": "The remote server did not respond. "
                              "lease, try again later."})


# http://localhost:8000/api/v1/diff/usd/60/
@api_view(['GET'])
def biggest_diff(request, code, number):
    """The biggest_diff view retrieves the major difference between the highest
    ask price and the lowest bid price for the last `number` days of currency
    with the given `code`.
    """

    if not validate_code(code, LIST_OF_CODES):
        return Response({"Error": "Please provide standard code abbreviation. "
                                  "The list of codes can be found at "
                                  "'https://nbp.pl/en/statistic-and-financial-reporting/rates/table-a/'"})

    if not validate_period(number):
        return Response({"Error": "The number of requested records "
                                  "should be within the range from 1 to 255."})

    if data := fetch_data(f"http://api.nbp.pl/api/exchangerates/rates/c/{code}/last/{number}/?format=json"):
        rates = [(record['ask'] - record['bid']) for record in data['rates']]
        return Response({"major difference": round(max(rates), 3)})
    return Response({"Error": "The remote server did not respond. "
                              "Please, try again later."})


@api_view(['GET'])
def available_codes(request):
    """The function returns the list of all currency codes supported by the bank."""
    return Response({"codes": LIST_OF_CODES})


def fetch_data(url):
    """The function sends GET request to given url and returns the
    response in JSON format. If url does not respond it returns None.
    """

    try:
        data = requests.get(url, timeout=5).json()
    except requests.exceptions.Timeout:
        return None
    return data


def list_of_codes():
    """The function collects all currency codes supported by bank
    and returns the list of them.
    """

    codes = []

    try:
        data = requests.get('https://static.nbp.pl/dane/kursy/xml/en/23a078en.xml', timeout=5)
    except requests.exceptions.Timeout:
        return codes
    str_data = data.content.decode('utf-8')

    root = ET.fromstring(str_data)
    for code in root:
        codes.append(code.get('code'))

    return codes


LIST_OF_CODES = list_of_codes()


def validate_code(code, codes_list):
    """The function validates that the currency code provided by
    the user exists in list of codes supported by the bank.
    """

    if not codes_list:
        return False
    if code.upper() not in LIST_OF_CODES:
        return False
    return True


def validate_date(date):
    """The function validates that the user-provided date is in correct format."""

    if re.match(r'\d{4}-\d{2}-\d{2}', date) is None:
        return False
    return True


def validate_period(number):
    """The function validates that the requested period of interest is within
    the limit of 255 records.
    """

    if 1 <= number <= 255:
        return True
    return False

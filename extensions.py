import requests
import json
from config import Exchange_TOKEN, keys

class APIException(Exception):
    pass

class Convertor:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Одинаковые валюты {base} не переводятся.')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Неверно задано значение {amount}')

        r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key={Exchange_TOKEN}')
        return round(
            (json.loads(r.content)['rates'][base_ticker] / json.loads(r.content)['rates'][quote_ticker]) * int(amount),
            2)

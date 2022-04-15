import json
import requests
from config import keys

class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = keys[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            quote_key = keys[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        if base_key == quote_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')
        
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')
        
        r = requests.get(f"https://openexchangerates.org/api/latest.json?app_id=80289f5530f4487a8cb0bc492f029298&base={base_key}")
        resp = json.loads(r.content)
        new_price = resp['rates'][quote_key] * amount
        new_price = round(new_price, 3)
        message =  f"Цена {amount} {base} в {quote} : {new_price}"
        return message
import requests
import json
from currency_converter import CurrencyConverter
currency = CurrencyConverter()
API_KEY="ljo0rdtfme3bfrr3r033d"

def get_info(coin):
    symbol = get_symbol(coin.capitalize())
    if symbol is None: symbol = coin
    url = "https://api.lunarcrush.com/v2?data=assets&key="+API_KEY+"&symbol="+symbol
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()['data']
        current_value = data[0]['price']
        intro = "Here are a few informations about " + coin + " !!!\n"
        current_value_usd = "Current USD: " + str(round(data[0]['price'])) + "\n"
        current_value_eur = "Currrent EUR: " + str(currency.convert(current_value, 'USD', 'EUR'))  + "\n"
        percent_change_24h = "24H Percentage Change " + str(data[0]['percent_change_24h']) + "%\n"
        nb_news_article =  "News article nb: " + str(data[0]['news_calc_24h_previous'])
        return intro + current_value_usd + current_value_eur + percent_change_24h + nb_news_article
    else:
        return "Something went wrong :("
    
def get_symbol(coin_name):
    with open("cryptocurrencies.json") as json_file:
        crypto = json.load(json_file)
    crypto = {value : key for (key, value) in crypto.items()}
    return crypto.get(coin_name)
from currency_converter import CurrencyConverter
from web3 import Web3
from sys import argv
import requests
import decimal
import config
import json


c = CurrencyConverter()
http_provider = Web3.HTTPProvider(config.ALCHEMY_POLYGON_MAINNET)
w3 = Web3(http_provider)


def getsKlimaBalance(address):
    """ Get the config.ADRRESS sKlima Balance """
    sKlima = declareToken()
    sKlima_balance_wei = sKlima.functions.balanceOf(address).call()
    sKlima_balance = w3.fromWei(sKlima_balance_wei, 'gwei')
    return sKlima_balance


def declareToken():
    """ Return the declared Token to call functions.balanceOf """
    return w3.eth.contract(address=config.sKLIMA_TOKEN_ADDRESS,
                           abi=config.sKLIMA_ABI)


def getKlimaPrice():
    """ Return the actual USDc price of Klima """
    URL = config.API_SUSHISWAP + '?chainID=137&action=get_pair&pair=' + \
        config.USDC_KLIMA_PAIR_SUSHISWAP
    req = requests.get(URL).text
    price = json.loads(req)
    klima_price = price[0]['Token_1_price']
    return decimal.Decimal(float(klima_price))


def main(address):
    """ Get the config.ADRRESS sKlima Balance
            declareToken
        Get the current Klima price

        Return the value of the sKlima balance in USD
    """
    balance_sKlima = getsKlimaBalance(address)
    klimaPrice = getKlimaPrice()

    klima_usd = '{} USD'.format(int(balance_sKlima * klimaPrice))
    klima_eur = '{} EUR'.format(
        int(c.convert((balance_sKlima * klimaPrice), 'USD', 'EUR')))

    print(klima_usd)
    print(klima_eur)


if __name__ == "__main__":
    if w3.isAddress(argv[1]):
        price = main(argv[1])
    else:
        print('Not a correct polygon address')

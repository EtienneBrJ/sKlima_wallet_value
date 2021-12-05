from web3 import Web3
from sys import argv
from datetime import datetime
from pymongo import MongoClient
import requests
import config
import json

client = MongoClient(
    'mongodb+srv://titi:kaq9f92QNKfMUsx@cluster0.xfvlr.mongodb.net/KlimaDAO?retryWrites=true&w=majority')
db = client.KlimaDAO
http_provider = Web3.HTTPProvider(config.ALCHEMY_POLYGON_MAINNET)
w3 = Web3(http_provider)


def getsKlimaBalance():
    """ Get the config.ADRRESS sKlima Balance """
    sKlima = declareToken()
    sKlima_balance_wei = sKlima.functions.balanceOf(
        config.WALLET_PUBLIC_ADDRESS).call()
    sKlima_balance = w3.fromWei(sKlima_balance_wei, 'gwei')
    return float(sKlima_balance)


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
    return float(klima_price)


def main():
    """ Get the config.ADRRESS sKlima Balance
            declareToken
        Get the current Klima price

        Return the value of the sKlima balance in USD
    """
    balance_sKlima = getsKlimaBalance()
    klimaPrice = getKlimaPrice()

    klima_usd = int(balance_sKlima * klimaPrice)
    date_now = datetime.now().replace(microsecond=0)

    return (balance_sKlima, klima_usd, date_now)


if __name__ == "__main__":
    balance, usd_value, date = main()
    sKlimaValue = {
        'balance_sKlima': balance,
        'usd_value': usd_value,
        'date': date
    }
    inserted_value = db.sKlimaWallet.insert_one(sKlimaValue)
    print('Created {}'.format(inserted_value.inserted_id))

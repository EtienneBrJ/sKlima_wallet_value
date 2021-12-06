"""
    sKlima Wallet Value - The stacked token of KlimaDAO

    Script that track the current value of config.WALLET_PUBLIC_ADDRESS
    Priced on SushiSwap USDC/Klima pair

    Insert into MongoDB collection:
        - balance ok sKlima,
        - Usd value,
        - Date of the insertion 
"""
from dotenv import load_dotenv
from web3 import Web3
from sys import argv
from datetime import datetime
from pymongo import MongoClient
import requests
import config
import json
import os

load_dotenv()
client = MongoClient(
    'mongodb+srv://titi:' + os.environ.get('password') + '@cluster0.xfvlr.mongodb.net/KlimaDAO?retryWrites=true&w=majority')
db = client.KlimaDAO
http_provider = Web3.HTTPProvider(config.ALCHEMY_POLYGON_MAINNET)
w3 = Web3(http_provider)


def getsKlimaBalance():
    """ Get the sKlima balance of the address specified in config.py """
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
    """ Get the sKlima balance of the address specified in config.py
        Get the current usd price of Klima

        Return a tupple with balance (float), usd_value (int), date (date)
    """
    balance_sKlima = getsKlimaBalance()
    klimaPrice = getKlimaPrice()

    klima_usd = int(balance_sKlima * klimaPrice)
    date_now = datetime.now()
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

""" Graph module

    Iterate in a MongoDB collection and save the date and the price in two separate arrays
    Generate a plot with these arrays and save it as an image in the static folder
    ...
"""
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import pymongo
import os

load_dotenv()


client = pymongo.MongoClient(
    'mongodb+srv://titi:' + os.environ.get('password') + '@cluster0.xfvlr.mongodb.net/KlimaDAO?retryWrites=true&w=majority')
db = client.KlimaDAO
sKlimaCol = db.sKlimaWallet


def getPlot():

    x_data = []
    y_data = []
    ite = 0

    for document in sKlimaCol.find({}, {'_id': 0}):
        ite += 1
        x_data.append(ite)
        y_data.append(document.get('usd_value'))

    x = np.array(x_data)
    y = np.array(y_data)
    plt.plot(x, y)
    plt.savefig('static/sKlimaPlot.png')

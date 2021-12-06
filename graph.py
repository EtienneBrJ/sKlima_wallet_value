""" Graph module
    ...
    ...
"""
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import pymongo
import os

load_dotenv()

x_data = []
y_data = []

client = pymongo.MongoClient(
    'mongodb+srv://titi:' + os.environ.get('password') + '@cluster0.xfvlr.mongodb.net/KlimaDAO?retryWrites=true&w=majority')
db = client.KlimaDAO
sKlimaCol = db.sKlimaWallet

for document in sKlimaCol.find({}, {'_id': 0}):
    # Put in two list separately the date and the usd_value to display a graph
    print(document.get('date'))
    x_data.append(document.get('date'))
    y_data.append(document.get('usd_value'))


x = np.array(x_data)
y = np.array(y_data)

plt.plot(x, y)
plt.show()

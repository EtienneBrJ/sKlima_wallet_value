from flask import config, render_template
from graph import getPlot
from flask import Flask
import config


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/graph')
def graph():
    return render_template('graph.html', plot=getPlot(), address=config.WALLET_PUBLIC_ADDRESS)

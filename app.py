from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests, re
import getdata

app = Flask(__name__)

@app.route('/')
def index():
    getdata.startSession()
    return render_template('index.html')

@app.route('/data/', methods=['POST'])
def data():
    dateInput = request.form['dateInput']
    peopleInput = request.form['peopleInput']
    return str(getdata.getByDate("2017-07-05", "1"))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

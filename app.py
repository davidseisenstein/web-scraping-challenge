# import dependencies

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
#from splinter import Browser
from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

# Use pymongo to set up mongo connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars

@app.route("/")
def index():
    mars_data = db.marsdata.find_one(sort=[( '_id', pymongo.DESCENDING )])
    print(mars_data)
    return render_template("index.html", data = mars_data)

@app.route("/scrape")
def scraper():
    mars_data = scrape_mars.scrape()
    db.marsdata.insert_one(mars_data)
    return redirect("/", code=302)

if __name__ == '__main__':
    app.run(debug=True)
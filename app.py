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
    mars_data = db.mars.find_one()
    return render_template("index.html", mars_data = mars_data)

@app.route("/scrape")
def scraper():
    mars = db.mars
    mars_data = scrape_mars.scrape()
    db.marsdata.insert_one(mars_data)
    return redirect("/", code=302)

if __name__ == '__main__':
    app.run(debug=True)
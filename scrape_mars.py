def scrape():

    import pandas as pd
    import numpy as np
    from bs4 import BeautifulSoup
    import requests
    #from splinter import Browser
    from flask import Flask, render_template, redirect
    import pymongo
    import scrape_mars
    # Instantiate the dictionary that we will return
    return_dict = {}
    # Scrape nasa mars site
    url = 'http://mars.nasa.gov/news'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Collect the latest news title from the soup object

    news_title = soup.find_all('div', class_='content_title')[0].a.text.strip()
    news_paragraph = soup.find_all('div', class_='rollover_description_inner')[0].text.strip()

    #Append the data to the return dictionary
    return_dict['news_title'] = news_title
    return_dict['news_paragraph'] = news_paragraph

    #Scrape JPL Featured Image Site for image URLs
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Fetch the URL for the image
    baseurl = 'https://www.jpl.nasa.gov'

    # I feel like there is an easier way to do this part, but it worked. Oh, i was supposed to use splinter.
    relativeurl = soup.find_all('article', class_='carousel_item')[0]['style'].split(' ')[1].split('(')[1].replace("'", '').replace(")", '').replace(";", '')

    featured_image_url = baseurl + relativeurl

    #Append the data to the return dictionary
    return_dict['featured_image_url'] = featured_image_url

    # Scrape mars facts table using Pandas

    url = 'https://space-facts.com/mars/'
    response = requests.get(url)

    facts_table = pd.read_html(url)[0]
    # convert the table into an HTML string with Pandas

    facts_html = facts_table.to_html()

    #Append the data to the return dictionary
    return_dict['facts_html'] = facts_html

    # Pull the High Res images of Mar's Hemisphere from USGS
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    hemi_soup = soup.find_all('a', class_='itemLink product-item')

    base_url = 'https://astrogeology.usgs.gov/'
    hemis_list = []

    #let's loop through and create our dictionary
    for hemi in hemi_soup:
        hemi_name = hemi.h3.text.replace('Enhanced','').strip()
        image_page = base_url + hemi['href']
        print(hemi_name, image_page)
        hemi_dict = {}
        hemi_dict['title'] = hemi_name
        hemi_dict['img_url'] = image_page
        
        hemis_list.append(hemi_dict)

    return_dict['hemis_list'] = hemis_list
    return return_dict
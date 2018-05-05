#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  4 08:49:28 2018

@author: guirlynolivar
"""

import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def getLatestNews():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    titles = soup.find_all('div',class_='content_title')
    news_title = titles[0].text.strip() 
    paragraphs = soup.find_all('div',class_='rollover_description_inner')
    news_p = paragraphs[0].text.strip()
    browser.quit()
    return (news_title,news_p)


def getFeaturedImage():
    browser = init_browser()
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #click on the url link of the Featured
    browser.find_option_by_text('Featured').first.click() 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # get the featured article
    art = soup.find_all('h1',class_='media_feature_title')
    featured_article = art[0].text.strip()
    # get the list of article titles and respective images for all featured article
    title_img = []
    for x in range(1,5):
        listelement = soup.find_all('a', class_='fancybox')
        for li in listelement:
            title_img.append ({'title':li['data-title'],
                           'img': li['data-fancybox-href']})
        if browser.find_by_name('More'):
            browser.find_by_name('More').first.click()

    base_featured_url = "https://www.jpl.nasa.gov"
    # get the image for the featured article
    for n in title_img:
        if n['title'] == featured_article:
            featured_image_url = base_featured_url + n['img']
            break
    browser.quit()
    return(featured_article,featured_image_url)

def getMarsWeather():
    browser = init_browser()
    twitter_url = 'https://twitter.com/marswxreport?lang=e'
    browser.visit(twitter_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')    
    tweets = soup.find_all('p',class_='TweetTextSize')
    mars_weather = tweets[0].text
    browser.quit()
    return(mars_weather)


def getMarsFacts():
    browser = init_browser()
    url = 'http://space-facts.com/mars/'
    tables = pd.read_html(url)    
    facts = tables[0]
    facts.columns = (['fact','value'])
    facts.set_index('fact', inplace=True)
    mars_facts = facts.to_dict()
    browser.quit()
    return(mars_facts)

def getHemispheres():
    browser = init_browser()
    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemisphere_image_urls =[]
    browser.visit(hem_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title_results = soup.find_all('h3')
    title_results
    for t in title_results:
        print(t.text.strip())    
    hemispheres = [t.text.strip() for t in title_results]
    all_img_results = soup.find_all('a',class_='itemLink product-item')
    img_results = []
    for i in all_img_results:
        if img_results == []:
            img_results.append(i['href'])
        elif img_results[-1] != i['href']:
            img_results.append(i['href'])
    # get the image after clicking each ref
    img_src = []
    count = 1
    base_hem_url = "https://astrogeology.usgs.gov"
    for i in img_results:
        ref = base_hem_url + i
        browser.visit(ref)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        browser.click_link_by_text('Sample')
        img_url = browser.windows[count].url
        count=count+1
        img_src.append(img_url)

    hemisphere_image_urls = []
    hemiz = zip(hemispheres, img_src)
    for z in hemiz:
        print(z[1])
        hemisphere_image_urls.append({'title':z[0],'img_url':z[1]})

    browser.quit()
    return(hemisphere_image_urls)



def storeMongo(news_title,news_p,featured_article,featured_image_url,mars_weather,mars_facts,hemisphere_image_urls):
    import pymongo

    # The default port used by MongoDB is 27017
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    # Define the 'classDB' database in Mongo

    db = client.marsDB
    db.marsnews.drop()
    db.marsnews.insert_one(
    {
        'news_title': news_title,
        'news_p': news_p,
        'featured_article': featured_article,
        'featured_image': featured_image_url,
        'mars_weather':mars_weather,
        'mars_facts':mars_facts,
        'hemisphere':hemisphere_image_urls
    })


def scrape():
    news_title, news_p = getLatestNews()
    time.sleep(1)
    featured_article,featured_image_url = getFeaturedImage()
    time.sleep(1)
    mars_weather = getMarsWeather()
    time.sleep(1)
    mars_facts = getMarsFacts()
    time.sleep(1)
    hemisphere_image_urls = getHemispheres()
    time.sleep(1)
    
    storeMongo(news_title,news_p,
        featured_article,featured_image_url,
        mars_weather,
        mars_facts,
        hemisphere_image_urls)
    

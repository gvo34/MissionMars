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

##
#    init_browser: 
#    initialize the browser for BeatifulSoup by first setting the path for chromedriver
##
def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


##
#    getLatestNews:
#    get the latest news titles and content from https://mars.nasa.gov/news/
#    Using beatiful soup to retrieve the main content information collect the data and return 
#   in the tuple (news_title, news_p) 
##
def getLatestNews(browser, url):
    
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    titles = soup.find_all('div',class_='content_title')
    news_title = titles[0].text.strip() 
    paragraphs = soup.find_all('div',class_='rollover_description_inner')
    news_paragraph = paragraphs[0].text.strip()
    return (news_title,news_paragraph)

##
#    getFeaturedImage:
#   Retrieve the image associated with the featured article
##
def getFeaturedImage(browser, jpl_url):
    
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
    
    return(featured_article,featured_image_url)

def getMarsWeather(browser, twitter_url):
    
    browser.visit(twitter_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')    
    tweets = soup.find_all('p',class_='TweetTextSize')
    mars_weather = tweets[0].text
    return(mars_weather)


def getMarsFacts(browser, url):
    
    tables = pd.read_html(url)    
    facts = tables[0]
    facts.columns = (['fact','value'])
    facts.set_index('fact', inplace=True)
    mars_facts = facts.to_dict()
    return(mars_facts)

def getHemispheres(browser, hem_url):
    
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
    #base_hem_url = "https://astrogeology.usgs.gov"
    base_hem_url = hem_url[0:30]
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

   
    return(hemisphere_image_urls)



def scrape():
    wbrowser = init_browser()
    mars = {}

    title,paragraph = getLatestNews(wbrowser, 'https://mars.nasa.gov/news/')
    mars["news_title"] = title
    mars["news_paragrapg"] = paragraph
    time.sleep(1)
    
    featured_article,featured_image_url = getFeaturedImage(wbrowser, 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    mars["featured_article"] = featured_article
    mars["featured_image"] = featured_image_url
    time.sleep(1)

    weather = getMarsWeather(wbrowser, 'https://twitter.com/marswxreport?lang=e')
    mars["weather"]=weather
    time.sleep(1)

    facts = getMarsFacts(wbrowser,'http://space-facts.com/mars/')
    mars["facts"]=facts
    time.sleep(1)

    hemisphere_image_urls = getHemispheres(wbrowser, 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    mars["hemispheres"] = hemisphere_image_urls
    time.sleep(1)

    wbrowser.quit()

    return mars

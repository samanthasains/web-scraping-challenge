# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 21:55:16 2020

@author: saman
"""
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import requests

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:/Users/saman/.wdm/drivers/chromedriver/win32/87.0.4280.88/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser=init_browser()
    mars_dict={}
    
    #NASA article
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    html = requests.get(url)
    nasa_soup = BeautifulSoup(html.text, 'html.parser')
    # Examine the results and look for a div withe the class 'content_title'
    results = nasa_soup.find_all('div', class_='content_title')
    # Access the thread's text content
    news_title=(results[0]).a.text
    news_title=news_title.replace('\n', '')
    # Examine the results and look for a div withe the class 'rollver_description_inner'
    results = nasa_soup.find('div', class_='rollover_description_inner').text
    text_content=results.replace('\n', '')
    
    #JPL Image
    url = 'https://www.jpl.nasa.gov/spaceimages'
    browser.visit(url)
    # HTML object
    html = browser.html
    jpl_soup = BeautifulSoup(html, 'html.parser')
    # Retrieve all elements of the button fancybox
    results = jpl_soup.find('a', class_='fancybox')
    #Save image url
    href=results.get('data-fancybox-href')
    featured_image_url=f'https://www.jpl.nasa.gov{href}'
    
    #Mars fact
    url = 'https://space-facts.com/mars/'
    #Get results
    results=pd.read_html(url)
    #Write facts table to html
    mars_facts=results[0].to_html(index=False, header=False)
    
    #Set url for astrogeology
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    # HTML object
    html = browser.html
    
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Retrieve all elements of the button fancybox
    results = soup.find_all('div', class_='item')
    
    #Define dictionary
    hemisphere_dict=[]
    
    for div in results:
        # Use Beautiful Soup's find() method to navigate and retrieve attributes
        h3 = div.find('h3')
        link = div.find('a')
        href = link['href']
        
        # Loop through image links
        try:
            #Go to web page
            browser.visit('https://astrogeology.usgs.gov' + href)
        
            #HTML object
            html=browser.html
            
            #Parse HTML with Beautiful Soup
            soup = BeautifulSoup(html, 'html.parser')
    
            #Retrieve all images
            results = soup.find('div', class_='downloads')
            image_url = results.find('li').a['href']
    
        #Create Dictionary to store title and url info
            image_dict = {}
            image_dict['title'] = h3.text
            image_dict['img_url'] = image_url
            hemisphere_dict.append(image_dict)
        
        except:
            print("Scraping Complete")

    #Write all to dictionary
    mars_dict={
        "news_title": news_title,
        "news_para": text_content,
        "featured_image_url": featured_image_url,
        "fact_table": mars_facts,
        "hemisphere_images": hemisphere_dict}
    
    # Close the browser after scraping
    browser.quit()
            

    return mars_dict
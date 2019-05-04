from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    #NASA Mars News

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #JPL Mars Space Images - Featured Image

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    img_url = soup.find('div',class_='img').find('img')['src']

    img_url = img_url.replace('wallpaper', 'largesize')
    img_url = img_url.replace('-640x350','_hires')

    featured_image_url = 'https://www.jpl.nasa.gov' + img_url

    #Mars Weather

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_tweets = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')

    for t in mars_tweets:
        tweet = t.text
        if 'low' and 'pressure' in tweet:
            mars_weather = tweet.split('pic.twit')[0]
            break

    #Mars Facts

    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)

    facts_df = tables[0]
    facts_df.columns = ['Characteristic', 'Data']
    facts_df.set_index('Characteristic', inplace=True)

    html_table = facts_df.to_html()
    
    facts_table = html_table.replace('\n', '')

    #Mars Hemispheres

    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemis = soup.find_all('div', class_='description')

    astro_url = 'https://astrogeology.usgs.gov'

    hemisphere_image_urls = []

    for h in hemis:
        source = astro_url + h.find('a')['href']
        title = (h.find('h3').text).split(' Enhanced')[0]
        
        browser.visit(source)
        
        new_html = browser.html
        new_soup = BeautifulSoup(new_html, 'html.parser')
        
        img_url = astro_url + new_soup.find('img', class_='wide-image')['src']
        
        hemisphere_image_urls.append({'title':title,'img_url':img_url})
    
    mars_dict = {
        "news_title" : news_title,
        "news_p" : news_p,
        "featured_image_url" : featured_image_url,
        "mars_weather" : mars_weather,
        "facts_table" : facts_table,
        "hemisphere_images" : hemisphere_image_urls
    }

    browser.quit()

    return mars_dict
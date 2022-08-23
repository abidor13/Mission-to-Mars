#!/usr/bin/env python
# coding: utf-8

# In[61]:


# Import Splinter and BeautifulSoup
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager


# In[62]:


# set the executable path then set up the URL:
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[63]:


# Assign the mars nasa news site url and instruct the browser to visit it:
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[64]:


# Set up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[65]:


# Begin Scraping
slide_elem.find('div', class_='content_title')


# In[66]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[67]:


# There are two methods used to find tags and attributes with BeautifulSoup:

# .find() is used when we want only the first class and attribute we've specified.
# .find_all() is used when we want to retrieve all of the tags and attributes.
# For example, if we were to use .find_all() instead of .find() when pulling the summary, 
# we would retrieve all of the summaries on the page instead of just the first one.


# In[68]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[69]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[70]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[71]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[72]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[73]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[74]:


# Scrape the entire table with Pandas' .read_html() function.

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[75]:


#  Convert our DF back into HTML-ready code using the .to_html()
df.to_html()


# In[76]:


browser.quit()


# In[77]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[78]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[79]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[80]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[81]:


slide_elem.find('div', class_='content_title')


# In[82]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[83]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[84]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[85]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[86]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[87]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[88]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[89]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[90]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[91]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[92]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[93]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for i in range(4):
    
    # Create a dictionary to hold each image and title.
    hemispheres = {}
    
    # Find the HTML tag that holds all the links to the full-resolution images.
    browser.find_by_tag('h3')[i].click()

    # Get the image URL.
    img_url_rel = browser.links.find_by_text('Sample').first
    hemispheres['img_url'] = img_url_rel['href']
    
    # Get the title.
    title = browser.find_by_css('h2.title').text
    hemispheres['title'] = title

    # Add image and title dictionary to the list.
    hemisphere_image_urls.append(hemispheres)

    # Navigate back to the beginning to get the next hemisphere image.
    browser.back()


# In[94]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[95]:


# 5. Quit the browser
browser.quit()


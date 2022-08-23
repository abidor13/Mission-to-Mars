# Import Splinter and BeautifulSoup
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls = mars_hemispheres(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere_image_urls,
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Assign the mars nasa news site url and instruct the browser to visit it:
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # Set up the HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    

    try:
        
        # Begin Scraping
        slide_elem = news_soup.select_one('div.list_text')


        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
    
        # There are two methods used to find tags and attributes with BeautifulSoup:
        # .find() is used when we want only the first class and attribute we've specified.
        # .find_all() is used when we want to retrieve all of the tags and attributes.
        # For example, if we were to use .find_all() instead of .find() when pulling the summary, 
        # we would retrieve all of the summaries on the page instead of just the first one.


        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None    


    return news_title, news_p

# ### Featured Images
def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')


    try:
    # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    
    return img_url


# Scrape the entire table with Pandas' .read_html() function.

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")


### Hemispheres Scraping

def mars_hemispheres(browser):

    # Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Write code to retrieve the image urls and titles for each hemispheres.
    # Loop through to get 4 different images
    for i in range(4):
    
        hemispheres = {}
        browser.find_by_tag('h3')[i].click()
        img_url_rel = browser.links.find_by_text('Sample').first
        hemispheres['img_url'] = img_url_rel['href']
        title = browser.find_by_css('h2.title').text
        hemispheres['title'] = title  
        hemisphere_image_urls.append(hemispheres)
        browser.back()

    return hemisphere_image_urls

# if __name__ == "__main__":

#     # If running as script, print scraped data
#     print(scrape_all())


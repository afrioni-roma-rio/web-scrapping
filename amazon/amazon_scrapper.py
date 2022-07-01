from selenium import webdriver
from selenium.webdriver.edge.service import Service
from bs4 import BeautifulSoup
import urllib.parse
import time
import os
import pandas as pd
import numpy as np

## Keyword
keyword = str(input("Please insert a keyword!"))
q = urllib.parse.quote(keyword)

## Path, options and driver for Edge
PATH = os.getcwd() + "\msedgedriver.exe"
service = Service(PATH)
op = webdriver.EdgeOptions()
op.add_argument('--ignore-certificate-errors')
op.add_argument('--incognito')
# op.add_argument('--headless')
driver = webdriver.Edge(service=service, options=op)

## Maximize browser
driver.maximize_window()

## Browse page
driver.get(f"https://www.amazon.com/s?k={q}")


driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")


## Get maximum page
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(3)
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'lxml')
pagination = soup.find('div', class_= "a-section a-text-center s-pagination-container")
max_page = pagination.find(class_= "s-pagination-item s-pagination-disabled").get_text()

print('max page:', max_page)

product_name_list = []
image_link_list = []
rating_list = []
no_of_review_list = []
min_price_list = []
max_price_list = []
product_price = [] # if multiple price, take the median (max + min)/2

## Section types in amazon website
# list[0]= product name 
# list[1]= image link
section_dic = {
                'a-section':['a-size-medium a-color-base a-text-normal', 's-image'],
                'a-section a-spacing-base': ['a-size-base-plus a-color-base a-text-normal', 's-image'],
                'a-section sbv-product' : ['a-size-medium a-color-base a-text-normal', 'sbv-product-img']
        }

for page in range(1,int(max_page)+1):
    driver.get(f"https://www.amazon.com/s?k={q}&page={page}")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(2)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')

    for section in section_dic:

        product_section = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == section.split()) # create list from string with space
        
        for i in range(len(product_section)):
                ## product name and image
                try:
                        section_dic.get(section)[0].split() 
                        product_name = product_section[i].find(lambda tag: tag.name == 'span' and tag.get('class') == section_dic.get(section)[0].split() )
                        product_name = product_name.get_text()
                except Exception as e: 
                        product_name = np.nan  
                product_name_list.append(product_name)

                try:
                        product_image = product_section[i].find(lambda tag: tag.name == 'img' and tag.get('class') == section_dic.get(section)[1].split())['src']
                except Exception as e:
                        product_image = np.nan 
                image_link_list.append(product_image)


                ## product rating
                try:
                        product_rating = product_section[i].find(class_='a-icon-alt')
                        product_rating = product_rating.get_text()
                        product_rating = product_rating.split(' ', 1)[0]
                        product_rating = float(product_rating)

                except Exception as e:
                        product_rating = np.nan

                try:
                        no_of_review = product_section[i].find(class_='a-size-base s-underline-text').get_text()
                        no_of_review = int(no_of_review.replace(',', ''))

                except Exception as e:
                        no_of_review = np.nan

                rating_list.append(product_rating)
                no_of_review_list.append(no_of_review)

                ## product price

                cek_price_range = product_section[i].find(lambda tag: tag.name == 'span' and tag.get('class') == ["a-price-range"])
                if cek_price_range != None:
                        price_range = cek_price_range.find_all(lambda tag: tag.name == 'span' and tag.get('class') == ["a-price"])
                        min_price = price_range[0].find(class_='a-offscreen').get_text()
                        min_price = float(min_price[1:].replace(',', ''))

                        max_price = price_range[1].find(class_='a-offscreen').get_text()
                        max_price = float(max_price[1:].replace(',', ''))
                        median_price = round((min_price + max_price) / 2,2) 

                        min_price_list.append(min_price)
                        max_price_list.append(max_price)
                        product_price.append(median_price)

                else:
                        try:
                                price = product_section[i].find(lambda tag: tag.name == 'span' and tag.get('class') == ["a-price"])
                                price = price.find(class_='a-offscreen').get_text()
                                price = float(price[1:].replace(',', ''))
                        except Exception as e:
                                price = np.nan
                        
                        min_price_list.append(price)
                        max_price_list.append(price)
                        product_price.append(price)

## Save data to csv using data-frame
df = pd.DataFrame({'product_name': product_name_list, 'product_image': image_link_list, 'product_rating': rating_list, 
                'no_of_review': no_of_review_list, 'min_price': min_price_list, 'max_price': max_price_list, 'price': product_price })

df['currency'] ='USD'
df = df[~df['product_name'].isnull()] ## drop null product name
file_path = os.getcwd()
df.to_csv(f'{file_path}\\amazon\\{keyword}.csv', index = False)


driver.quit()

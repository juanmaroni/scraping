'''
Source: http://books.toscrape.com/
It is a sandbox for web scraping.

The script gets and prints to console the data from the bookstore catalogue pages
(http://books.toscrape.com/catalogue/)
'''

from typing import Dict
import requests
from bs4 import BeautifulSoup

Response = requests.models.Response

# For the rating system, the bookstore uses classes named after the name of the rating number
# and I use a dict to convert them to numbers (string type)
RATINGS_BY_CLASSNAME: Dict = {'One': '1',
                              'Two': '2',
                              'Three': '3',
                              'Four': '4',
                              'Five': '5'}
                            
print('Title\tPrice (£)\tIn stock\tRating (1-5)\tCover image URL')

n_products: int = 0
page: int = 1
page_url: str = f'http://books.toscrape.com/catalogue/page-{page}.html'
resp: Response = requests.get(page_url)

while resp.status_code == 200:
    bs: BeautifulSoup = BeautifulSoup(resp.text, 'html.parser')
    article_product_pod = bs.findAll('article', class_='product_pod')

    for book in article_product_pod:
        # Book title
        title: str = book.find('h3').find('a').get('title')

        # Price (in pounds) and Stock (Y/N)
        div_price_stock = book.find('div', class_='product_price')
        price: str = div_price_stock.find('p', class_='price_color').text[2:]
        stock: str = 'Yes' if div_price_stock.find('p', class_='instock').text.strip() == 'In stock' else 'No'

        # Rating
        rating: str = RATINGS_BY_CLASSNAME[book.find('p').get('class')[1]]

        # Image URL
        img_url: str = book.find('div', class_='image_container').find('a').find('img').get('src')

        # Print formatted data
        print(f'{title}\t{price}\t{stock}\t{rating}\t{img_url}')
        n_products += 1
    
    page += 1
    page_url = f'http://books.toscrape.com/catalogue/page-{page}.html'
    resp = requests.get(page_url)

print(f'\nTotal number of books: {n_products}\n')

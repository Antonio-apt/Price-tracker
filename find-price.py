import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import re
load_dotenv()


URL = 'https://www.americanas.com.br/busca/'

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}

#print(soup.prettify())

#titles = soup.findAll("h3", {"class": "card-product-name"})

def extract_infos(product_cards):
    products = []
    
    for div in product_cards:
        indexes = {}
        href = div.get('href')
        scope = div.find("div",{"class":"Info-bwhjk3-5 gWiKbT ViewUI-sc-1ijittn-6 iXIDWU"})
        title = scope.find("h2",{"class": "TitleUI-bwhjk3-15 khKJTM TitleH2-sc-1wh9e1x-1 gYIWNc"}).get_text()
        price = scope.find("span", {"class": re.compile("PriceUI-bwhjk3-11*")}).get_text()
        indexes['link'] = href
        indexes['title'] = title
        indexes['price'] = price
        products.append(indexes)
    
    return products

def show_products(product_infos):
    print(max(product_infos, key=len))
    for (indice, product) in enumerate(product_infos, start=1):
        print('-----------------------------------------------')
        print(f'{indice}. - {product["title"]}')
        print(product['price'])

def menu

while True:
    search = input('O que você deseja encontrar: ')
    search.lower().replace(' ', '-')

    URL = URL + search
    print (URL)
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup.title)
    titles = soup.findAll("a", {"class": "Link-bwhjk3-2 iDkmyz TouchableA-p6nnfn-0 joVuoc"})
    products = extract_infos(titles)
    show_products(products)








    
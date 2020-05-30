import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
#import threading
import re
from checker_price import checker 
import select_database as sd
load_dotenv()

URL = 'https://www.americanas.com.br/busca/'

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}

#process = threading.Thread(target=checker, args=(headers))
#process.start()

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
    for (indice, product) in enumerate(product_infos, start=1):
        print('-----------------------------------------------')
        print(f'{indice}. - {product["title"]}')
        print(product['price'])

def interface(*args):
    options = []
    for elem in args:
        options.append(elem)
    size = len(max(options, key=len)) + 4
    print(('-')*(size+2))
    print('|'+((' ')*size)+'|')
    for elem in args:
        if len(elem) < size:
            spaces = (size-len(elem)) - 2
            print('|  ' + elem + ((' ')*spaces) + '|')
        else:
            print(f'|  {elem}  |')
    print('|'+((' ')*size)+'|')
    print(('-')*(size+2))


def search_products_menu():
        search = input('O que você deseja encontrar: ')
        search = search.lower().replace(' ', '-')

        print (URL + search)
        page = requests.get(URL + search, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        print(soup.title)
        titles = soup.findAll("a", {"class": "Link-bwhjk3-2 iDkmyz TouchableA-p6nnfn-0 joVuoc"})
        if titles:
            products = extract_infos(titles)
            show_products(products)
            def internal_menu():
                interface('O que deseja fazer:', '1. Acompanhar produto','2. Fazer outra busca','3. Voltar ao menu')
                try:
                    answer = int(input(' Digite uma opção: '))
                except ValueError as e:
                    print('valor invalido', e)
                else:
                    if(answer == 1):
                        while True:
                            try:
                                selected_product = int(input(' Digite o indice do produto: '))
                            except ValueError as e:
                                print('valor invalido', e)
                            else:
                                if selected_product in range(1, (len(products)+1)):
                                    email = input(' Digite seu email: ')
                                    if(re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email)):
                                        email = {'email': email}
                                        products[selected_product-1].update(email)
                                        sd.insert(products[(selected_product-1)])
                                    else:
                                        print('Email Invalido')
                                        input("Press Enter to return...")
                                    break
                                else:
                                    print('Indice invalido')
                                    continue
                        internal_menu()
                    if(answer == 2):
                        search_products_menu()
                    if(answer == 3):
                        pass
                    else:
                        print('Resposta invalida')
                        input("Press Enter to continue...")
                        internal_menu()
            internal_menu()
        else:
            print('Houve um erro ao pesquisar')
            input("Press Enter to continue...")
            search_products_menu()

while True:
        interface('Tracker de preços','1. Ver produtos selecionados','2. Pesquisar novo produto',
                '3. Dados estatisticos', '4. Limpar produtos', '5. Fechar programa')
        try: 
            answer = int(input(' Digite uma opção: '))
        except ValueError as e:
            print('valor invalido', e)
        else:
            if(answer == 1):
                save_products = sd.show_selected_products()
                for i in save_products:
                    print(i)
                input("Press Enter to continue...")
            elif(answer == 2):
                search_products_menu()
            elif(answer == 3):
                print('Dados estatiscos dos valores salvos: ')
                sd.analysis()
                input("Press Enter to continue...")
            elif(answer == 4):
                sd.clear()
                input("Press Enter to continue...")
            elif(answer == 5):
                print("Obrigado")
                break
            else:
                print("Valor invalido")
                input("Press Enter to continue...")








    
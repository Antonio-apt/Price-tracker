import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
#import threading
import re
from checker_price import checker 
import select_database as sd
from prettytable import PrettyTable
import logging

URL = 'https://www.americanas.com.br/busca/'

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}

def extract_infos(product_cards):
    products = []
    
    for div in product_cards:
        indexes = {}
        href = div.get('href')
        scope = div.find("div",{"class":"Info-bwhjk3-5 gWiKbT ViewUI-sc-1ijittn-6 iXIDWU"})
        title = scope.find("h2",{"class": re.compile("TitleUI-bwhjk3-15 khKJTM*")}).get_text()
        price = scope.find("span", {"class": re.compile("PriceUI-bwhjk3-11*")}).get_text()
        indexes['link'] = href
        indexes['title'] = title
        indexes['price'] = price
        products.append(indexes)
    return products

def show_products(product_infos):
    tabela = PrettyTable(["Indice", "Produto", "Preço"])
    tabela.padding_width = 1
    tabela.align["Produto"] = "l"
    tabela.align["Preço"] = "l"
    for (indice, product) in enumerate(product_infos, start=1):
        tabela.add_row([indice, product['title'], product['price']])
    print(tabela)

def internal_menu(products):
    menu = PrettyTable()
    menu.add_column('O que deseja fazer:', ["1. Acompanhar produto", "2. Voltar ao menu"])
    menu.align["O que deseja fazer:"] = "l"
    print(menu)
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
                        if(re.search('\w+[.|\w]\w+@\w+[.]\w+[.|\w+]\w+', email)):
                            email = {'email': email}
                            products[selected_product-1].update(email)
                            sd.insert(products[(selected_product-1)])
                            break
                        else:
                            print('Email Invalido')
                            input("Press Enter to return...")
                            break
                    else:
                        print('Indice invalido')
                        continue
            return
        if(answer == 2):
            pass
        else:
            print('Resposta invalida')
            input("Press Enter to continue...")


def search_products_menu():
        search = input('O que você deseja encontrar: ')
        search = search.lower().replace(' ', '-')

        print (URL + search)

        try:
            page = requests.get(URL + search, headers=headers)
        except Exception as e:
            logging.error("Exception in _query: %s" % e)
        
        soup = BeautifulSoup(page.content, 'html.parser')
        print(soup.title)
        titles = soup.findAll("a", {"class": "Link-bwhjk3-2 iDkmyz TouchableA-p6nnfn-0 joVuoc"})
        if titles:
            products = extract_infos(titles)
            show_products(products)
            return products
        else:
            print('Houve um erro ao pesquisar')
            input("Press Enter to continue...")
    
def main_menu():
    while True:
        menu = PrettyTable()
        menu.add_column("Tracker de preços:", ["1. Ver produtos selecionados", "2. Pesquisar novo produto", "3. Voltar ao menu", "3. Dados estatisticos",
                        "4. Limpar produtos", "5. Fechar programa"])
        menu.align["Tracker de preços:"] = "l"
        print(menu)
        try: 
            answer = int(input(' Digite uma opção: '))
        except ValueError as e:
            print('valor invalido', e)
        else:
            if(answer == 1):
                save_products = sd.show_selected_products()
                tabela = PrettyTable(["Produto", "Preço", "Email"])
                tabela.padding_width = 1
                for i in save_products:
                    tabela.add_row([i[0], i[1], i[2]]) 
                print(tabela)
                input("Press Enter to continue...")
            elif(answer == 2):
                products = search_products_menu()
                internal_menu(products)
            elif(answer == 3):
                print('Dados estatiscos dos valores salvos: ')
                sd.analysis()
                input("Press Enter to continue...")
            elif(answer == 4):
                sd.clean()
                input("Press Enter to continue...")
            elif(answer == 5):
                print("Obrigado")
                break
            else:
                print("Valor invalido")
                input("Press Enter to continue...")


main_menu()








    
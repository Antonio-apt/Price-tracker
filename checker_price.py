import requests
import re
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import select_database as sd
import logging
import smtplib
import time

load_dotenv()

URL = 'https://www.americanas.com.br'

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}

def float_price(price):
    price = price[2:].replace('.','').replace(',','.')
    return float(price)


def send_mail(product, new_price):
    print(os.getenv("EMAIL"))
    server = smtplib.SMTP('64.233.184.108')
    try:
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(os.getenv("EMAIL"), os.getenv("EMAIL_PASSWORD"))


        subject = "Preço diminuiu!!"
        body = f"""
            Preço diminuiu!!
            Caiu de {product[3]} para {new_price}
            Veja no link: {URL + product[1]}<
        """

        msg=f"Subject: {subject}\n\n{body}"
        server.sendmail(
            os.getenv("EMAIL"),
            product[4],
            msg.encode("utf8") 
        )

        print("Email has been sent")
    except Exception as e:
        print(e)
    finally:
        server.quit()

def checker():
    
        products = sd.show_selected_products()
        for i in products:
            try:
                page = requests.get(URL + i[1], headers=headers)
            except Exception as e:
                logging.error("Exception: %s" % e)
            else:
                soup = BeautifulSoup(page.content, 'html.parser')
                price = soup.find('span', {"class": re.compile("price*")}).get_text()
                if not price:
                    price = soup.find('span', {"class": re.compile("sales-price")}).get_text()
                price = float_price(price)

                if(price<i[3]):
                    send_mail(i,price)
                    sd.update(i[0], price)
                
                print(price)

while True:
    checker()
    #seconds
    time.sleep(3600)
from bs4 import BeautifulSoup
import requests

url = 'https://www.bcv.org.ve/'
response = requests.get(url)

# Verifica si la solicitud fue exitosa
def obtenerUsd():
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        div_dolar = soup.find('div', id='dolar')
        strong_tag = div_dolar.find('strong')
        priceVes = strong_tag.text[0:7]
        return priceVes
    else:
        print('La solicitud no fue exitosa')
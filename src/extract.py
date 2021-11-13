from bs4 import BeautifulSoup
import requests
import pandas as pd


def extract_data():

    # Store collect
    model_brand = []
    price = []
    year_km_color_cambio = []
    advertiser = []


    url = 'https://www.icarros.com.br/comprar/usados/sao-paulo-sp'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    html = requests.get( url, headers=headers )
    soup = BeautifulSoup(html.text, 'html.parser')

    list_model_brand = soup.find_all('h2', class_='esquerda titulo_anuncio')

    # model, brand, motor
    for i in range(len(list_model_brand)):
        model_brand.append(list_model_brand[i].get_text())


    # price
    list_price = soup.find_all('h3', class_='direita preco_anuncio')

    for i in range(len(list_price)):
        price.append(list_price[i].get_text())


    # All car data
    car_data = soup.find_all('div', class_='dados_veiculo')

    for i in range(len(car_data)):
        year_km_color_cambio.append(car_data[i].get_text())


    # Car advertiser
    car_advertiser = soup.find_all('div', class_='dados_anunciante')

    for i in range(len(car_advertiser)):
        advertiser.append(car_advertiser[i].get_text())

    # To Dataframes
    data = pd.DataFrame([model_brand, price, year_km_color_cambio, advertiser]).T
    data.columns = ['model_brand', 'price', 'year_km_color_cambio', 'advertiser']

    print('1: EXTRACT OK')
    return data
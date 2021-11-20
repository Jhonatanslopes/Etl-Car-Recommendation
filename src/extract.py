from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import logging


def extract_data():

    # -- Logging
    path = 'C:/Users/Jhonatans/projects/ETL/Etl-Car-Recommendation/'
    if not os.path.exists(path + 'logs'):
        os.makedirs(path + 'logs')

    logging.basicConfig(
        filename= path + 'logs/etl_icarros.txt',
        level = logging.DEBUG,
        format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s -',
        datefmt= '%Y-%m-%d %H:%M:%S'
    )

    logger = logging.getLogger('etl_icarros')

    # -- Store data
    model_brand = []
    price = []
    year_km_color_cambio = []
    advertiser = []

    # -- Enter 2 pag
    for pag in range(1, 3):

        if pag == 1:
            url = 'https://www.icarros.com.br/comprar/usados/sao-paulo-sp'

        else:
            url = f'https://www.icarros.com.br/ache/listaanuncios.jsp?bid=1&app=20&sop=nta_17|44|51.1_-kmm_1.1_-est_SP.1_-cid_9668.1_-rai_50.1_-esc_2.1_-sta_1.1_&pas=1&lis=0&pag={pag}&ord=22'

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.text, 'html.parser')


        # -- Collect model, brand, motor
        list_model_brand = soup.find_all('h2', class_='esquerda titulo_anuncio')

        for i in range(len(list_model_brand)):
            model_brand.append(list_model_brand[i].get_text())
            logger.debug('URL: %s Value: %s', url, i)


        # -- Collect price
        list_price = soup.find_all('h3', class_='direita preco_anuncio')

        for i in range(len(list_price)):
            price.append(list_price[i].get_text())
            logger.debug('URL: %s Value: %s', url, i)


        # -- Collect car data
        car_data = soup.find_all('div', class_='dados_veiculo')

        for i in range(len(car_data)):
            year_km_color_cambio.append(car_data[i].get_text())
            logger.debug('URL: %s Value: %s', url, i)


        # -- Collect car advertiser
        car_advertiser = soup.find_all('div', class_='dados_anunciante')

        for i in range(len(car_advertiser)):
            advertiser.append(car_advertiser[i].get_text())
            logger.debug('URL: %s Value: %s', url, i)


    # Parse Dataframe
    data = pd.DataFrame([model_brand, price, year_km_color_cambio, advertiser]).T
    data.columns = ['model_brand', 'price', 'year_km_color_cambio', 'advertiser']

    return data
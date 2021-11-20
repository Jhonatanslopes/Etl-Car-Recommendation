import pandas as pd
import re
from datetime import datetime
import os
import logging

def transform_data(data):

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


    # Store transormation
    car_engine = []
    km = []
    color = []
    transmission = []
    description = []


    # model_brand
    data['brand'] =  data['model_brand'].apply(lambda x: x.split(' ')[0].strip('\n').lower())
    data['model'] = data['model_brand'].apply(lambda x: x.split(' ')[1].strip('\n').lower())

    for text in data['model_brand']:

        position = text.find(' ')
        text_procured = text[position:]

        try:
            car_engine.append(re.search('(\d.\d)', text_procured).group(1).lower())

        except AttributeError:
            car_engine.append('')


    # Motor
    data['motor'] = car_engine
    data['motor'] = data['motor'].apply(lambda x: 'uninformed' if x == '' else x.replace('0 1', '1.0').replace('2 1', '2.0').replace('250', '2.5').replace('5 2', '5.2').replace('230', '2.3').replace('208', '2.0'))

    # price
    data['price'] = data['price'].apply(lambda x: x.split(' ')[1].replace('preço', ''))

    # year_km_color_cambio for year
    data['year'] = data['year_km_color_cambio'].apply(lambda x: re.search('(\d+)', x.split(' ')[0].strip()).group(1))

    # advertiser
    data['district'] = data['advertiser'].apply(lambda x: x.strip().replace('\n\n', '\n').split('\n')[0].lower())

    data['city'] = data['advertiser'].apply(lambda x: x.strip().replace('\n\n', '\n').split('\n')[1].lower())
    data['state'] = 'sp'


    for i in data['year_km_color_cambio']:

        position_km = i.rfind('Km')
        position_color = i.rfind('Cor')

        km.append(i[position_km:position_color].replace(' ', '').replace('\n', '').replace('Km', ''))
        color.append(i[position_color:].replace('\n', ' ').split('  ')[0].lower())

        try:
            transmission.append(i[position_color:].replace('\n', ' ').split('  ')[1].lower())

        except IndexError:
            regex = bool(re.search('auto\w.\w+', i))

            if regex == True:
                transmission.append('automático')

            else:
                transmission.append('manual')

        try:
            description.append(i[position_color:].replace('\n', ' ').split('  ')[2].lower())

        except IndexError:
            description.append(i[position_color:].replace('\n', ' '))

    data['km']  = km
    data['color']  = color
    data['transmission']  = transmission
    data['advertiser_description'] = description

    logger.info('Dados derivados OK')

    # Clean color and transmission
    data['color'] = data['color'].apply(lambda x: x.replace('cor ', ''))
    data['transmission'] = data['transmission'].apply(lambda x: x.replace('câmbio ', ''))

    # Drop columns
    data.drop(columns=['model_brand', 'advertiser', 'year_km_color_cambio'], inplace=True)

    # -- Change type
    data['price'] = data['price'].apply(lambda x: x.replace('.', '').replace(',', '.')).astype('float')
    data['km'] = data['km'].apply(lambda x: x[:6] if len(x) > 8 else x).astype('float')
    logger.info('Mudanca de tipos OK')

    # date scrapy
    date_now = datetime.now().strftime('%Y-%m-%d')
    data['scrapy_date'] = date_now

    return data
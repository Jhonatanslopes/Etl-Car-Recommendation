import pandas as pd
import re

def transform_data(data):

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
        car_engine.append(re.search('(\d.\d)', text_procured).group(1).lower())

    data['motor'] = car_engine

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
        transmission.append(i[position_color:].replace('\n', ' ').split('  ')[1].lower())
        description.append(i[position_color:].replace('\n', ' ').split('  ')[2].lower())

    data['km']  = km
    data['color']  = color
    data['transmission']  = transmission
    data['advertiser_description'] = description

    # Drop columns
    data.drop(columns=['model_brand', 'advertiser', 'year_km_color_cambio'], inplace=True)

    # change type
    data['price'] = data['price'].apply(lambda x: x.replace('.', '').replace(',', '.')).astype('float')
    data['color'] = data['color'].apply(lambda x: x.replace('cor ', ''))
    data['transmission'] = data['transmission'].apply(lambda x: x.replace('câmbio ', ''))

    """data['motor'] = data['motor'].apply(lambda x: re.search('(d\s\d)', str(x)).group(1)[1] + '.0' if re.search('(d\s\d)', str(x)).group(1)[0] == '0' else re.search('(d\s\d)', str(x)).group(1)[0] + '.0').astype('float')"""

    data['motor'] = data['motor'].apply(lambda x: x.replace('0 1', '1.0').replace('2 1', '2.0')).astype('float')
    data['km'] = data['km'].astype('float')

    print('2: TRANSFORM OK')
    return data
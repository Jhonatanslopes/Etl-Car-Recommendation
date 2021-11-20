import sqlalchemy


def loading_data(data):

    try:
        database_username = 'root'
        database_password = 'J1l2c317171010'
        database_ip       = '127.0.0.1'
        database_name     = 'db_car'

        database_connection = sqlalchemy.create_engine(
            'mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format(
                database_username, database_password, 
                database_ip, database_name
        ))

    except ConnectionError:
        print('Connection Error')

    try:
        data.to_sql('tb_cars', con=database_connection, if_exists='append', index=False)

    except sqlalchemy.exc.InvalidRequestError:
        print('Loading Error')


    return database_connection
from extract import extract_data
from loading import loading_data
from report import send_report
from transform import transform_data
import os
import logging

def start_etl():

    # Logging
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


    # Extract
    data = extract_data()
    logger.info(' Job 1: Extract data OK')
    
    # Transform
    data = transform_data(data)
    logger.info('Job 2: Tranform data OK')

    # Loading
    conn = loading_data(data)
    logger.info('Job 3: Loading data OK')

    # Report/Send
    send_report(conn)
    logger.info('Job 4: Send Email OK')


if __name__ == '__main__':
    start_etl()
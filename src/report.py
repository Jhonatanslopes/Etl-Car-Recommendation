import win32com.client as win32
import sqlalchemy
import pandas as pd
import os
from datetime import datetime


def send_report(conn):

    try:
        date_query = str(datetime.now().strftime('%Y-%m-%d'))
        query = '''
            SELECT * FROM tb_cars
                WHERE scrapy_date = "{}"
        '''.format(date_query)

        data = pd.read_sql_query(query, conn)
        conn.dispose() 

    except sqlalchemy.exc.InvalidRequestError:
        print('SELECT Error')
   

    # Create file excel
    try:
        path = 'report/report_icarros.xlsx'
        f = open(path)
        f.close()

        os.remove(path)
        data.to_excel('report/report_icarros.xlsx', index=False)
    
    except:
        data.to_excel('report/report_icarros.xlsx', index=False)


    # Send Email
    date = datetime.now().strftime('%d-%m')
    outlook = win32.Dispatch('outlook.application')
    email = outlook.CreateItem(0)

    email.To = 'jhonatans.ti@icloud.com'
    email.Subject = f'Relatório Veículos - Icarros {date}'
    email.HTMLBody = '''
    <p>Olá,</p>

    <p>Segue em anexo, relatório dos veículos coletados do site.</p>

    <p> </p>

    <p>Atenciosamente,</p>

    <p>Jhonatans Lopes</p>

    '''

    # all path the file
    file = 'C:/Users/Jhonatans/projects/ETL/Etl-Car-Recommendation/report/report_icarros.xlsx'
    email.Attachments.Add(file)
    email.Send()
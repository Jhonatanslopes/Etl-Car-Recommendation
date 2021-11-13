import win32com.client as win32
import sqlalchemy
import pandas as pd
import os


def send_report(conn):

    try:
        query = '''
            SELECT * FROM tb_cars
        '''

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
    outlook = win32.Dispatch('outlook.application')
    email = outlook.CreateItem(0)

    email.To = 'jhonatans.ti@icloud.com'
    email.Subject = 'Etl'
    email.HTMLBody = '''
    <p>Boa noite,</p>

    <p>Segue ETL.</p>

    <p> </p>

    <p>Atenciosamente,</p>

    <p>Jhonatans Lopes</p>

    '''

    # all path the file
    file = 'C:/Users/Jhonatans/projects/ETL/car_recommendation/report/report_icarros.xlsx'
    email.Attachments.Add(file)
    email.Send()
    print('4: SEND OK')
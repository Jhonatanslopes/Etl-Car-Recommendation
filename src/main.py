from extract import extract_data
from loading import loading_data
from report import send_report
from transform import transform_data


def start_etl():
    
    data = extract_data()
    data = transform_data(data)
    conn = loading_data(data)
    send_report(conn)


if __name__ == '__main__':
    start_etl()
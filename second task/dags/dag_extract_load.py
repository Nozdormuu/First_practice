from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import psycopg2

# Настройки для подключения к Google Sheets
GOOGLE_SHEETS_CREDS = 'path/to/credentials.json'
GOOGLE_SHEETS_KEY = 'your_google_sheets_key'

# Настройки для подключения к PostgreSQL
POSTGRESQL_CONN_ID = 'your_postgresql_conn_id'

def extract_from_google_sheets():
    # Подключение к Google Sheets
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_CREDS, scope)
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_key(GOOGLE_SHEETS_KEY).sheet1

    # Получение данных из Google Sheets
    data = sheet.get_all_records()

    return data

def load_to_postgresql():
    # Подключение к PostgreSQL
    conn = psycopg2.connect(conn_id=POSTGRESQL_CONN_ID)
    cursor = conn.cursor()

    # Получение данных из Google Sheets
    data = extract_from_google_sheets()

    # Загрузка данных в PostgreSQL
    for row in data:
        cursor.execute("INSERT INTO your_table (column1, column2) VALUES (%s, %s)", (row['column1'], row['column2']))

    conn.commit()
    cursor.close()
    conn.close()

# Создание DAG с отключенным отставанием
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2021, 1, 1),
}

dag = DAG('google_sheets_to_postgresql', default_args=default_args, schedule_interval='*/1 * * * *', catchup=False)


# Определение задач DAG
extract_task = PythonOperator(
    task_id='extract_from_google_sheets',
    python_callable=extract_from_google_sheets,
    dag=dag
)

load_task = PythonOperator(
    task_id='load_to_postgresql',
    python_callable=load_to_postgresql,
    dag=dag
)

# Определение зависимостей между задачами
extract_task >> load_task

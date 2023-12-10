import psycopg2
import sys, os
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
confing_dir = os.path.dirname(project_dir)
sys.path.append(confing_dir)
from config import *

# Подключение к базе данных
connection = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

cursor = connection.cursor()

with open(f'{project_dir}/data/data.txt', 'r') as f:
    schools = [line.title().strip() for line in f]
    for school in schools:
        cursor.execute("INSERT INTO Education_Organization (Name_org) VALUES (%s)", (str(school),))

# Закрыть подключение
connection.commit()
cursor.close()
connection.close()
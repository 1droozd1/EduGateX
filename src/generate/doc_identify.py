import psycopg2, sys, os
import random
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

# Получение всех AbiturientID из таблицы Abiturient
cursor.execute("SELECT AbiturientID FROM Abiturient")
abiturients = cursor.fetchall()

# Вставка данных в Document_identifier для каждого AbiturientID
for abiturient in abiturients:
    abiturient_id = abiturient[0]

    document_data = {
        'Doc_type_ID': random.choices([1, 2, 3, 4, 5, 6], weights=[0.9, 0.08, 0.01, 0.025, 0.025, 0.025], k=1)[0],
        'series_doc': random.randint(1000, 9999),
        'number_doc': random.randint(100000, 999999),
        'date_issue': f'{random.randint(2018, 2020)}-{random.randint(1, 12)}-{random.randint(1, 28)}',
        'org_id': random.randint(1, 16496),
        'AbiturientID': abiturient_id
    }

    insert_sql = """
        INSERT INTO Document_identifier (Doc_type_ID, series_doc, number_doc, date_issue, org_id, AbiturientID)
        VALUES (%(Doc_type_ID)s, %(series_doc)s, %(number_doc)s, %(date_issue)s, %(org_id)s, %(AbiturientID)s)
    """
    cursor.execute(insert_sql, document_data)

# Закрыть подключение
connection.commit()
cursor.close()
connection.close()

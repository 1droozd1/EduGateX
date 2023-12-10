import psycopg2, sys
import random, os
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
        'Doc_type_ID': random.choices([1, 2, 3, 4], weights=[0.9, 0.09, 0.005, 0.005], k=1)[0],
        'series_doc': random.randint(1000, 9999),
        'number_doc': random.randint(100000, 999999),
        'date_issue': f'{random.randint(2018, 2020)}-{random.randint(1, 12)}-{random.randint(1, 28)}',
        'org_id': random.randint(1, 8788),
        'presence_of_original': random.choices([True, False], weights=[0.8, 0.2], k = 1)[0],
        'AbiturientID': abiturient_id
    }
    insert_sql = """
        INSERT INTO Document_education (Doc_type_ID, series_doc, number_doc, date_issue, org_id, presence_of_original, AbiturientID)
        VALUES (%(Doc_type_ID)s, %(series_doc)s, %(number_doc)s, %(date_issue)s, %(org_id)s, %(presence_of_original)s, %(AbiturientID)s)
    """
    cursor.execute(insert_sql, document_data)

# Закрыть подключение
connection.commit()
cursor.close()
connection.close()
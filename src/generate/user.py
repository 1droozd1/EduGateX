import psycopg2
import sys, os
from werkzeug.security import generate_password_hash
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

cursor.execute("SELECT AbiturientID, surname, first_name FROM Abiturient")
list_abitur = list(data for data in cursor.fetchall())
password = generate_password_hash(str(list_abitur[0][0]))
for user in list_abitur: 
    cursor.execute(
        """
        INSERT INTO User_account (username, password_user, AbiturientID)
        VALUES (%s, %s, %s)
        """, 
    (user[2] + user[1][0], password, user[0], ))

# Закрыть подключение
connection.commit()
cursor.close()
connection.close()
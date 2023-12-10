import psycopg2
import sys, csv, os
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
confing_dir = os.path.dirname(project_dir)
sys.path.append(confing_dir)

from config import *
import random

# Подключение к базе данных
connection = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

cursor = connection.cursor()

cursor.execute("SELECT COUNT(AbiturientID) FROM Abiturient")
count_abitur = int(cursor.fetchall()[0][0])

cursor.execute("SELECT COUNT(SpecialityID) FROM Specialty_for_study")
count_special = int(cursor.fetchall()[0][0])

cursor.execute("SELECT EmployeeID FROM Employee WHERE PositionID != 3")
count_emploee = [desc[0] for desc in cursor.fetchall()]

for id in range(1, count_abitur + 1):
    AbiturientID = id
    SpecialityID = random.randint(1, count_special)
    data_application = f'2023-{random.randint(6, 7)}-{random.randint(1, 30)}'
    EmployeeID = random.choices(count_emploee)[0]

    cursor.execute(
            """
            INSERT INTO Application_for_admission (AbiturientID, SpecialityID, data_application, EmployeeID)
            VALUES (%s, %s, %s, %s)
            """, 
        (AbiturientID, SpecialityID, data_application, EmployeeID,))
    
# Закрыть подключение
connection.commit()
cursor.close()
connection.close()
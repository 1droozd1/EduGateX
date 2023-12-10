import psycopg2
import sys, csv, os
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

with open(f'{project_dir}/data/programs_bak.txt', 'r') as file:
    programs = [line.strip() for line in file]
    dict_programs = {}
    for index in range(0, len(programs), 3):
        dict_programs[programs[index]] = [programs[index + 1], programs[index + 2].replace(' ', '').split("/")]

for program, value in dict_programs.items():
    if value[1][1] != '-':
        cursor.execute(
            """
            INSERT INTO Specialty_for_study (code_speciality, name_speciality, is_paid, amount_place)
            VALUES (%s, %s, %s, %s)
            """, 
            (value[0], program, True, value[1][1],))
    if value[1][0] != '-':
        cursor.execute(
            """
            INSERT INTO Specialty_for_study (code_speciality, name_speciality, is_paid, amount_place)
            VALUES (%s, %s, %s, %s)
            """, 
            (value[0], program, False, value[1][0],))
# Закрыть подключение
connection.commit()
cursor.close()
connection.close()
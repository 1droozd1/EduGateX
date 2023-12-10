'''Генерация данных для БД'''
import random
from faker import Faker
import psycopg2, sys, os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
confing_dir = os.path.dirname(project_dir)
sys.path.append(confing_dir)

from config import *

def generate_russian_phone_number():
    '''Генерирует номер телефона в формате +7(999)999-99-99'''
    phone_number = random.randint(100_0000, 999_9999)
    formatted_number = f"+7(9{random.randint(10,99)}){phone_number:07d}"
    return formatted_number

male_names = [name for name in open(f'{project_dir}/data/names/names_m.txt', encoding='utf-8').read().strip().splitlines()]
female_names = [name for name in open(f'{project_dir}/data/names/names_f.txt', encoding='utf-8').read().strip().splitlines()]
male_surname = [name for name in open(f'{project_dir}/data/names/surname_m.txt', encoding='utf-8').read().strip().splitlines()]
female_surname = [name for name in open(f'{project_dir}/data/names/surname_f.txt', encoding='utf-8').read().strip().splitlines()]
male_midnames = [name for name in open(f'{project_dir}/data/names/midnames_m.txt', encoding='utf-8').read().strip().splitlines()]
female_midnames = [name for name in open(f'{project_dir}/data/names/midnames_f.txt', encoding='utf-8').read().strip().splitlines()]

# Устанавливаем соединение с базой данных
# Подключение к базе данных
connection = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

# Создаем объект Faker для генерации данных
fake = Faker()

# Создаем курсор для выполнения SQL-запросов
cursor = connection.cursor()

# Генерируем и вставляем данные
for _ in range(5000):
    sex = random.choice(['male', 'female'])
    
    if sex == 'male':
        first_name = random.choice(male_names)
        surname = random.choice(male_surname)
        patronymic = random.choice(male_midnames)
    else:
        first_name = random.choice(female_names)
        surname = random.choice(female_surname)
        patronymic = random.choice(female_midnames)
    
    DateOfBirth = f'{random.randint(2005, 2006)}-{random.randint(1, 12)}-{random.randint(1, 28)}'
    phone = generate_russian_phone_number()
    email = fake.email()

    # SQL-запрос для вставки данных в таблицу applicants
    INSERT_QUERY = "INSERT INTO Abiturient (first_name, surname, patronymic, DateOfBirth, sex, phone, email) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(INSERT_QUERY, (first_name, surname, patronymic, DateOfBirth, sex[0], phone, email))

# Фиксируем изменения в базе данных
connection.commit()

# Закрываем соединение
connection.close()

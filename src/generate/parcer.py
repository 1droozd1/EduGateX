import requests
import json

# URL, откуда вы хотите получить данные
url = 'https://russiaedu.ru/_ajax/schools?edu_school_filter%5BschoolName%5D=&edu_school_filter%5Bfederal_district%5D=1&edu_school_filter%5Bregion%5D=&edu_school_filter%5Bdistrict%5D=&edu_school_filter%5BformType%5D=&edu_school_filter%5BownershipType%5D=&edu_school_filter%5B_token%5D=xnHnDlVDs6JbUmfiNUjLgzco6XPRidlqrmD98BlmXDs&pp=8787&pageNumber=1&direction='

# Отправка GET-запроса
response = requests.get(url)

# Проверяем, что запрос выполнен успешно
if response.status_code == 200:
    # Преобразуем данные в JSON
    data = response.json()
    
    # Извлекаем список школ
    schools = data.get('eduSchools', [])
    # Имя файла для сохранения
    filename = 'data.txt'
    
    # Открытие файла для записи
    with open(filename, 'w', encoding='utf-8') as file:
    # Перебираем школы и извлекаем названия
        for school in schools:
            school_data = school.get('data', {})
            title = school_data.get('title', '')
            # Запись данных в файл
            file.writelines(title + '\n')
else:
    print("Ошибка при выполнении запроса:", response.status_code)

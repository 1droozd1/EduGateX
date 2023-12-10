-- Запрос: Вывод абитурьентов, которые предоставили паспорт и которые предоставили свидетельство
-- о рождении
-- Выборка абитуриентов с паспортами
SELECT 
    A.first_name,
    A.surname,
    A.patronymic,
    'Паспорт' AS document_type
FROM 
    Abiturient A
JOIN 
    Document_identifier D ON A.AbiturientID = D.AbiturientID
JOIN 
    Types_Document_identifier T ON D.Doc_type_ID = T.Doc_type_ID
WHERE 
    T.Name_doc_type = 'Паспорт РФ'
UNION
-- Выборка абитуриентов со свидетельствами о рождении
SELECT 
    A.first_name,
    A.surname,
    A.patronymic,
    'Свидетельство о рождении' AS document_type
FROM 
    Abiturient A
JOIN 
    Document_identifier D ON A.AbiturientID = D.AbiturientID
JOIN 
    Types_Document_identifier T ON D.Doc_type_ID = T.Doc_type_ID
WHERE 
    T.Name_doc_type = 'Свидетельство о рождении';

-- Запрос: Вывод абитуриентов 17-летних и 18-летних
-- Абитуриенты, которым сейчас 18 лет
SELECT
    first_name,
    surname,
    patronymic,
    DateOfBirth
FROM
    Abiturient
WHERE
    EXTRACT(YEAR FROM AGE(DateOfBirth)) = 18
UNION
-- Абитуриенты, которым сейчас 17 лет
SELECT
    first_name,
    surname,
    patronymic,
    DateOfBirth
FROM
    Abiturient
WHERE
    EXTRACT(YEAR FROM AGE(DateOfBirth)) = 17;

-- Запрос: Вывод абитуриентов, которые получили документы в МВД ПО РЕСП. АДЫГЕЯ и ОТДЕЛЕНИЕМ ОФМС РОССИИ ПО РЕСП. АДЫГЕЯ В ПОС. ТУЛЬСКИЙ

-- Абитуриенты, получившие документы в 'Организация 1'
SELECT 
    A.first_name,
    A.surname,
    A.patronymic,
    A.DateOfBirth,
    A.sex,
    O.Name_org
FROM 
    Abiturient A
JOIN 
    Document_identifier D ON A.AbiturientID = D.AbiturientID
JOIN 
    Issuing_Organization O ON D.org_id = O.org_id
WHERE 
    O.Name_org = 'МВД ПО РЕСП. АДЫГЕЯ'
UNION
-- Абитуриенты, получившие документы в 'Организация 2'
SELECT 
    A.first_name,
    A.surname,
    A.patronymic,
    A.DateOfBirth,
    A.sex,
    O.Name_org
FROM 
    Abiturient A
JOIN 
    Document_identifier D ON A.AbiturientID = D.AbiturientID
JOIN 
    Issuing_Organization O ON D.org_id = O.org_id
WHERE 
    O.Name_org = 'ГУ МВД РОССИИ ПО ВОЛГОГРАДСКОЙ ОБЛ.';

-- Запрос: вывод телефонов и email абитуриентов
-- Выборка телефонов абитуриентов
SELECT 
    first_name,
    surname,
    'Телефон' AS contact_type,
    phone AS contact
FROM 
    Abiturient
WHERE 
    phone IS NOT NULL
UNION ALL
-- Выборка email абитуриентов
SELECT 
    first_name,
    surname,
    'Email' AS contact_type,
    email AS contact
FROM 
    Abiturient
WHERE 
    email IS NOT NULL;

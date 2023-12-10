-- Соединение таблицы самой с собой

-- Запрос: Найти всех абитуриентов, у которых дата рождения совпадает
SELECT 
    a1.AbiturientID AS AbiturientID_1,
    a1.first_name AS first_name_1,
    a1.surname AS surname_1,
    a2.AbiturientID AS AbiturientID_2,
    a2.first_name AS first_name_2,
    a2.surname AS surname_2,
    a1.DateOfBirth as DateOfBirth_1,
    a2.DateOfBirth as DateOfBirth_2
FROM 
    Abiturient as a1, Abiturient as a2
WHERE
    a1.DateOfBirth = a2.DateOfBirth AND a1.AbiturientID > a2.AbiturientID
ORDER BY
    a1.DateOfBirth, a1.AbiturientID;

-- Запрос: Найти документы с одинаковыми номерами, но выданные разными организациями

SELECT 
    d1.document_identifier_ID AS doc_id_1,
    d2.document_identifier_ID AS doc_id_2,
    d1.number_doc,
    d1.org_id AS org_id_1,
    d2.org_id AS org_id_2
FROM 
    Document_identifier as d1, Document_identifier as d2
WHERE 
    d1.number_doc = d2.number_doc and d1.document_identifier_ID < d2.document_identifier_ID
ORDER BY
    d1.number_doc;

-- Запрос: Найти всех однофамильцев в таблице Abiturient
SELECT
    a1.AbiturientID as first_id,
    a1.first_name as first_name,
    a2.AbiturientID as second_id,
    a2.first_name as second_name,
    a1.surname as common_surname
FROM
    Abiturient as a1, Abiturient as a2
WHERE
    a1.surname = a2.surname and a1.AbiturientID < a2.AbiturientID
ORDER BY
    a1.AbiturientID

-- Запрос: Найти всех студентов, у которых документ был выдан одной организацией

SELECT
    d1.abiturientid as first_stud,
    d2.abiturientid as second_stud,
    d1.org_id as common_organization
FROM
    Document_identifier as d1, Document_identifier as d2
WHERE
    d1.org_id = d2.org_id and d1.AbiturientID < d2.AbiturientID
ORDER BY
    d1.org_id
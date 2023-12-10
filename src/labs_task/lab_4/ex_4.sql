-- Подзапросы, возвращающие множество значений

-- Запрос: Найти средний возраст мужчин в таблице Abiturient
SELECT round(AVG(age), 10) as avg_male_age
FROM (
    SELECT EXTRACT(YEAR FROM age(DateOfBirth)) AS age
    FROM Abiturient
    WHERE sex = 'm'
) AS subquery;

-- Запрос: Определить средний возраст абитуриентов, которые предоставили документы
SELECT round(AVG(EXTRACT(YEAR FROM age(DateOfBirth))), 10) as avg_age
FROM Abiturient
WHERE AbiturientID in (SELECT AbiturientID FROM Document_identifier);

-- Запрос: Типы документов, которые были выданы абитуриентам младше 18 лет:
SELECT Name_doc_type
FROM Types_Document_identifier
WHERE Doc_type_ID IN (
    SELECT Doc_type_ID
    FROM Document_identifier
    WHERE AbiturientID IN (
        SELECT AbiturientID 
        FROM Abiturient 
        WHERE EXTRACT(YEAR FROM AGE(DateOfBirth)) < 17
    )
);

-- Запрос: Типы документов, которые не были выданы ни одному абитуриенту:
SELECT Name_doc_type
FROM Types_Document_identifier
WHERE Doc_type_ID NOT IN (
    SELECT DISTINCT Doc_type_ID 
    FROM Document_identifier
);

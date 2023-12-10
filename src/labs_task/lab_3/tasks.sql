-- Запрос: Найти всех абитуриентов (мужчин), которым уже исполнилось 18 лет
SELECT
    AbiturientID,
    first_name,
    surname
FROM
    Abiturient
WHERE sex = 'm' and EXTRACT(YEAR FROM age(DateOfBirth)) >= 18

-- Запрос: Посчитать количество документов (identify) выданных всеми органициями, 
-- отсортировать по количеству (убыванию) и вывести 100 первых
SELECT
    count(document_identifier_ID) as amount_doc
FROM
    Document_identifier
GROUP BY
    org_id
ORDER BY
    amount_doc DESC
LIMIT 100

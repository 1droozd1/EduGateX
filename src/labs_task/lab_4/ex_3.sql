-- Подзапросы, возвращающие единичное значение

-- Запрос: Количество документов, которые были выданы самой 
-- активной организацией (организацией, выдавшей наибольшее количество документов):

SELECT 
    COUNT(document_identifier_ID)
FROM Document_identifier
WHERE org_id = (
    SELECT org_id 
    FROM Document_identifier 
    GROUP BY org_id 
    ORDER BY COUNT(document_identifier_ID) DESC
    LIMIT 1
);

-- Запрос: Найти документы самого молодого абитуриента
SELECT
    document_identifier_ID,
    Doc_type_ID,
    series_doc,
    number_doc
FROM
    Document_identifier
WHERE
    AbiturientID in (
        SELECT AbiturientID
        FROM Abiturient
        ORDER BY DateOfBirth DESC
        LIMIT 1
    );

-- Запрос: Дата, когда было выдано наибольшее количество документов:
SELECT 
    date_issue
FROM
    Document_identifier
GROUP BY
    date_issue
HAVING COUNT(document_identifier_ID) = 
    (
        SELECT MAX(cnt) 
        FROM(
                SELECT COUNT(document_identifier_ID) as cnt
                FROM Document_identifier 
                GROUP BY date_issue
            ) AS subquery
    );
-- Запрос: Наиболее часто используемый код организации при выдаче документов
SELECT
    code_org
FROM
    Issuing_Organization 
WHERE org_id = (
                SELECT
                    org_id
                FROM
                    Document_identifier
                GROUP BY
                    org_id
                ORDER BY
                    COUNT(*) DESC
                LIMIT 1
    );

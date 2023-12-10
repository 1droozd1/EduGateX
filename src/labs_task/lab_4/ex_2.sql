-- Active: 1696235511511@@127.0.0.1@5432@bd_project@public
-- Применение курсора -> запрос с WITH

-- Запрос: Вывести список абитуриентов, чьи документы были выданы определенной организацией
WITH OrgDocuments AS (
    SELECT
        d.AbiturientID
    FROM
        Document_identifier as d
    WHERE
        d.org_id in (SELECT org_id FROM Issuing_Organization WHERE name_org = 'МВД ПО РЕСП. БАШКОРТОСТАН')
)
SELECT
    a.AbiturientID,
    a.first_name,
    a.surname
FROM
    Abiturient as a
JOIN
    OrgDocuments od ON a.AbiturientID = od.AbiturientID

-- Запрос: Список организаций, которые выдали документы абитуриентам, родившимся 
-- после определенной даты

WITH YoungAbiturients AS (
    SELECT 
        AbiturientID
    FROM 
        Abiturient
    WHERE 
        DateOfBirth > '2002-01-01'
)
SELECT DISTINCT 
    io.Name_org
FROM 
    Issuing_Organization as io
JOIN 
    Document_identifier d ON io.org_id = d.org_id
JOIN 
    YoungAbiturients as ya ON d.AbiturientID = ya.AbiturientID;

-- Запрос: Список типов документов и количество абитуриентов, у которых есть этот тип документа
WITH TypeCount AS (
    SELECT 
        Doc_type_ID,
        COUNT(DISTINCT AbiturientID) as AbiturientCount
    FROM 
        Document_identifier
    GROUP BY 
        Doc_type_ID
)
SELECT 
    t.Name_doc_type,
    tc.AbiturientCount
FROM 
    Types_Document_identifier as t
JOIN 
    TypeCount tc ON t.Doc_type_ID = tc.Doc_type_ID;

-- Запрос: Абитуриенты, чьи документы были выданы раньше всех
WITH EarliestDocuments AS (
    SELECT 
        AbiturientID,
        date_issue AS EarliestDate
    FROM 
        Document_identifier
    ORDER BY
        date_issue
    LIMIT
        5
)
SELECT 
    a.first_name,
    a.surname,
    a.patronymic,
    ed.EarliestDate
FROM 
    Abiturient as a
JOIN 
    EarliestDocuments as ed ON a.AbiturientID = ed.AbiturientID
ORDER BY 
    a.abiturientid

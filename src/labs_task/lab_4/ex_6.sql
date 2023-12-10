-- Предикаты на подзапросах, использующие операции EXISTS и NOT EXISTS

-- Запрос: Найти всех абитуриентов, у которых есть паспорт в качестве документа подтверждения личности.
SELECT first_name, surname
FROM Abiturient a
WHERE EXISTS (
    SELECT 1
    FROM Document_identifier as d
    JOIN Types_Document_identifier as t ON d.Doc_type_ID = t.Doc_type_ID
    WHERE a.AbiturientID = d.AbiturientID AND t.Name_doc_type = 'Паспорт РФ'
);

-- Запрос: Найти всех абитуриентов, у которых есть документ, выданный после 1 января 2020 года.
SELECT first_name, surname
FROM Abiturient a
WHERE EXISTS (
    SELECT 1
    FROM Document_identifier d
    WHERE a.AbiturientID = d.AbiturientID AND d.date_issue > '2020-01-01'
);


-- Запрос: Найти всех абитуриентов, у которых нет паспорта.
SELECT first_name, surname
FROM Abiturient a
WHERE NOT EXISTS (
    SELECT 1
    FROM Document_identifier d
    JOIN Types_Document_identifier t ON d.Doc_type_ID = t.Doc_type_ID
    WHERE a.AbiturientID = d.AbiturientID AND t.Name_doc_type = 'Паспорт РФ'
);

-- Запрос: Найти организации, которые ни разу не выдали документ абитуриентам.
SELECT Name_org
FROM Issuing_Organization o
WHERE NOT EXISTS (
    SELECT 1
    FROM Document_identifier d
    WHERE o.org_id = d.org_id
);

-- Запрос: Найти организации, которые не выдали ни одного документа абитуриентам в 2020 году.
SELECT Name_org
FROM Issuing_Organization as o
WHERE NOT EXISTS (
    SELECT 1
    FROM Document_identifier d
    WHERE o.org_id = d.org_id AND EXTRACT(YEAR FROM d.date_issue) = 2020
);

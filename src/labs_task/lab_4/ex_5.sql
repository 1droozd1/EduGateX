-- Предикаты на подзапросах, использующие SOME, ANY и ALL

-- Запрос: Найти всех абитуриентов, у которых есть хотя бы один документ 
--с датой выпуска после определенной даты.
SELECT DISTINCT a.first_name, a.surname
FROM Abiturient a
WHERE a.AbiturientID IN (
    SELECT AbiturientID 
    FROM Document_identifier 
    WHERE date_issue > SOME (SELECT date_issue FROM Document_identifier WHERE date_issue > '2020-01-01')
);

-- Запрос: Найти всех абитуриентов, чья фамилия начинается с какой-либо из заданных букв.
SELECT first_name, surname
FROM Abiturient
WHERE LEFT(surname, 1) = SOME (ARRAY['А', 'Б', 'В'])
ORDER BY surname;

-- Запрос: Найти все типы документов, которые выданы хотя бы одному из абитуриентов.
SELECT Name_doc_type
FROM Types_Document_identifier
WHERE Doc_type_ID = ANY (SELECT DISTINCT Doc_type_ID FROM Document_identifier);

-- Запрос: Найти абитуриентов, у которых номер телефона оканчивается на любую из заданных цифр.
SELECT first_name, surname
FROM Abiturient
WHERE RIGHT(phone, 1) = ANY (ARRAY['1', '2', '3']);

-- Запрос: Найти всех абитуриентов, чей возраст больше чем у всех абитуриентов родившихся после 2005 года.

SELECT first_name, surname, DateOfBirth
FROM Abiturient
WHERE DateOfBirth <= ALL (SELECT DateOfBirth FROM Abiturient WHERE DateOfBirth >= '2005-01-01')
ORDER BY DateOfBirth;

-- Запрос: Найти документы, дата выпуска которых раньше всех документов, выданных в 2018 году.
SELECT series_doc, number_doc
FROM Document_identifier
WHERE date_issue <= ALL (SELECT date_issue FROM Document_identifier WHERE EXTRACT(YEAR FROM date_issue) = 2018);

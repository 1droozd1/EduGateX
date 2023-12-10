-- Создание таблицы для хранения информации об абитурентах
CREATE TABLE Abiturient (
    AbiturientID SERIAL PRIMARY KEY,
	first_name VARCHAR(50) NOT NULL,
	surname VARCHAR(50) NOT NULL,
    patronymic VARCHAR(50),
    DateOfBirth DATE NOT NULL,
    sex VARCHAR(1) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    photo BYTEA
);

-- Создание таблицы для хранения информации об пользователях
CREATE TABLE User_account (
    userID SERIAL PRIMARY KEY,
    username VARCHAR(80) NOT NULL,
    password_user VARCHAR(180) NOT NULL,
    AbiturientID INT REFERENCES Abiturient(AbiturientID) ON DELETE CASCADE
)

-- Создание таблицы для хранения информации о документах (подтверждение личности) абитурентов
CREATE TABLE Document_identifier (
    document_identifier_ID SERIAL PRIMARY KEY,
    Doc_type_ID INT REFERENCES Types_Document_identifier(Doc_type_ID),
    series_doc INT,
    number_doc INT,
    date_issue DATE,
    org_id INT REFERENCES Issuing_Organization(org_id),
    AbiturientID INT REFERENCES Abiturient(AbiturientID) ON DELETE CASCADE
);

-- Создание таблицы для хранения типов документов (подтверждение личности)
CREATE TABLE Types_Document_identifier (
    Doc_type_ID SERIAL PRIMARY KEY,
    Name_doc_type VARCHAR(255) NOT NULL
);

-- Создание таблицы для хранения организаций, выдающих документы
CREATE TABLE Issuing_Organization (
    org_id SERIAL PRIMARY KEY,
    code_org INT,
    Name_org VARCHAR(255) NOT NULL
);

-- Создание таблицы для хранения информации об образовании абитурентов
CREATE TABLE Document_education (
    document_identifier_ID SERIAL PRIMARY KEY,
    Doc_type_ID INT REFERENCES Types_Document_education(Doc_type_ID),
    series_doc INT,
    number_doc INT,
    date_issue DATE,
    org_id INT REFERENCES Education_Organization(org_id),
    presence_of_original BOOLEAN,
    AbiturientID INT REFERENCES Abiturient(AbiturientID) ON DELETE CASCADE
);

-- Создание таблицы для хранения типов образовательных документов
CREATE TABLE Types_Document_education (
    Doc_type_ID SERIAL PRIMARY KEY,
    Name_doc_type VARCHAR(255) NOT NULL
);

-- Создание таблицы для хранения информации об образовательных организациях
CREATE TABLE Education_Organization (
    org_id SERIAL PRIMARY KEY,
    Name_org VARCHAR(310) NOT NULL
);

-- Создание таблицы для хранения заявлений на поступление
CREATE TABLE Application_for_admission (
    ApplicationID SERIAL PRIMARY KEY,
    AbiturientID INT REFERENCES Abiturient(AbiturientID) ON DELETE CASCADE,
    SpecialityID INT REFERENCES Specialty_for_study(SpecialityID),
    data_application DATE,
    EmployeeID INT REFERENCES Employee(EmployeeID)
);

-- Создание таблицы для хранения специальностей для обучения
CREATE TABLE Specialty_for_study (
    SpecialityID SERIAL PRIMARY KEY,
    code_speciality VARCHAR(20) NOT NULL,
    name_speciality VARCHAR(100) NOT NULL,
    is_paid BOOLEAN,
    amount_place INT
);

-- Создание таблицы для связи специальностей и экзаменов
CREATE TABLE Programm_for_study (
    ProgrammID INT REFERENCES Specialty_for_study(SpecialityID),
    ExamID INT REFERENCES Exam(ExamID)
);

-- Создание таблицы для хранения информации об экзаменах
CREATE TABLE Exam (
    ExamID SERIAL PRIMARY KEY,
    name_exam VARCHAR(50) NOT NULL
);

-- Создание таблицы для хранения результатов экзаменов
CREATE TABLE Exam_res (
    AbiturientID INT REFERENCES Abiturient(AbiturientID) ON DELETE CASCADE,
    ExamID INT REFERENCES Exam(ExamID),
    score INT
);

-- Создание таблицы для хранения информации о сотрудниках
CREATE TABLE Employee (
    EmployeeID SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
	surname VARCHAR(50) NOT NULL,
    patronymic VARCHAR(50),
    username VARCHAR(80) NOT NULL,
    password_user VARCHAR(180) NOT NULL,
    PositionID INT REFERENCES Positions_rights(PositionID)
);

-- Создание таблицы для хранения прав сотрудников
CREATE TABLE Positions_rights (
    PositionID SERIAL PRIMARY KEY,
    name_position VARCHAR(50) NOT NULL,
    rights_position VARCHAR(50) NOT NULL
)
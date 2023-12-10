from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Abiturient(db.Model):
    abiturientid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    patronymic = db.Column(db.String(50))
    dateofbirth = db.Column(db.Date, nullable=False)
    sex = db.Column(db.String(1), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    # Связь с пользовательской учетной записью (один-к-одному)
    user_account = db.relationship('User_account', backref='abiturient_user', cascade='all, delete-orphan', uselist=False)

    # Связь с документами и образованием (один-ко-многим)
    documents = db.relationship('Document_identifier', backref='abiturient_doc', cascade='all, delete-orphan')
    education_documents = db.relationship('Document_education', backref='abiturient_edu_doc', cascade='all, delete-orphan')

    # Связь с заявлениями (один-ко-многим)
    applications = db.relationship('Application_for_admission', backref='abiturient_apl', cascade='all, delete-orphan')

    # Связь с результатами экзаменов (один-ко-многим)
    exam_res = db.relationship('Exam_res', backref='abiturient_exam_res', cascade='all, delete-orphan')

class User_account(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password_user = db.Column(db.String(120), nullable=False)
    abiturientid = db.Column(db.Integer, db.ForeignKey('abiturient.abiturientid'))

class Document_identifier(db.Model):
    document_identifier_id = db.Column(db.Integer, primary_key=True)
    doc_type_id = db.Column(db.Integer, db.ForeignKey('types_document_identifier.doc_type_id'))
    series_doc = db.Column(db.Integer)
    number_doc = db.Column(db.Integer)
    date_issue = db.Column(db.Date)
    org_id = db.Column(db.Integer, db.ForeignKey('issuing_organization.org_id'))
    abiturientid = db.Column(db.Integer, db.ForeignKey('abiturient.abiturientid'))

class Types_document_identifier(db.Model):
    __tablename__ = 'types_document_identifier'
    doc_type_id = db.Column(db.Integer, primary_key=True)
    name_doc_type = db.Column(db.String(255), nullable=False)

class Issuing_Organization(db.Model):
    __tablename__ = 'issuing_organization'
    org_id = db.Column(db.Integer, primary_key=True)
    code_org = db.Column(db.Integer)
    name_org = db.Column(db.String(255), nullable=False)

class Document_education(db.Model):
    document_identifier_id = db.Column(db.Integer, primary_key=True)
    doc_type_id = db.Column(db.Integer, db.ForeignKey('types_document_education.doc_type_id'))
    series_doc = db.Column(db.Integer)
    number_doc = db.Column(db.Integer)
    date_issue = db.Column(db.Date)
    org_id = db.Column(db.Integer, db.ForeignKey('education_organization.org_id'))
    presence_of_original = db.Column(db.Boolean)
    abiturientid = db.Column(db.Integer, db.ForeignKey('abiturient.abiturientid'))

class Types_Document_education(db.Model):
    __tablename__ = 'types_document_education'
    doc_type_id = db.Column(db.Integer, primary_key=True)
    name_doc_type = db.Column(db.String(255), nullable=False)

class Education_Organization(db.Model):
    __tablename__ = 'education_organization'
    org_id = db.Column(db.Integer, primary_key=True)
    name_org = db.Column(db.String(310), nullable=False)

class Application_for_admission(db.Model):
    applicationid = db.Column(db.Integer, primary_key=True)
    abiturientid = db.Column(db.Integer, db.ForeignKey('abiturient.abiturientid'))
    specialityid = db.Column(db.Integer, db.ForeignKey('specialty_for_study.specialityid'))
    data_application = db.Column(db.Date)
    employeeid = db.Column(db.Integer, db.ForeignKey('employee.employeeid'))

class Specialty_for_study(db.Model):
    specialityid = db.Column(db.Integer, primary_key=True)
    code_speciality = db.Column(db.String(20), nullable=False)
    name_speciality = db.Column(db.String(200), nullable=False)
    is_paid = db.Column(db.Boolean)
    amount_place = db.Column(db.Integer)

class Programm_for_study(db.Model):
    programmID = db.Column(db.Integer, db.ForeignKey('specialty_for_study.specialityid'), primary_key=True)
    examid = db.Column(db.Integer, db.ForeignKey('exam.examid'), primary_key=True)

class Exam(db.Model):
    examid = db.Column(db.Integer, primary_key=True)
    name_exam = db.Column(db.String(50), nullable=False)

class Exam_res(db.Model):
    abiturientID = db.Column(db.Integer, db.ForeignKey('abiturient.abiturientid'), primary_key=True)
    examID = db.Column(db.Integer, db.ForeignKey('exam.examID'), primary_key=True)
    score = db.Column(db.Integer)

class Employee(db.Model):
    employeeid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    patronymic = db.Column(db.String(50))
    username = db.Column(db.String(80), nullable=False)
    password_user = db.Column(db.String(120), nullable=False)
    positionid = db.Column(db.Integer, db.ForeignKey('positions_rights.positionid'), primary_key=True)

class Positions_rights(db.Model):
    positionID = db.Column(db.Integer, primary_key=True)
    name_position = db.Column(db.String(50), nullable=False)
    rights_position = db.Column(db.String(50), nullable=False)
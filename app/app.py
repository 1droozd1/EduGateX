from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from model import *

import sys, os
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.append(project_dir)

from config import *
from sqlalchemy import or_, desc, func

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

# Инициализируйте объект SQLAlchemy для работы с базой данных
db.init_app(app)

def get_rating_lists_for_special_detail(specialty_id):
    applications = Application_for_admission.query.filter_by(specialityid=specialty_id).all()

    for app in applications:
        specialty = Specialty_for_study.query.get(app.specialityid)

        # Результаты экзаменов студентов подавших заявление на данное направление
        exam_scores = (
            db.session.query(
                Exam_res.abiturientid,
                Exam_res.score,
                Exam.name_exam
            )
            .join(Exam, Exam_res.examid == Exam.examid)
            .join(Programm_for_study, Exam.examid == Programm_for_study.programmid)
            .join(Application_for_admission, Exam_res.abiturientid == Application_for_admission.abiturientid)

            .where(
                Application_for_admission.specialityid == specialty.specialityid and
                Programm_for_study.programmid == Application_for_admission.specialityid
            )
            .group_by(Exam_res.abiturientid, Exam.name_exam, Exam_res.score)
            .order_by(Exam_res.abiturientid)
            .all()
        )

        dict_exam_scores = {}
        for abiturientID, total_exam_score, name_exam in exam_scores:
            try:
                dict_exam_scores[abiturientID].append((name_exam, total_exam_score))
            except KeyError:
                dict_exam_scores[abiturientID] = [(name_exam, total_exam_score)]
        
        # Список экзаменов необходимых для данной специальности
        need_exam = (
            db.session.query(Exam.name_exam)
            .join(Programm_for_study, Exam.examid == Programm_for_study.examid)
            .join(Specialty_for_study, Programm_for_study.programmid == Specialty_for_study.specialityid)
            .filter(Specialty_for_study.specialityid == specialty.specialityid)
            .all()
        )
        need_exam = [exam.name_exam for exam in need_exam]

        # Формируем список абитуриентов с индексами
        indexed_abiturients = []

        for abiturientID, exams_res in dict_exam_scores.items():
            abiturient = Abiturient.query.get(abiturientID)
            score_abi = sum(score for _, score in exams_res) - min([score for subject, score in exams_res if subject in need_exam[1:3]])
            indexed_abiturients.append([abiturient, score_abi])

        indexed_abiturients_sorted = sorted(indexed_abiturients, key=lambda x: x[1], reverse=True)

        index = 1
        for _ in range(len(indexed_abiturients_sorted)):
            indexed_abiturients_sorted[_].insert(0, index)
            indexed_abiturients_sorted[_].insert(4, specialty.amount_place >= index)
            index += 1

    
    return indexed_abiturients_sorted

def get_rating_lists_for_all_specialties(user_abiturientid):
    rating_lists = {}
    applications = Application_for_admission.query.filter_by(abiturientid=user_abiturientid).all()

    for app in applications:
        specialty = Specialty_for_study.query.get(app.specialityid)

        # Результаты экзаменов студентов подавших заявление на данное направление
        exam_scores = (
            db.session.query(
                Exam_res.abiturientid,
                Exam_res.score,
                Exam.name_exam
            )
            .join(Exam, Exam_res.examid == Exam.examid)
            .join(Programm_for_study, Exam.examid == Programm_for_study.programmid)
            .join(Application_for_admission, Exam_res.abiturientid == Application_for_admission.abiturientid)

            .where(
                Application_for_admission.specialityid == specialty.specialityid and
                Programm_for_study.programmid == Application_for_admission.specialityid
            )
            .group_by(Exam_res.abiturientid, Exam.name_exam, Exam_res.score)
            .order_by(Exam_res.abiturientid)
            .all()
        )

        dict_exam_scores = {}
        for abiturientID, total_exam_score, name_exam in exam_scores:
            try:
                dict_exam_scores[abiturientID].append((name_exam, total_exam_score))
            except KeyError:
                dict_exam_scores[abiturientID] = [(name_exam, total_exam_score)]
        
        # Список экзаменов необходимых для данной специальности
        need_exam = (
            db.session.query(Exam.name_exam)
            .join(Programm_for_study, Exam.examid == Programm_for_study.examid)
            .join(Specialty_for_study, Programm_for_study.programmid == Specialty_for_study.specialityid)
            .filter(Specialty_for_study.specialityid == specialty.specialityid)
            .all()
        )
        need_exam = [exam.name_exam for exam in need_exam]

        # Формируем список абитуриентов с индексами
        indexed_abiturients = []

        for abiturientID, exams_res in dict_exam_scores.items():
            abiturient = Abiturient.query.get(abiturientID)
            is_current_user = user_abiturientid == abiturientID
            score_abi = sum(score for _, score in exams_res) - min([score for subject, score in exams_res if subject in need_exam[1:3]])
            indexed_abiturients.append([abiturient, is_current_user, score_abi])

        indexed_abiturients_sorted = sorted(indexed_abiturients, key=lambda x: x[2], reverse=True)

        index = 1
        for _ in range(len(indexed_abiturients_sorted)):
            indexed_abiturients_sorted[_].insert(0, index)
            indexed_abiturients_sorted[_].insert(4, specialty.amount_place >= index)
            index += 1

        rating_lists[specialty] = indexed_abiturients_sorted
    
    return rating_lists

@app.route('/', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        # Обработка входа и проверка логина и пароля
        username = request.form['username']
        password = request.form['password']

        # Проверка, является ли пользователь администратором
        admin = Employee.query.filter_by(username=username).first()

        if admin is not None and check_password_hash(admin.password_user, password):
            session['employeeid'] = admin.employeeid
            session['username'] = username
            # Если пользователь - админ, перенаправляем на страницу администратора
            return redirect(url_for('admin_dashboard', username=username))
        else:
            # Проверяем, является ли пользователь обычным пользователем
            user = User_account.query.filter_by(username=username).first()
            if user is not None and check_password_hash(user.password_user, password):
                # Вход выполнен успешно, перенаправляем на страницу профиля
                return redirect(url_for('profile', username=username))
            else:
                flash("Неправильный логин или пароль", "danger")

    return render_template('welcome.html')

@app.route('/admin_dashboard/<username>')
def admin_dashboard(username):
    admin = Employee.query.filter_by(username=username).first()
    if admin:
        # Получаем список всех специальностей и количество поданных заявлений на каждую из них
        specialties = Specialty_for_study.query.all()
        applications_count = {}
        for specialty in specialties:
            applications_count[specialty] = [
                Application_for_admission.query.filter_by(specialityid=specialty.specialityid).count(),
                'платное' if specialty.is_paid else 'бюджетное'
            ]

        # Сохраняем предыдущий URL в сессии
        session['admin_dashboard'] = request.url
        return render_template('admin_dashboard.html', admin=admin, applications_count=applications_count)
    else:
        return "Администратор не найден", 404
    
@app.route('/add_abiturient_form')
def add_abiturient_form():
    specialties = Specialty_for_study.query.all()
    exam_names = Exam.query.all()
    return render_template('add_abiturient_form.html', specialties=specialties, exam_names=exam_names)

@app.route('/add_abiturient', methods=['POST'])
def add_abiturient():
    if request.method == 'POST':

        specialityid = request.form.get('specialityid')

        # Получение данных из формы
        first_name = request.form.get('first_name')
        surname = request.form.get('surname')
        patronymic = request.form.get('patronymic')
        dateofbirth = request.form.get('dateofbirth')
        sex = request.form.get('sex')
        phone = request.form.get('phone')
        email = request.form.get('email')

        # Создание экземпляра абитуриента
        new_abiturient = Abiturient(first_name=first_name, surname=surname, patronymic=patronymic, dateofbirth=dateofbirth, sex=sex, phone=phone, email=email)
        
        # Добавление в базу данных
        db.session.add(new_abiturient)
        db.session.commit()

        data_application = datetime.now().date().strftime("%Y-%m-%d")
        employeeid = session['employeeid']
        new_application = Application_for_admission(abiturientid=new_abiturient.abiturientid, specialityid=specialityid, data_application=data_application, employeeid=employeeid)
        db.session.add(new_application)
        db.session.commit()

        # Обработка данных по экзаменам
        exam_ids = request.form.getlist('examid[]')
        exam_scores = request.form.getlist('exam_score[]')
        for exam_id, exam_score in zip(exam_ids, exam_scores):
            new_exam_result = Exam_res(abiturientid=new_abiturient.abiturientid, examid=exam_id, score=exam_score)
            db.session.add(new_exam_result)
            db.session.commit()

        flash('AbiturientAddedSuccessfully')
        return redirect(url_for('admin_dashboard', username=session['username']))

    return redirect(url_for('admin_dashboard', username=session['username']))

@app.route('/search_abiturient', methods=['GET'])
def search_abiturient():
    search_query = request.args.get('search_query')
    if search_query:
        # Разбиваем запрос на компоненты
        parts = search_query.split()

        # Формируем запрос в зависимости от количества введенных слов
        query = Abiturient.query
        if len(parts) == 1:
            query = query.filter(or_(Abiturient.surname.ilike(f'%{parts[0]}%'), Abiturient.first_name.ilike(f'%{parts[0]}%')))
        if len(parts) >= 2:
            query = query.filter(Abiturient.surname.ilike(f'%{parts[0]}%'))
            query = query.filter(Abiturient.first_name.ilike(f'%{parts[1]}%'))
        if len(parts) >= 3:
            query = query.filter(Abiturient.patronymic.ilike(f'%{parts[2]}%'))

        search_result = query.all()
        return render_template('search_results.html', abiturients=search_result)
    else:
        return redirect(url_for('admin_dashboard', username=session['username']))
    

@app.route('/show_all_abiturients', methods=['GET'])
def show_all_abiturients():
    abiturients = Abiturient.query.order_by(Abiturient.surname).all()
    return render_template('show_all_abiturients.html', abiturients=abiturients)

@app.route('/view_abiturient/<int:abiturientid>', methods=['GET'])
def view_abiturient(abiturientid):
    # Получите информацию об абитуриенте по abiturientid
    abiturient = Abiturient.query.get_or_404(abiturientid)
    documents = Document_identifier.query.filter_by(abiturientid=abiturientid).all()
    education_documents = Document_education.query.filter_by(abiturientid=abiturientid).all()
    document_types = [document.name_doc_type for document in Types_document_identifier.query.all()]
    issuing_organizations = [org.name_org for org in Issuing_Organization.query.all()]
    education_document_types = [document.name_doc_type for document in Types_Document_education.query.all()]
    education_organizations = [org.name_org for org in Education_Organization.query.all()]
    
    # Отображение информации об абитуриенте
    return render_template('view_abiturient.html', abiturient=abiturient, documents=documents, document_types=document_types, issuing_organizations=issuing_organizations, education_documents=education_documents, education_document_types=education_document_types, education_organizations=education_organizations)

@app.route('/delete_abiturient/<int:abiturientid>', methods=['GET', 'POST'])
def delete_abiturient(abiturientid):
    abiturient = Abiturient.query.get_or_404(abiturientid)
    if abiturient:
        # Удаление абитуриента из базы данных
        db.session.delete(abiturient)
        db.session.commit()
        flash('Абитуриент успешно удален', 'success')
    else:
        flash('Абитуриент не найден', 'danger')
    
    return redirect(url_for('admin_dashboard', username=session['username']))

@app.route('/edit_abiturient/<int:abiturientid>', methods=['GET', 'POST'])
def edit_abiturient(abiturientid):
    abiturient = Abiturient.query.get_or_404(abiturientid)
    documents = Document_identifier.query.filter_by(abiturientid=abiturientid).all()
    education_documents = Document_education.query.filter_by(abiturientid=abiturientid).all()
    document_types = Types_document_identifier.query.all()
    issuing_organizations = Issuing_Organization.query.all()
    education_document_types = Types_Document_education.query.all()
    education_organizations = Education_Organization.query.all()

    if request.method == 'POST':
        # Обновление данных абитуриента
        abiturient.first_name = request.form['first_name']
        abiturient.surname = request.form['surname']
        abiturient.patronymic = request.form['patronymic']
        abiturient.dateofbirth = request.form['dateofbirth']
        abiturient.sex = request.form['sex']
        abiturient.phone = request.form['phone']
        abiturient.email = request.form['email']

        for document in documents:
            document.series_doc = request.form[f'series_doc_{document.document_identifier_id}']
            document.number_doc = request.form[f'number_doc_{document.document_identifier_id}']
            document.date_issue = request.form[f'date_issue_{document.document_identifier_id}']
            document.doc_type_id = request.form[f'doc_type_{document.document_identifier_id}']
            document.org_id = request.form[f'org_id_{document.document_identifier_id}']
        
        for edu_document in education_documents:
            edu_document.doc_type_id = request.form[f'edu_doc_type_{edu_document.document_identifier_id}']
            edu_document.series_doc = request.form[f'edu_series_doc_{edu_document.document_identifier_id}']
            edu_document.number_doc = request.form[f'edu_number_doc_{edu_document.document_identifier_id}']
            edu_document.date_issue = request.form[f'edu_date_issue_{edu_document.document_identifier_id}']
            edu_document.org_id = request.form[f'edu_org_id_{edu_document.document_identifier_id}']

        db.session.commit()
        flash("Данные абитуриента обновлены")
        return redirect(url_for('admin_dashboard', username=session['username']))

    return render_template('edit_abiturient_form.html', abiturient=abiturient, documents=documents, document_types=document_types, issuing_organizations=issuing_organizations, education_documents=education_documents, education_document_types=education_document_types, education_organizations=education_organizations)

@app.route('/specialty_detail/<int:specialty_id>')
def specialty_detail(specialty_id):
    specialty = Specialty_for_study.query.get_or_404(specialty_id)
    applications = get_rating_lists_for_special_detail(specialty_id)

    return render_template('specialty_detail.html', specialty=specialty, applications=applications)

@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    user = User_account.query.filter_by(username=username).first()
    if user:
        abiturient = Abiturient.query.get(user.abiturientid)
        documents = Document_identifier.query.filter_by(abiturientid=user.abiturientid).all()
        education_documents = Document_education.query.filter_by(abiturientid=user.abiturientid).all()
        
        document_types = [document.name_doc_type for document in Types_document_identifier.query.all()]
        issuing_organizations = [org.name_org for org in Issuing_Organization.query.all()]

        education_document_types = [document.name_doc_type for document in Types_Document_education.query.all()]
        education_organizations = [org.name_org for org in Education_Organization.query.all()]

        applications = Application_for_admission.query.filter_by(abiturientid=user.abiturientid).all()
        specialties_info = [(Specialty_for_study.query.get(app.specialityid), app) for app in applications]
        
        # Получаем рейтинговые списки
        rating_lists = get_rating_lists_for_all_specialties(user.abiturientid)

        # Определяем специальность абитуриента
        abiturient_specialty = None
        for specialty, abiturients in rating_lists.items():
            if any(is_current_user for _, _, is_current_user, _, _ in abiturients):
                abiturient_specialty = specialty
                break
        
        # Находим абитуриента в списке его специальности
        abiturient_place = None
        abiturient_score = None

        if abiturient_specialty:
            abiturient_score = None
            for index, (_, _, is_current_user, score, _) in enumerate(rating_lists[abiturient_specialty]):
                if is_current_user:
                    abiturient_score = score
                    abiturient_place = index + 1
                    break
        
        print(abiturient_score, abiturient_place)

        return render_template('profile.html', abiturient=abiturient, documents=documents, document_types=document_types, issuing_organizations=issuing_organizations, education_documents=education_documents, education_document_types=education_document_types, education_organizations=education_organizations, specialties_info=specialties_info, rating_lists=rating_lists, place=abiturient_place, abiturient_score=abiturient_score)
    else:
        return "Пользователь не найден", 404


if __name__ == '__main__':
    app.run(debug=True)

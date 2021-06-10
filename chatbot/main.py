from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import User, Intents, File
from . import db
import csv
import pandas as pd
from chatterbot import ChatBot

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/add')
def add():
    return render_template('add.html')


@login_required
@main.route('/upload')
def uploadImg():
    return render_template('file.html')


@login_required
@main.route('/upload', methods=['POST'])
def upload():
    csv = request.files['csv']

    if not csv:
        return 'NO FILE UPLOADED', 400

    filename = secure_filename(csv.filename)
    mimetype = csv.mimetype
    img = File(img=csv.read(), mimetype=mimetype, name=filename, user=current_user)
    db.session.add(img)
    db.session.commit()

    return redirect(url_for('main.profile'))


@main.route('/add', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        intents = request.form
        question = intents['question']
        answer = intents['answer']
        print(question, answer)

        adddata = Intents(question=question, answer=answer, user=current_user)
        db.session.add(adddata)
        db.session.commit()

    return redirect(url_for('main.add'))


@main.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        values = current_user
        question = values.name
        answer = values.email
        print(question, answer)
        return question, answer

    # file = current_user.intents
    # data = open(file, 'r')
    # print(data)
    # return file
def transform(text_file_contents):
    return text_file_contents.replace("=", ",")

@main.route('/getdata', methods=['GET', 'POST'])
def RetrieveDataList():
    file = User.query.filter_by(name=current_user.name)
    # return render_template('details.html', employees=file)
    # file = File.query.filter_by(user_id=current_user.id)
    # data = file.img
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                line_count += 1
        print(f'Processed {line_count} lines.')
    return line_count

    # csv_input = csv.reader(file)
    # print(file)
    # print(type(file))
    # print(csv_input)
    # for row in csv_input:
    #     print(row)
    #
    # result = transform(file)
    #
    # responce = make_response
    # return responce
    # return render_template('details.html',employees = file)

@main.route('/intents')
def intents():
    file = Intents.query.filter_by(userid=current_user.id)
    return file
    # return render_template('chatbot.html', file=file)

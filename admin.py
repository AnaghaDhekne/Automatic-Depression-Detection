from flask import Flask, render_template, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, RadioField
from wtforms.validators import InputRequired, Email, Length, NumberRange
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from datetime import datetime, date
from password_strength import PasswordPolicy
import random
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import matplotlib.pyplot as plt
import os
import time
from numpy import mean
from numpy import std
from scipy.stats import pearsonr

app = Flask(__name__)
app.config['SECRET_KEY'] = '#########################'
app.config['IS_LOGIN'] = False
bootstrap = Bootstrap(app)
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": '##############',
    "MAIL_PASSWORD": '###########'
}
app.config['MAIL_DEFAULT_SENDER'] = '####################'
app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_two'
app.config.update(mail_settings)
mail = Mail(app)
s = URLSafeTimedSerializer('#########################')
CONNECTION = mysql.connector.connect(
    host="#############",
    user="####",
    password="####",
    database="#######",
    auth_plugin='mysql_native_password'
)
app.config['CONNECTION'] = CONNECTION


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    age = IntegerField('Age', validators=[InputRequired(), NumberRange(18, 75, 'Age not supported for application')])
    gender = RadioField('Gender', choices=[(1, 'Male'), (2, 'Female')], coerce=int)


class OTPForm(FlaskForm):
    otp = IntegerField('OTP', validators=[InputRequired(), NumberRange(00000, 99999, 'Wrong OTP')])


class EmailForm(FlaskForm):
    email_id = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def handle_intsrverr(e):
    return render_template("500.html")


@app.errorhandler(408)
def handle_reqTimeOut(e):
    return render_template("408.html")


@app.errorhandler(503)
def handle_serverUnavailable(e):
    return render_template("503.html")


@app.route('/pagenotfunderror', methods=['GET', 'POST'])
def pagenotfunderror():
    return redirect(url_for('index'))


@app.route('/level', methods=['GET', 'POST'])
def level():
    delete_graphs()
    my_db = CONNECTION
    mild_female = moderate_female = minimal_female = severe_female = 0
    mild_male = moderate_male = minimal_male = severe_male = 0
    first_age_minimal = second_age_minimal = third_age_minimal = 0
    first_age_mild = second_age_mild = third_age_mild = 0
    first_age_moderate = second_age_moderate = third_age_moderate = 0
    first_age_severe = second_age_severe = third_age_severe = 0
    my_cursor = my_db.cursor()
    sql = "SELECT * FROM results"
    my_cursor.execute(sql)
    user = my_cursor.fetchall()
    for entry in user:
        if entry[8] == 1:
            if entry[11] == 'Female':
                minimal_female = minimal_female + 1
            elif entry[11] == 'Male':
                minimal_male = minimal_male + 1

            if 17 <= entry[10] <= 25:
                first_age_minimal = first_age_minimal + 1
            elif 26 <= entry[10] <= 50:
                second_age_minimal = second_age_minimal + 1
            else:
                third_age_minimal = third_age_minimal + 1
        elif entry[8] == 2:
            if entry[11] == 'Female':
                mild_female = mild_female + 1
            elif entry[11] == 'Male':
                mild_male = mild_male + 1

            if 17 <= entry[10] <= 25:
                first_age_mild = first_age_mild + 1
            elif 26 <= entry[10] <= 50:
                second_age_mild = second_age_mild + 1
            else:
                third_age_mild = third_age_mild + 1
        elif entry[8] == 3:
            if entry[11] == 'Female':
                moderate_female = moderate_female + 1
            elif entry[11] == 'Male':
                moderate_male = moderate_male + 1

            if 17 <= entry[10] <= 25:
                first_age_moderate = first_age_moderate + 1
            elif 26 <= entry[10] <= 50:
                second_age_moderate = second_age_moderate + 1
            else:
                third_age_moderate = third_age_moderate + 1
        else:
            if entry[11] == 'Female':
                severe_female = severe_female + 1
            elif entry[11] == 'Male':
                severe_male = severe_male + 1

            if 17 <= entry[10] <= 25:
                first_age_severe = first_age_severe + 1
            elif 26 <= entry[10] <= 50:
                second_age_severe = second_age_severe + 1
            else:
                third_age_severe = third_age_severe + 1
    labels = ['Female', 'Male']

    sizes_minimal = [minimal_female, minimal_male]  # Add upto 100%
    fig = plt.figure(figsize=(10, 10), dpi=100)
    fig.patch.set_alpha(0.0)
    plt.pie(sizes_minimal, startangle=90, shadow=True, autopct='%.2f')
    fig.suptitle('Minimal Depression Level-Gender', fontsize=30, color='white')
    plt.legend(labels=labels)
    plt.axis('equal')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    path = os.getcwd()
    path = os.path.join(path, 'static')
    path = os.path.join(path, 'images')
    chart_path = os.path.join(path, 'charts')
    image_path = os.path.join(chart_path, 'level_gender_minimal.png')
    plt.savefig(image_path)

    sizes_mild = [mild_female, mild_male]
    fig = plt.figure(figsize=(10, 10), dpi=100)
    fig.patch.set_alpha(0.0)
    fig.suptitle('Mild Depression Level-Gender', fontsize=30, color='white')
    plt.pie(sizes_mild, startangle=90, shadow=True, autopct='%.2f')
    plt.legend(labels=labels)
    plt.axis('equal')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    image_path = os.path.join(chart_path, 'level_gender_mild.png')
    plt.savefig(image_path)

    sizes_moderate = [moderate_female, moderate_male]
    fig = plt.figure(figsize=(10, 10), dpi=100)
    fig.patch.set_alpha(0.0)
    fig.suptitle('Moderate Depression Level-Gender', fontsize=30, color='white')
    plt.pie(sizes_moderate, startangle=90, shadow=True, autopct='%.2f')
    plt.legend(labels=labels)
    plt.axis('equal')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    image_path = os.path.join(chart_path, 'level_gender_moderate.png')
    plt.savefig(image_path)

    sizes_severe = [severe_female, severe_male]
    fig = plt.figure(figsize=(10, 10), dpi=100)
    fig.patch.set_alpha(0.0)
    fig.suptitle('Severe Depression Level-Gender', fontsize=30, color='white')
    plt.pie(sizes_severe, startangle=90, shadow=True, autopct='%.2f')
    plt.legend(labels=labels)
    plt.axis('equal')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    image_path = os.path.join(chart_path, 'level_gender_severe.png')
    plt.savefig(image_path)

    labels = ['18-25 age', '26-50 age', '51-75 age']

    sizes_minimal = [first_age_minimal, second_age_minimal, third_age_minimal]  # Add upto 100%
    fig = plt.figure(figsize=(10, 10), dpi=100)
    fig.patch.set_alpha(0.0)
    plt.pie(sizes_minimal, startangle=90, shadow=True, autopct='%.2f')
    fig.suptitle('Minimal Depression Level-Age', fontsize=30, color='white')
    plt.legend(labels=labels)
    plt.axis('equal')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    image_path = os.path.join(chart_path, 'level_age_minimal.png')
    plt.savefig(image_path)

    sizes_mild = [first_age_mild, second_age_mild, third_age_mild]  # Add upto 100%
    fig = plt.figure(figsize=(10, 10), dpi=100)
    fig.patch.set_alpha(0.0)
    plt.pie(sizes_mild, startangle=90, shadow=True, autopct='%.2f')
    fig.suptitle('Mild Depression Level-Age', fontsize=30, color='white')
    plt.legend(labels=labels)
    plt.axis('equal')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    image_path = os.path.join(chart_path, 'level_age_mild.png')
    plt.savefig(image_path)

    sizes_moderate = [first_age_moderate, second_age_moderate, third_age_moderate]  # Add upto 100%
    fig = plt.figure(figsize=(10, 10), dpi=100)
    fig.patch.set_alpha(0.0)
    plt.pie(sizes_moderate, startangle=90, shadow=True, autopct='%.2f')
    fig.suptitle('Moderate Depression Level-Age', fontsize=30, color='white')
    plt.legend(labels=labels)
    plt.axis('equal')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    image_path = os.path.join(chart_path, 'level_age_moderate.png')
    plt.savefig(image_path)

    sizes_severe = [first_age_severe, second_age_severe, third_age_severe]  # Add upto 100%
    fig = plt.figure(figsize=(10, 10), dpi=100)
    fig.patch.set_alpha(0.0)
    plt.pie(sizes_severe, startangle=90, shadow=True, autopct='%.2f')
    fig.suptitle('Severe Depression Level-Age', fontsize=30, color='white')
    plt.legend(labels=labels)
    plt.axis('equal')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    image_path = os.path.join(chart_path, 'level_age_severe.png')
    plt.savefig(image_path)
    return render_template('level.html')


@app.route('/age', methods=['GET', 'POST'])
def age():
    delete_graphs()
    my_db = CONNECTION
    mild_age_1 = moderate_age_1 = minimal_age_1 = severe_age_1 = 0
    mild_age_2 = moderate_age_2 = minimal_age_2 = severe_age_2 = 0
    mild_age_3 = moderate_age_3 = minimal_age_3 = severe_age_3 = 0
    positive_age_1 = negative_age_1 = neutral_age_1 = 0
    positive_age_2 = negative_age_2 = neutral_age_2 = 0
    positive_age_3 = negative_age_3 = neutral_age_3 = 0
    my_cursor = my_db.cursor()
    sql = "SELECT * FROM results"
    my_cursor.execute(sql)
    user = my_cursor.fetchall()
    for entry in user:
        if 17 <= entry[10] <= 25:
            if entry[8] == 1:
                minimal_age_1 = minimal_age_1 + 1
            elif entry[8] == 2:
                mild_age_1 = mild_age_1 + 1
            elif entry[8] == 3:
                moderate_age_1 = moderate_age_1 + 1
            elif entry[8] == 4:
                severe_age_1 = severe_age_1 + 1

            positive_age_1 = positive_age_1 + entry[6]
            negative_age_1 = negative_age_1 + entry[4]
            neutral_age_1 = neutral_age_1 + entry[5]
        elif 26 <= entry[10] <= 50:
            if entry[8] == 1:
                minimal_age_2 = minimal_age_2 + 1
            elif entry[8] == 2:
                mild_age_2 = mild_age_2 + 1
            elif entry[8] == 3:
                moderate_age_2 = moderate_age_2 + 1
            elif entry[8] == 4:
                severe_age_2 = severe_age_2 + 1

            positive_age_2 = positive_age_2 + entry[6]
            negative_age_2 = negative_age_2 + entry[4]
            neutral_age_2 = neutral_age_2 + entry[5]
        else:
            if entry[8] == 1:
                minimal_age_3 = minimal_age_3 + 1
            elif entry[8] == 2:
                mild_age_3 = mild_age_3 + 1
            elif entry[8] == 3:
                moderate_age_3 = moderate_age_3 + 1
            elif entry[8] == 4:
                severe_age_3 = severe_age_3 + 1

            positive_age_3 = positive_age_3 + entry[6]
            negative_age_3 = negative_age_3 + entry[4]
            neutral_age_3 = neutral_age_3 + entry[5]

    labels = ['Minimal', 'Mild', 'Moderate', 'Severe']

    sizes_age_1 = [minimal_age_1, mild_age_1, moderate_age_1, severe_age_1]  # Add upto 100%
    fig = plt.figure(figsize=(10, 10), dpi=100)
    fig.patch.set_alpha(0.0)
    plt.pie(sizes_age_1, startangle=90, shadow=True, autopct='%.2f')
    fig.suptitle('Age 17 to 25-Depression Level', fontsize=30, color='white')
    plt.legend(labels=labels)
    plt.axis('equal')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    path = os.getcwd()
    path = os.path.join(path, 'static')
    path = os.path.join(path, 'images')
    chart_path = os.path.join(path, 'charts')
    image_path = os.path.join(chart_path, 'level_age_1.png')
    plt.savefig(image_path)

    sizes_age_2 = [minimal_age_2, mild_age_2, moderate_age_2, severe_age_2]
    fig = plt.figure(figsize=(10, 10), dpi=100)
    fig.patch.set_alpha(0.0)
    fig.suptitle('Age 26 to 50-Depression Level', fontsize=30, color='white')
    plt.pie(sizes_age_2, startangle=90, shadow=True, autopct='%.2f')
    plt.legend(labels=labels)
    plt.axis('equal')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    image_path = os.path.join(chart_path, 'level_age_2.png')
    plt.savefig(image_path)

    sizes_age_3 = [minimal_age_3, mild_age_3, moderate_age_3, severe_age_3]
    fig = plt.figure(figsize=(10, 10), dpi=100)
    fig.patch.set_alpha(0.0)
    fig.suptitle('Age 51 to 75-Depression Level', fontsize=30, color='white')
    plt.pie(sizes_age_3, startangle=90, shadow=True, autopct='%.2f')
    plt.legend(labels=labels)
    plt.axis('equal')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    image_path = os.path.join(chart_path, 'level_age_3.png')
    plt.savefig(image_path)

    labels = ['Positive', 'Negative', 'Neutral']

    sizes_emotion_1 = [positive_age_1, negative_age_1, neutral_age_1]  # Add upto 100%
    fig = plt.figure(figsize=(10, 10), dpi=100)
    fig.patch.set_alpha(0.0)
    plt.pie(sizes_emotion_1, startangle=90, shadow=True, autopct='%.2f')
    fig.suptitle('Age 18 to 25-Emotion', fontsize=30, color='white')
    plt.legend(labels=labels)
    plt.axis('equal')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    image_path = os.path.join(chart_path, 'emotion_age_1.png')
    plt.savefig(image_path)

    sizes_emotion_2 = [positive_age_2, negative_age_2, neutral_age_2]  # Add upto 100%
    fig = plt.figure(figsize=(10, 10), dpi=100)
    fig.patch.set_alpha(0.0)
    plt.pie(sizes_emotion_2, startangle=90, shadow=True, autopct='%.2f')
    fig.suptitle('Age 26 to 50-Emotion', fontsize=30, color='white')
    plt.legend(labels=labels)
    plt.axis('equal')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    image_path = os.path.join(chart_path, 'emotion_age_2.png')
    plt.savefig(image_path)

    sizes_emotion_3 = [positive_age_3, negative_age_3, neutral_age_3]  # Add upto 100%
    fig = plt.figure(figsize=(10, 10), dpi=100)
    fig.patch.set_alpha(0.0)
    plt.pie(sizes_emotion_3, startangle=90, shadow=True, autopct='%.2f')
    fig.suptitle('Age 51 to 75-Emotion', fontsize=30, color='white')
    plt.legend(labels=labels)
    plt.axis('equal')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    image_path = os.path.join(chart_path, 'emotion_age_3.png')
    plt.savefig(image_path)
    return render_template('age.html')


@app.route('/gender', methods=['GET', 'POST'])
def gender():
    delete_graphs()
    my_db = CONNECTION
    mild_female = moderate_female = minimal_female = severe_female = 0
    mild_male = moderate_male = minimal_male = severe_male = 0
    positive_female = negative_female = neutral_female = 0
    positive_male = negative_male = neutral_male = 0
    my_cursor = my_db.cursor()
    sql = "SELECT * FROM results"
    my_cursor.execute(sql)
    user = my_cursor.fetchall()

    for entry in user:
        if entry[11] == 'Female':
            if entry[8] == 1:
                minimal_female = minimal_female + 1
            elif entry[8] == 2:
                mild_female = mild_female + 1
            elif entry[8] == 3:
                moderate_female = moderate_female + 1
            elif entry[8] == 4:
                severe_female = severe_female + 1

            positive_female = positive_female + entry[6]
            negative_female = negative_female + entry[4]
            neutral_female = neutral_female + entry[5]
        else:
            if entry[8] == 1:
                minimal_male = minimal_male + 1
            elif entry[8] == 2:
                mild_male = mild_male + 1
            elif entry[8] == 3:
                moderate_male = moderate_male + 1
            elif entry[8] == 4:
                severe_male = severe_male + 1

            positive_male = positive_male + entry[6]
            negative_male = negative_male + entry[4]
            neutral_male = neutral_male + entry[5]
    labels = ['Minimal', 'Mild', 'Moderate', 'Severe']

    sizes_female = [minimal_female, mild_female, moderate_female, severe_female]  # Add upto 100%
    fig = plt.figure(figsize=(10, 10), dpi=100)
    fig.patch.set_alpha(0.0)
    plt.pie(sizes_female, startangle=90, shadow=True, autopct='%.2f')
    fig.suptitle('Female Gender-Depression Level', fontsize=30, color='white')
    plt.legend(labels=labels)
    plt.axis('equal')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    path = os.getcwd()
    path = os.path.join(path, 'static')
    path = os.path.join(path, 'images')
    chart_path = os.path.join(path, 'charts')
    image_path = os.path.join(chart_path, 'gender_female.png')
    plt.savefig(image_path)

    sizes_male = [minimal_male, mild_male, moderate_male, severe_male]
    fig = plt.figure(figsize=(10, 10), dpi=100)
    fig.patch.set_alpha(0.0)
    fig.suptitle('Male Gender-Depression Level', fontsize=30, color='white')
    plt.pie(sizes_male, startangle=90, shadow=True, autopct='%.2f')
    plt.legend(labels=labels)
    plt.axis('equal')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    image_path = os.path.join(chart_path, 'gender_male.png')
    plt.savefig(image_path)

    labels = ['Positive', 'Negative', 'Neutral']

    sizes_female = [positive_female, negative_female, neutral_female]  # Add upto 100%
    fig = plt.figure(figsize=(10, 10), dpi=100)
    fig.patch.set_alpha(0.0)
    plt.pie(sizes_female, startangle=90, shadow=True, autopct='%.2f')
    fig.suptitle('Female Gender-Emotion', fontsize=30, color='white')
    plt.legend(labels=labels)
    plt.axis('equal')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    image_path = os.path.join(chart_path, 'gender_female_emotion.png')
    plt.savefig(image_path)

    sizes_male = [positive_male, negative_male, neutral_male]  # Add upto 100%
    fig = plt.figure(figsize=(10, 10), dpi=100)
    fig.patch.set_alpha(0.0)
    plt.pie(sizes_male, startangle=90, shadow=True, autopct='%.2f')
    fig.suptitle('Male Gender-Emotion', fontsize=30, color='white')
    plt.legend(labels=labels)
    plt.axis('equal')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    image_path = os.path.join(chart_path, 'gender_male_emotion.png')
    plt.savefig(image_path)
    return render_template('gender.html')


@app.route('/emotion_bdi', methods=['GET', 'POST'])
def emotion_bdi():
    delete_graphs()
    my_db = CONNECTION
    my_cursor = my_db.cursor()
    sql = "SELECT * FROM results"
    my_cursor.execute(sql)
    user = my_cursor.fetchall()
    sample_bdi = []
    sample_negative = []
    sample_positive = []
    sample_neutral = []
    for entry in user:
        sample_bdi.append(entry[3])
        sample_negative.append(entry[4])
        sample_neutral.append(entry[5])
        sample_positive.append(entry[6])

    # prepare data
    data1 = sample_negative
    data2 = sample_bdi
    # summarize
    print('data1: mean=%.3f stdv=%.3f' % (mean(data1), std(data1)))
    print('data2: mean=%.3f stdv=%.3f' % (mean(data2), std(data2)))
    # plot
    fig = plt.figure(figsize=(15, 15), dpi=150)
    ax = plt.axes()
    ax.set_facecolor("#44544c")
    fig.patch.set_alpha(0.0)
    fig.suptitle('Emotion-BDI', fontsize=40, color='white')
    plt.scatter(data1, data2, s=200, c='white')
    plt.axis('equal')
    plt.tight_layout(rect=[1, 1, 1, 1])
    plt.xlabel("Negative Emotions", fontsize=30, color='white')
    plt.ylabel("BDI score", fontsize=30, color='white')
    plt.xticks(color='white', fontsize=20)
    plt.yticks(color='white', fontsize=20)
    path = os.getcwd()
    path = os.path.join(path, 'static')
    path = os.path.join(path, 'images')
    chart_path = os.path.join(path, 'charts')
    image_path = os.path.join(chart_path, 'scatter_negative.png')
    plt.savefig(image_path)
    corr, _ = pearsonr(data1, data2)
    print('Pearsons correlation: %.3f', corr)

    # prepare data
    data1 = sample_positive
    data2 = sample_bdi
    print(data1)
    # summarize
    print('data1: mean=%.3f stdv=%.3f' % (mean(data1), std(data1)))
    print('data2: mean=%.3f stdv=%.3f' % (mean(data2), std(data2)))
    # plot
    fig = plt.figure(figsize=(15, 15), dpi=150)
    ax = plt.axes()
    ax.set_facecolor("#44544c")
    fig.patch.set_alpha(0.0)
    fig.suptitle('Emotion-BDI', fontsize=40, color='white')
    plt.scatter(data1, data2, s=200, c='white')
    plt.axis('equal')
    plt.tight_layout(rect=[1, 1, 1, 1])
    plt.xlabel("Positive Emotions", fontsize=30, color='white')
    plt.ylabel("BDI score", fontsize=30, color='white')
    plt.xticks(color='white', fontsize=20)
    plt.yticks(color='white', fontsize=20)
    image_path = os.path.join(chart_path, 'scatter_positive.png')
    plt.savefig(image_path)

    # prepare data
    data1 = sample_neutral
    data2 = sample_bdi
    # summarize
    print('data1: mean=%.3f stdv=%.3f' % (mean(data1), std(data1)))
    print('data2: mean=%.3f stdv=%.3f' % (mean(data2), std(data2)))
    # plot
    fig = plt.figure(figsize=(15, 15), dpi=150)
    ax = plt.axes()
    # Setting the background color
    ax.set_facecolor("#44544c")
    fig.patch.set_alpha(0.0)
    fig.suptitle('Emotion-BDI', fontsize=40, color='white')
    plt.scatter(data1, data2, s=200, c='white')
    plt.axis('equal')
    plt.tight_layout(rect=[1, 1, 1, 1])
    plt.xlabel("Neutral Emotions", fontsize=30, color='white')
    plt.ylabel("BDI score", fontsize=30, color='white')
    plt.xticks(color='white', fontsize=20)
    plt.yticks(color='white', fontsize=20)
    image_path = os.path.join(chart_path, 'scatter_neutral.png')
    plt.savefig(image_path)

    return render_template('emotion_bdi.html')


@app.route('/user_result', methods=['GET', 'POST'])
def user_result():
    delete_graphs()
    eform = EmailForm()
    if eform.validate_on_submit():
        email_id = eform.email_id.data
        mydb = CONNECTION
        mycursor = mydb.cursor()
        sql = "SELECT * FROM users WHERE email = %s"
        mycursor.execute(sql, (email_id,))
        users = mycursor.fetchone()
        if users:
            mycursor1 = mydb.cursor()
            sql1 = "SELECT * FROM results where email_id = %s ORDER BY id DESC LIMIT 1"
            mycursor1.execute(sql1, (email_id,))
            user = mycursor1.fetchone()
            labels = ['Positive', 'Negative', 'Neutral']

            sizes_user = [user[6], user[4], user[5]]  # Add upto 100%
            fig = plt.figure(figsize=(10, 10), dpi=100)
            fig.patch.set_alpha(0.0)
            plt.pie(sizes_user, startangle=90, shadow=True, autopct='%.2f')
            fig.suptitle('User-Emotions', fontsize=30, color='white')
            plt.legend(labels=labels)
            plt.axis('equal')
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])

            path = os.getcwd()
            path = os.path.join(path, 'static')
            path = os.path.join(path, 'images')
            chart_path = os.path.join(path, 'charts')
            image_path = os.path.join(chart_path, 'user_result.png')
            plt.savefig(image_path)
            return render_template('user_result.html', age=user[10], gender=user[11], level=user[8], positive=user[6],
                                   neutral=user[5], negative=user[4], bdi=user[2], email=user[9])
        flash('Not a valid user', 'warning')
        return render_template('admin_result.html', eform=eform)
    flash("Enter correct mail id", "warning")
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    eform = EmailForm()
    if form.validate_on_submit():
        mydb = CONNECTION
        mycursor = mydb.cursor()
        sql = "SELECT * FROM admin WHERE email_id = %s"
        email = form.email.data
        mycursor.execute(sql, (email,))
        user = mycursor.fetchone()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if user:
            if user[6] == 1:
                if check_password_hash(user[3], form.password.data):
                    app.config['IS_LOGIN'] = True
                    session['loggedin'] = True
                    session['id'] = user[0]
                    session['emailId'] = user[2]
                    sql = "INSERT INTO login_admin (email_id,password,date,time) VALUES (%s,%s,%s,%s)"
                    val = (form.email.data, user[3], date.today(), current_time)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    return render_template('admin_result.html', eform=eform)
                else:
                    flash(
                        "Weak Password or Incorrect Password! Must be combination of letters, numbers, symbols. Try again",
                        "warning")
                    return render_template('admin_page.html', lform=form)
            else:
                token = generate_confirmation_token(email)
                confirm_url = url_for('confirm_email', token=token, _external=True)
                html = render_template('activate.html', confirm_url=confirm_url)
                subject = "Please confirm your email"
                send_email(form.email.data, subject, html)
                flash('Mail has not been confirmed. A confirmation email has been sent via email.', 'warning')
                return render_template('admin_page.html', lform=form)
        flash('Not a valid user. Please Sign Up', 'warning')
        return render_template('admin_page.html', lform=form)
    flash("Enter correct mail id and password", "warning")
    return redirect(url_for('index'))


@app.route('/signuppage', methods=['GET', 'POST'])
def signuppage():
    form = RegisterForm()
    return render_template('admin_signuppage.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    policy = PasswordPolicy.from_names(
        length=8,  # min length: 8
        uppercase=1,  # need min. 2 uppercase letters
        numbers=1,  # need min. 2 digits
        special=1,  # need min. 2 special characters
    )
    if not policy.test(form.password.data):
        if form.validate_on_submit():
            error = 0
            mydb = CONNECTION
            my_cursor = mydb.cursor()
            sql = "SELECT email_id FROM admin"
            my_cursor.execute(sql)
            email_user = my_cursor.fetchall()
            for email_id in email_user:
                if email_id[0] == form.email.data:
                    error = 2
                    break
            if 2 == error:
                flash('The mail id is already been used. Please use other email', 'warning')
                return render_template('admin_signuppage.html', form=form)
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            if form.gender.data == 1:
                gender = 'Male'
            else:
                gender = 'Female'
            mycursor = mydb.cursor()
            sql = "INSERT INTO admin (username,email_id,password,age,gender,confirmed) VALUES (%s,%s,%s,%s,%s,%s)"
            val = (form.username.data, form.email.data, hashed_password, form.age.data, gender, 0)
            mycursor.execute(sql, val)

            token = generate_confirmation_token(form.email.data)
            confirm_url = url_for('confirm_email', token=token, _external=True)
            html = render_template('activate.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(form.email.data, subject, html)
            flash('A confirmation email has been sent via email.', 'success')
            mydb.commit()
            return redirect(url_for('index'))
    flash('Enter the information as following rules: strong password, age more than 18', 'warning')
    return render_template('admin_signuppage.html', form=form)


# part of Email Verification module
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


# part of Email Verification module
def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)


# part of Email Verification module
@app.route('/confirm/<token>')
def confirm_email(token):
    form = RegisterForm()
    mydb = CONNECTION
    mycursor = mydb.cursor()
    session['session_email'] = form.email.data
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('index'))
    finally:
        sql = "UPDATE admin SET confirmed = %s WHERE email_id = %s"
        val = (1, email)
        mycursor.execute(sql, val)
        mydb.commit()
        flash('Account confirmed')
    return redirect(url_for('index'))


# part of Email Verification module
def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email


def path_file_delete(path):
    if os.path.isdir(path):
        for filename in os.listdir(path):
            os.remove(os.path.join(path, filename))
        time.sleep(5)


def delete_graphs():
    current_path = os.getcwd()
    path = os.path.join(current_path, 'static')
    path = os.path.join(path, 'images')
    chart_path = os.path.join(path, 'charts')
    path_file_delete(chart_path)


@app.route('/logout')
def logout():
    delete_graphs()
    app.config['IS_LOGIN'] = False
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('emailId', None)
    return redirect(url_for('index'))


@app.route('/forgetpassword', methods=['GET', 'POST'])
def forgetpassword():
    oform = OTPForm()
    eform = EmailForm()
    form = RegisterForm()
    login_form = LoginForm()
    cform = ChangePasswordForm()
    return render_template('admin_forgetpassword.html', oform=oform, eform=eform, form=form, lform=login_form,
                           value=0, cform=cform)


@app.route('/emailsubmit', methods=['GET', 'POST'])
def email_submit():
    oform = OTPForm()
    eform = EmailForm()
    login_form = LoginForm()
    cform = ChangePasswordForm()
    if eform.validate_on_submit():
        mydb = CONNECTION
        mycursor = mydb.cursor()
        sql = "SELECT * FROM admin WHERE email_id = %s"
        email = eform.email_id.data
        mycursor.execute(sql, (email,))
        user = mycursor.fetchone()
        try:
            if user[2] == eform.email_id.data:
                with app.app_context():
                    otp = random.randrange(00000, 99999)
                    msg = Message(subject="Password OTP",
                                  sender=app.config.get("MAIL_USERNAME"),
                                  recipients=[eform.email_id.data],  # replace with your email for testing
                                  body="Your One Time Password is: " + str(otp))
                    mail.send(msg)
                    session['otp'] = otp
                    session['password_update_mail'] = eform.email_id.data
                    return render_template('admin_forgetpassword.html', oform=oform, eform=eform, lform=login_form,
                                           value=1, cform=cform)
        except:
            flash("Email id not registered else check internet connection", "warning")
            return render_template('admin_page.html', lform=login_form)
    flash("Enter correct mail id : '....@gmail.com'", "warning")
    return render_template('admin_page.html', lform=login_form)


@app.route('/otpsubmit', methods=['GET', 'POST'])
def otp_submit():
    cform = ChangePasswordForm()
    oform = OTPForm()
    eform = EmailForm()
    login_form = LoginForm()
    if oform.validate_on_submit() and (session['otp'] == oform.otp.data):
        session.pop('otp', None)
        return render_template('admin_forgetpassword.html', oform=oform, eform=eform, lform=login_form,
                               value=2, cform=cform)
    flash("Wrong one time password", "warning")
    return render_template('admin_page.html', lform=login_form)


@app.route('/passwordsubmit', methods=['GET', 'POST'])
def password_submit():
    login_form = LoginForm()
    cform = ChangePasswordForm()
    if cform.validate_on_submit():
        mydb = CONNECTION
        mycursor = mydb.cursor()
        hashed_password = generate_password_hash(cform.password.data, method='sha256')
        print(hashed_password)
        sql = "UPDATE admin SET password = %s WHERE email_id = %s"
        email = session['password_update_mail']
        print(email)
        val = (hashed_password, email)
        mycursor.execute(sql, val)
        mydb.commit()
        with app.app_context():
            msg = Message(subject="Password Updated",
                          sender=app.config.get("MAIL_USERNAME"),
                          recipients=[email],  # replace with your email for testing
                          body="Your Password has been updated. If you have not requested a change of password then send a mail to depressiede@gmail.com")
            mail.send(msg)
        session.pop('password_update_mail', None)
    flash("Password Updated", "success")
    return render_template('admin_page.html', lform=login_form)


@app.route('/')
def index():
    login_form = LoginForm()
    eform = EmailForm()
    if app.config['IS_LOGIN']:
        return render_template('admin_result.html', eform=eform)
    else:
        return render_template('admin_page.html', lform=login_form)


if __name__ == '__main__':
    app.run(host='localhost', port='8020')

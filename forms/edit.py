from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, RadioField, DateField
from wtforms.validators import DataRequired


class EditForm(FlaskForm):
    first_name = StringField('Имя:', validators=[DataRequired()])
    last_name = StringField('Фамилия:', validators=[DataRequired()])
    email = EmailField('Почтовый адрес:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль:', validators=[DataRequired()])
    gender = RadioField("Пол:", choices=[("male", "Мужской"), ("female", "Женский")], validators=[DataRequired()])
    date_of_birthday = DateField('Дата рождения:', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

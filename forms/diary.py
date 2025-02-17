from flask_wtf import FlaskForm
from wtforms import TextAreaField, TimeField, RadioField, SubmitField
from wtforms.validators import DataRequired


class DiaryForm(FlaskForm):
    brief_notes = TextAreaField('Краткие заметки:', validators=[DataRequired()],
                                render_kw={"placeholder": "Краткие заметки"})

    sleep_start = TimeField('Время начала сна:', validators=[DataRequired()])

    sleep_end = TimeField('Время окончания сна:', validators=[DataRequired()])

    sleep_imagination = TextAreaField('Содержание сна:', validators=[DataRequired()],
                                      render_kw={"placeholder": "Содержание сна"})

    condition_before = RadioField("Оценка вашего состояния до сна:",
                                 choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"),
                                          ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"), ("10", "10")],
                                 validators=[DataRequired()])

    condition_after = RadioField("Оценка вашего состояния после сна:",
                                 choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"),
                                          ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"), ("10", "10")],
                                 validators=[DataRequired()])

    submit = SubmitField('Сохранить')

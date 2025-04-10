from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField, SelectMultipleField, RadioField
from wtforms.fields.simple import StringField, EmailField, SubmitField, TextAreaField, FileField, BooleanField
from wtforms.validators import DataRequired, Email


class SelectionForm(FlaskForm):
    surname = StringField('', validators=[DataRequired()], render_kw={"placeholder": "Введите фамилию"})
    name = StringField('', validators=[DataRequired()], render_kw={"placeholder": "Введите имя"})
    email = EmailField('', validators=[DataRequired(), Email('Введён некорректный e-mail')],
                       render_kw={"placeholder": "Введите адрес почты"})
    selectEducation = SelectField('Какое у Вас образование?', validators=[DataRequired()], choices=[
        ('Без образования', 'Без образования'),
        ('Начальное', 'Начальное'),
        ('Среднее', 'Среднее'),
        ('Высшее', 'Высшее'),
    ])
    prof = SelectMultipleField('Какие у Вас есть профессии?', choices=[
        ('Инженер-исследователь', 'Инженер-исследователь'),
        ('Инженер-строитель', 'Инженер-строитель'),
        ('Пилот', 'Пилот'),
        ('Метеоролог', 'Метеоролог'),
        ('Инженер по жизнеобеспечению', 'Инженер по жизнеобеспечению'),
        ('Инженер по радиационной защит', 'Инженер по радиационной защите'),
        ('Врач', 'Врач'),
        ('Экзобиолог', 'Экзобиолог'),
    ])
    sex = RadioField('Укажите пол', validators=[DataRequired()], choices=[
        ('sex_male', 'Мужской'),
        ('sex_female', 'Женский'),
    ])
    description = TextAreaField('Почему Вы хотите принять участие в миссии?', validators=[DataRequired()],
                                render_kw={"rows": "6"})
    file = FileField('Приложите фотографию', validators=[DataRequired()])
    access = BooleanField('Готовы остаться на Марсе?', validators=[DataRequired()])
    submit = SubmitField('Отправить')

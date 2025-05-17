from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired


from .loginform import LoginForm

class ExtraLoginForm(FlaskForm):
    username = IntegerField('Id астронавта', validators=[DataRequired()])
    password = PasswordField('Пароль астронавта', validators=[DataRequired()])
    capitan = IntegerField('Id капитана', validators=[DataRequired()])
    capitan_password = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Войти')


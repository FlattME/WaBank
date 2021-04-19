from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class OrderCardForm(FlaskForm):
    fio = StringField('Фамилия Имя Отчество', validators=[DataRequired()])
    tel = StringField('Номер телефона', validators=[DataRequired()])
    nomer = StringField('Номер и серия паспорта', validators=[DataRequired()])
    vidan = StringField('Дата рождения (дд.мм.гггг)', validators=[DataRequired()])
    submit = SubmitField('Submit')

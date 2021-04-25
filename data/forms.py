from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField,\
    TextAreaField, IntegerField, SelectField, TextField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from datetime import datetime


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(
        min=8, max=16, message='Пароль должен быть (от 8 до 16 символов)')])

    password_again = PasswordField('Повторите пароль', validators=[DataRequired(message='Пароли не совпадают'),
                                        EqualTo('password', message='Пароли не совпадают')])

    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])

    age = StringField('Дата рождения (дд.мм.гггг)', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

    def validate_name(self, name):
        excluded_chars = "цукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪЫВАПРОЛДЖЭФЮБЬТИМСЧЯ"
        for char in self.name.data:
            if not (char in excluded_chars):
                raise ValidationError(
                    f"Только кириллица")

    def validate_surname(self, surname):
        excluded_chars = "цукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪЫВАПРОЛДЖЭФЮБЬТИМСЧЯ"
        for char in self.surname.data:
            if not (char in excluded_chars):
                raise ValidationError(
                    f"Только кириллица")

    def validate_age(self, age):
        excluded_chars = ".1234567890"
        c = self.age.data.split(".")
        if len(c) != 3 or (int(c[0]) > 31 or len(c[0]) != 2) or (int(c[1]) > 12 or len(c[1]) != 2) or (
                int(c[2]) > int(str(datetime.date(datetime.now())).split('-')[0]) or len(c[2]) != 4):
            raise ValidationError(f"Неверный формат")
        for char in self.age.data:
            if not (char in excluded_chars):
                raise ValidationError(f"Неверный формат")


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')

    submit = SubmitField('Войти')


class OrderCardForm(FlaskForm):
    fio = StringField('Фамилия Имя Отчество', validators=[DataRequired()])
    tel = StringField('Номер телефона', validators=[DataRequired(), Length(min=11, max=11, message="11 цифр")])
    nomer = StringField(
        'Номер и серия паспорта', validators=[DataRequired(), Length(min=10, max=10, message="10 цифр")])
    vidan = StringField('Дата рождения (дд.мм.гггг)', validators=[DataRequired()])
    add_card = SubmitField('Оформить карту')

    def validate_fio(self, fio):
        excluded_chars = " цукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪЫВАПРОЛДЖЭФЮБЬТИМСЧЯ"
        if (self.fio.data.split()) == 3:
            raise ValidationError(f"Неверный формат")
        for char in self.fio.data:
            if not (char in excluded_chars):
                raise ValidationError(
                    f"Только кириллица")

    def validate_nomer(self, nomer):
        excluded_chars = "1234567890 "
        for char in str(self.nomer.data):
            if not (char in excluded_chars):
                raise ValidationError(
                    f"Только цифры")

    def validate_vidan(self, vidan):
        excluded_chars = ".1234567890"
        c = self.vidan.data.split(".")
        if len(c) != 3 or (int(c[0]) > 31 or len(c[0]) != 2) or (int(c[1]) > 12 or len(c[1]) != 2) or (
                int(c[2]) > int(str(datetime.date(datetime.now())).split('-')[0]) or len(c[2]) != 4):
            raise ValidationError(f"Неверный формат")

        for char in self.vidan.data:
            if not (char in excluded_chars):
                raise ValidationError(
                    f"Неверный формат")


class OrderPensionCardForm(FlaskForm):
    fio = StringField('Фамилия Имя Отчество', validators=[DataRequired()])
    tel = StringField('Номер телефона', validators=[DataRequired(), Length(min=11, max=11, message="11 цифр")])
    nomer = StringField(
        'Номер и серия паспорта', validators=[DataRequired(), Length(min=10, max=10, message="10 цифр")])
    vidan = StringField('Дата рождения (дд.мм.гггг)', validators=[DataRequired()])
    add_card = SubmitField('Оформить карту')

    def validate_fio(self, fio):
        excluded_chars = " цукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪЫВАПРОЛДЖЭФЮБЬТИМСЧЯ"
        if (self.fio.data.split()) == 3:
            raise ValidationError(f"Неверный формат")
        for char in self.fio.data:
            if not (char in excluded_chars):
                raise ValidationError(
                    f"Только кириллица")

    def validate_tel(self, tel):
        excluded_chars = "1234567890"
        for char in str(self.tel.data):
            if not (char in excluded_chars):
                raise ValidationError(
                    f"Только кириллица")


class OrderCreditCardForm(FlaskForm):
    fio = StringField('Фамилия Имя Отчество', validators=[DataRequired()])
    tel = StringField('Номер телефона', validators=[DataRequired(), Length(min=11, max=11, message="11 цифр")])
    nomer = StringField(
        'Номер и серия паспорта', validators=[DataRequired(), Length(min=10, max=10, message="10 цифр")])
    vidan = StringField('Дата рождения (дд.мм.гггг)', validators=[DataRequired()])
    place_of_work = StringField('Место работы', validators=[DataRequired()])
    sum_ = IntegerField("Сумма кредита", validators=[DataRequired()])
    add_card = SubmitField('Оформить кредитную карту')

    def validate_fio(self, fio):
        excluded_chars = " цукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪЫВАПРОЛДЖЭФЮБЬТИМСЧЯ"
        if (self.fio.data.split()) == 3:
            raise ValidationError(f"Неверный формат")
        for char in self.fio.data:
            if not (char in excluded_chars):
                raise ValidationError(
                    f"Только кириллица")

    def validate_nomer(self, nomer):
        excluded_chars = "1234567890 "
        for char in str(self.nomer.data):
            if not (char in excluded_chars):
                raise ValidationError(
                    f"Только цифры")

    def validate_vidan(self, vidan):
        excluded_chars = ".1234567890"
        c = self.vidan.data.split(".")
        if len(c) != 3 or (int(c[0]) > 31 or len(c[0]) != 2) or (int(c[1]) > 12 or len(c[1]) != 2) or (
                int(c[2]) > int(str(datetime.date(datetime.now())).split('-')[0]) or len(c[2]) != 4):
            raise ValidationError(f"Неверный формат")
        for char in self.vidan.data:
            if not (char in excluded_chars):
                raise ValidationError(
                    f"Неверный формат")


class OrderCreditForm(FlaskForm):
    fio = StringField('Фамилия Имя Отчество', validators=[DataRequired()])
    tel = StringField('Номер телефона', validators=[DataRequired(), Length(min=11, max=11, message="11 цифр")])
    nomer = StringField(
        'Номер и серия паспорта', validators=[DataRequired(), Length(min=10, max=10, message="10 цифр")])
    place_of_work = StringField('Место работы', validators=[DataRequired()])
    vidan = StringField('Дата рождения (дд.мм.гггг)', validators=[DataRequired()])
    sum_ = IntegerField("Сумма кредита (руб.)", validators=[DataRequired()])
    transfer_card = SelectField('Куда перевести деньги?', choices={}, validators=[DataRequired()])
    transmitting_secret_code = StringField('Код безопасности', validators=[DataRequired()])
    add_card = SubmitField('Оформить кредит')

    def validate_transmitting_secret_code(self, transmitting_secret_code):
        excluded_chars = "1234567890"
        for char in str(self.transmitting_secret_code.data):
            if not (char in excluded_chars):
                raise ValidationError("Только цифры")

    def validate_fio(self, fio):
        excluded_chars = " цукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪЫВАПРОЛДЖЭФЮБЬТИМСЧЯ"
        if (self.fio.data.split()) == 3:
            raise ValidationError(f"Неверный формат")
        for char in self.fio.data:
            if not (char in excluded_chars):
                raise ValidationError(
                    f"Только кириллица")

    def validate_nomer(self, nomer):
        excluded_chars = "1234567890 "
        for char in str(self.nomer.data):
            if not (char in excluded_chars):
                raise ValidationError(
                    f"Только цифры")

    def validate_sum(self, sum_, min_=5000, max_=50000):
        excluded_chars = "1234567890"
        for char in str(self.sum_.data):
            if not (char in excluded_chars):
                raise ValidationError(
                    f"Только цифры")

    def validate_vidan(self, vidan):
        excluded_chars = ".1234567890"
        c = self.vidan.data.split(".")
        if len(c) != 3 or (int(c[0]) > 31 or len(c[0]) != 2) or (int(c[1]) > 12 or len(c[1]) != 2) or (
                int(c[2]) > int(str(datetime.date(datetime.now())).split('-')[0]) or len(c[2]) != 4):
            raise ValidationError(f"Неверный формат")
        for char in self.vidan.data:
            if not (char in excluded_chars):
                raise ValidationError(f"Неверный формат")


class OrderСontributionForm(FlaskForm):
    fio = StringField('Фамилия Имя Отчество', validators=[DataRequired()])
    tel = StringField('Номер телефона', validators=[DataRequired(), Length(min=11, max=11, message="11 цифр")])
    nomer = StringField(
        'Номер и серия паспорта', validators=[DataRequired(), Length(min=10, max=10, message="10 цифр")])
    sum_ = IntegerField("Сумма вклада (руб.)", validators=[DataRequired()])
    vidan = StringField('Дата рождения (дд.мм.гггг)', validators=[DataRequired()])
    transfer_card = SelectField('Карта', choices={}, validators=[DataRequired()])
    transmitting_secret_code = StringField('Код безопасности', validators=[DataRequired()])
    add_card = SubmitField('Оформить вклад')

    def validate_fio(self, fio):
        excluded_chars = " цукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪЫВАПРОЛДЖЭФЮБЬТИМСЧЯ"
        if (self.fio.data.split()) == 3:
            raise ValidationError(f"Неверный формат")

        for char in self.fio.data:
            if not (char in excluded_chars):
                raise ValidationError(f"Только кириллица")

    def validate_nomer(self, nomer):
        excluded_chars = "1234567890 "
        for char in str(self.nomer.data):
            if not (char in excluded_chars):
                raise ValidationError(f"Только цифры")

    def validate_sum(self, sum_, min_=5000, max_=50000):
        excluded_chars = "1234567890"
        for char in str(self.sum_.data):
            if not (char in excluded_chars):
                raise ValidationError(f"Только цифры")

    def validate_vidan(self, vidan):
        excluded_chars = ".1234567890"
        c = self.vidan.data.split(".")
        if len(c) != 3 or (int(c[0]) > 31 or len(c[0]) != 2) or (int(c[1]) > 12 or len(c[1]) != 2) or (int(c[2]) > int(str(datetime.date(datetime.now())).split('-')[0]) or len(c[2]) != 4):
            raise ValidationError(f"Неверный формат")
        for char in self.vidan.data:
            if not (char in excluded_chars):
                raise ValidationError(f"Неверный формат")


class AccountForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    age = StringField('Дата рождения (дд.мм.гггг)', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

    def validate_surname(self, surname):
        excluded_chars = " цукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪЫВАПРОЛДЖЭФЮБЬТИМСЧЯ"
        for char in self.surname.data:
            if not (char in excluded_chars):
                raise ValidationError(
                    f"Только кириллица")

    def validate_name(self, name):
        excluded_chars = " цукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪЫВАПРОЛДЖЭФЮБЬТИМСЧЯ"
        for char in self.name.data:
            if not (char in excluded_chars):
                raise ValidationError(
                    f"Только кириллица")


class SupportForm(FlaskForm):
    email = EmailField('Адрес электронной почты', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    user_message = TextAreaField('Сообщение', validators=[DataRequired()])
    submit = SubmitField('Отправить')

    def validate_name(self, name):
        excluded_chars = "цукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪЫВАПРОЛДЖЭФЮБЬТИМСЧЯ"
        for char in self.name.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Только латиница")

    def validate_user_message(self, user_message):
        excluded_chars = "цукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪЫВАПРОЛДЖЭФЮБЬТИМСЧЯ"
        for char in self.user_message.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Только латиница")


class TransfersForm(FlaskForm):
    recipient_input = StringField('Номер карты получателя', validators=[DataRequired()])
    transmitting_input = SelectField('Название карты', choices={}, validators=[DataRequired()])
    transmitting_secret_code = StringField('Код безопасности', validators=[DataRequired()])
    transfer_amount = IntegerField("Сумма перевода", validators=[DataRequired()])
    submit = SubmitField('Перевести')

    def validate_transmitting_secret_code(self, transmitting_secret_code):
        excluded_chars = "1234567890"
        for char in str(self.transmitting_secret_code.data):
            if not (char in excluded_chars):
                raise ValidationError("Только цифры")


class TopUpForm(FlaskForm):
    transmitting_input = SelectField('Название карты', choices={}, validators=[DataRequired()])
    transfer_amount = IntegerField("Сумма пополнения", validators=[DataRequired()])
    submit = SubmitField('Пополнить')

    def validate_transfer_amount(self, transfer_amount):
        excluded_chars = "1234567890"
        for char in str(self.transfer_amount.data):
            if not (char in excluded_chars):
                raise ValidationError("Только цифры")


class PayOffCreditForm(FlaskForm):
    credit_name = SelectField('Название кредита', choices={}, validators=[DataRequired()])
    transmitting_secret_code = StringField('Код безопасности', validators=[DataRequired()])
    pay_off_card = SelectField('Карта', choices={}, validators=[DataRequired()])
    transfer_amount = IntegerField("Сумма пополнения", validators=[DataRequired()])
    submit = SubmitField('Перевести')

    def validate_transfer_amount(self, transfer_amount):
        excluded_chars = "1234567890"
        for char in str(self.transfer_amount.data):
            if not (char in excluded_chars):
                raise ValidationError("Только цифры")


class AdminForm(FlaskForm):
    check_credits_and_contributions = SubmitField('Проверить кредиты и вклады')
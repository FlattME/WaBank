from datetime import datetime, date
import sqlalchemy
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import orm

from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase
import random


db = SqlAlchemyBase


class Users(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modifed_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.date(datetime.now()))
    admin = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)

    def __repr__(self):
        return f'{self.id} {self.surname} {self.name} {self.address} {self.email} {self.admin}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Cards(SqlAlchemyBase, UserMixin):
    __tablename__ = 'cards'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)
    sum_ = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    fio = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    tel = sqlalchemy.Column(sqlalchemy.String(12), nullable=False)
    nomer = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)
    vidan = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)
    card_number = sqlalchemy.Column(sqlalchemy.String(17), nullable=True)
    pin = sqlalchemy.Column(sqlalchemy.String(4), nullable=False)
    secret_code = sqlalchemy.Column(sqlalchemy.String(3), nullable=False)
    service_price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    privileges = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    transfer_history = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    block = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=0)
    user_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"), nullable=True)
    d = str(datetime.date(datetime.now())).split('-')
    d = date(*list(map(int, [str((int(d[0]) + 3))] + d[1:])))
    modifed_date = sqlalchemy.Column(sqlalchemy.DateTime, default=d)

    def __repr__(self):
        return f"{self.name}, {self.id}, {self.sum_}, {self.card_number}, {self.secret_code}, {self.transfer_history}, {self.block}, {self.modifed_date}"

    def set_pin(self, pin):
        self.hashed_pin = generate_password_hash(pin)

    def check_password(self, pin):
        return check_password_hash(self.pin, pin)


class PensionСards(SqlAlchemyBase, UserMixin):
    __tablename__ = 'pension_cards'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    sum_ = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    fio = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    tel = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    nomer = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    vidan = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    card_number = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    pin = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    secret_code = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    service_price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    privileges = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    transfer_history = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    block = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=0)
    user_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"), nullable=True)
    d = str(datetime.date(datetime.now())).split('-')
    d = date(*list(map(int, [str((int(d[0]) + 3))] + d[1:])))
    modifed_date = sqlalchemy.Column(sqlalchemy.DateTime, default=d)

    def __repr__(self):
        return f"{self.name}, {self.id}, {self.sum_}, {self.card_number}, {self.secret_code}, {self.transfer_history}, {self.block}, {self.modifed_date}"

    def set_pin(self, pin):
        self.hashed_pin = generate_password_hash(pin)

    def check_password(self, pin):
        return check_password_hash(self.pin, pin)


class CreditCards(SqlAlchemyBase, UserMixin):
    __tablename__ = 'credit_cards'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    sum_ = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    start_sum = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    fio = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    tel = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    nomer = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    vidan = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    place_of_work = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    term = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    percent = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    nonpercent = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    monthly_percent = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    card_number = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    pin = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    secret_code = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    transfer_history = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    block = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=0)
    user_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"), nullable=True)
    d = str(datetime.date(datetime.now())).split('-')
    d = date(*list(map(int, [str((int(d[0]) + 3))] + d[1:])))
    modifed_date = sqlalchemy.Column(sqlalchemy.DateTime, default=d)

    def __repr__(self):
        return f"{self.name}, {self.id}, {self.sum_}, {self.card_number}, {self.secret_code}, {self.sum_}, {self.percent}, {self.monthly_percent}, {self.transfer_history}, {self.block}, {self.modifed_date}"

    def set_pin(self, pin):
        self.hashed_pin = generate_password_hash(pin)

    def check_password(self, pin):
        return check_password_hash(self.pin, pin)


class Credits(SqlAlchemyBase, UserMixin):
    __tablename__ = 'credits'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    sum_ = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    start_sum = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    fio = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    tel = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    nomer = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    vidan = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    place_of_work = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    percent = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    monthly_percent = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    transfer_card = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    transfer_history = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    block = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=0)
    user_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"), nullable=True)
    modifed_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.date(datetime.now()))

    def __repr__(self):
        return f"{self.name}, {self.id}, {self.sum_}, {self.start_sum}, {self.percent}, {self.transfer_history}, {self.block}, {self.monthly_percent}"

    def set_pin(self, pin):
        self.hashed_pin = generate_password_hash(pin)

    def check_password(self, pin):
        return check_password_hash(self.pin, pin)


class Сontributions(SqlAlchemyBase, UserMixin):
    __tablename__ = 'contributions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    sum_ = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    fio = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    tel = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    nomer = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    vidan = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    percent = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    transfer_card = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    transfer_history = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    block = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=0)
    user_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"), nullable=True)
    d = str(datetime.date(datetime.now())).split('-')
    d = date(*list(map(int, [str((int(d[0]) + 3))] + d[1:])))
    modifed_date = sqlalchemy.Column(sqlalchemy.DateTime, default=d)

    def __repr__(self):
        return f"{self.name}, {self.id}, {self.sum_}, {self.percent}, {self.transfer_history}, {self.block}"


class Reviews(SqlAlchemyBase, UserMixin):
    __tablename__ = 'reviews'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    mail = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    message = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    def __repr__(self):
        return f"{self.name}, {self.mail}, {self.message}"
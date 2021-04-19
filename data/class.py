import datetime
import sqlalchemy
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import orm

from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase
import random


db = SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modifed_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f'{self.id} {self.surname} {self.name} {self.address} {self.email}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Cards(SqlAlchemyBase, UserMixin):
    __tablename__ = 'cards'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    sum_ = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    fio = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    tel = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    nomer = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    vidan = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    card_number = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    pin = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"), nullable=True)
    modifed_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"{self.name}, {self.sum_}, {self.card_number}"

    def set_pin(self, pin):
        self.hashed_pin = generate_password_hash(pin)

    def check_password(self, pin):
        return check_password_hash(self.pin, pin)


class CreditCard(SqlAlchemyBase, UserMixin):
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
    term = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    percent = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    nonpercent = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    card_number = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    pin = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    modifed_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    user_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"), nullable=True)

    def __repr__(self):
        return f"{self.name}, {self.sum_}, {self.card_number}"

    def set_pin(self, pin):
        self.hashed_pin = generate_password_hash(pin)

    def check_password(self, pin):
        return check_password_hash(self.pin, pin)

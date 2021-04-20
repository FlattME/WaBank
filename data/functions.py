import random
import sqlite3
import smtplib
import time
from datetime import datetime, date
import datetime as dtime
import smtplib, ssl
from .classes import CreditCards, Credits, Сontributions, Cards, PensionСards


from data import db_session


def set_credit_sum(id, sum_, percent, daily_percentage):
    if sum_ <= 0:
        con = sqlite3.connect('../db/users_db.sqlite')
        cur = con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        cur.execute(
            f"DELETE FROM credits WHERE id = {id}")
        con.commit()
        con.close()
    else:
        con = sqlite3.connect('../db/users_db.sqlite')
        cur = con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        cur.execute(
            f"UPDATE credits SET percent = {percent + daily_percentage}, sum_ = {sum_ + ((sum_ * percent) / 100)} WHERE id = {id}")
        con.commit()
        con.close()


def set_credit_cards_sum(id, moddifid_date, after_nonpercent_time, start_sum, sum_, percent, daily_percentage):
    print(after_nonpercent_time, moddifid_date.split()[0].split("-"))

    c = list(map(int, str(dtime.date(*list(map(int, moddifid_date.split()[0].split("-"))))).split('-')))
    print(c, type(c))
    c[-1] = c[-1] + after_nonpercent_time
    print(c, type(c))
    if datetime.now().date() > dtime.date(*c) and sum_ < start_sum:
        con = sqlite3.connect('../db/users_db.sqlite')
        cur = con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        cur.execute(
            f"UPDATE credits SET percent = {percent + daily_percentage}, sum_ = {start_sum + ((sum_ * percent) / 100)} WHERE id = {id}")
        con.commit()
        con.close()


def update_transfers(tablename, card_name, sum_, znak, id, percent=0):
    con = sqlite3.connect('db/users_db.sqlite')
    print(card_name)
    cur = con.cursor()
    sum_d = cur.execute(f"SELECT sum_ FROM {tablename} WHERE name = '{card_name}' AND user_id = '{id}'").fetchall()[0][0]
    print(sum_d)
    print(sum_)

    # Получили результат запроса, который ввели в текстовое поле
    print(eval(f'{sum_d} {znak} {sum_ + ((percent * sum_)/100)}'))
    cur.execute(
        f"UPDATE {tablename} SET sum_ = {eval(f'{sum_d} {znak} {sum_ + ((percent * sum_)/100)}')} WHERE name = '{card_name}' AND user_id = '{id}'").fetchall()
    con.commit()
    con.close()


def check_credit_sum(tablename, credit_name, id):
    con = sqlite3.connect('db/users_db.sqlite')
    cur = con.cursor()
    sum_d = cur.execute(f"SELECT sum_, start_sum FROM {tablename} WHERE name = '{credit_name}' AND user_id = '{id}'").fetchall()[0]
    con.close()
    return sum_d


def calculate_age(born):
    print(born)
    born = date(int(born[0]), int(born[1]), int(born[2]))
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def set_all():
    if str(datetime.date(datetime.now())).split('-')[-1] == '25':
        db_sess = db_session.create_session()
        print(db_sess.query(Credits).all())
        for credit in [(i.name, i.id, int(i.sum_), int(i.start_sum), int(i.percent), int(i.monthly_percent)) for i in db_sess.query(Credits).all()]:
            con = sqlite3.connect('../db/users_db.sqlite')
            cur = con.cursor()
            if credit[2] > (credit[3] - (credit[3] / 3)):
                cur.execute(
                    f"UPDATE credits SET sum_ = {check_credit_sum('credits', credit[0])[0] + ((check_credit_sum('credits', credit[0])[0] * credit[4]) / 100)}, percent = {credit[4] + credit[5]}, monthly_percent = {credit[4] + 1} WHERE name={credit[0]} AND id = '{credit[1]}'").fetchall()
            else:
                cur.execute(
                    f"UPDATE credits SET sum_ = {check_credit_sum('credits', credit[0])[0] + ((check_credit_sum('credits', credit[0])[0] * credit[4]) / 100)}").fetchall()

            con.commit()
            con.close()

        for c_card in [(i.name, i.id, int(i.sum_), int(i.start_sum), i.card_number, i.secret_code, int(i.percent), int(i.monthly_percent)) for i in db_sess.query(CreditCards).all()]:
            con = sqlite3.connect('../db/users_db.sqlite')
            cur = con.cursor()
            if c_card[2] > (c_card[3] - (c_card[3] / 24)):
                cur.execute(
                    f"UPDATE credit_cards SET sum_ = {check_credit_sum('credit_cards', c_card[0])[0] + ((check_credit_sum('credit_cards', c_card[0])[0] * c_card[-2]) / 100)}, percent = {c_card[-2] + c_card[-1]}, monthly_percent = {c_card[-1] + 1} WHERE name={c_card[0]} AND user_id = '{c_card[1]}'").fetchall()
            else:
                  cur.execute(
                    f"UPDATE credit_cards SET sum_ = {check_credit_sum('credit_cards', c_card[0])[0] + ((check_credit_sum('credit_cards', c_card[0])[0] * c_card[-2]) / 100)}").fetchall()

            con.commit()
            con.close()

        for cntrbtn in [(i.name, i.id, int(i.sum_), int(i.start_sum), i.card_number, i.secret_code, int(i.percent), int(i.monthly_percent)) for i in db_sess.query(CreditCards).all()]:
            con = sqlite3.connect('../db/users_db.sqlite')
            cur = con.cursor()
            cur.execute(f"UPDATE credit_cards SET sum_ = {check_credit_sum('contributions', cntrbtn[0])[0] + ((check_credit_sum('contributions', cntrbtn[0])[0] * cntrbtn[-2]) / 100)} WHERE name={cntrbtn[0]} AND user_id = '{cntrbtn[1]}'").fetchall()

            con.commit()
            con.close()

        all_cards = [(card.name, card.sum_, card.card_number, card.secret_code, card.modifed_date, card.id) for card in db_sess.query(Cards).all()] + \
                   [(card.name, card.sum_, card.card_number, card.secret_code, card.modifed_date, card.id) for card in
                    db_sess.query(CreditCards).all()] + \
                   [(card.name, card.sum_, card.card_number, card.secret_code, card.modifed_date, card.id) for card in
                    db_sess.query(PensionСards).all()]

        for card in all_cards:
            if calculate_age(card[-2]) > calculate_age(datetime.date(datetime.now())):
                con = sqlite3.connect('../db/users_db.sqlite')
                cur = con.cursor()
                # Получили результат запроса, который ввели в текстовое поле
                if 'Кредитная' in card[0]:
                    g = 'credit_cards'
                elif 'Дебютовая' in card[0]:
                    g = 'cards'
                else:
                    g = 'pension_cards'

                cur.execute(f"DELETE FROM {g} WHERE name = {card[0]} AND id = '{card[-1]}'")
                con.commit()
                con.close()
    return


def update_pay_off(tablename, card_name, credit_name, sum_, id):
    con = sqlite3.connect('db/users_db.sqlite')

    cur = con.cursor()
    sum_d = cur.execute(f"SELECT sum_ FROM {tablename} WHERE name = '{card_name}' AND user_id = '{id}'").fetchall()[0][0]

    # Получили результат запроса, который ввели в текстовое поле
    cur.execute(
        f"UPDATE {tablename} SET sum_ = {int(sum_d) - int(sum_)} WHERE name = '{card_name}' AND user_id = '{id}'").fetchall()
    con.commit()
    con.close()

    con = sqlite3.connect('db/users_db.sqlite')
    cur = con.cursor()
    sum_c = cur.execute(f"SELECT sum_ FROM credits WHERE name = '{credit_name}' AND user_id = '{id}'").fetchall()[0][0]

    cur.execute(
        f"UPDATE credits SET sum_ = {sum_c - sum_} WHERE name = '{credit_name}' AND user_id = '{id}'").fetchall()
    con.commit()
    con.close()


def remove_credit(credit_name, id):
    con = sqlite3.connect('db/users_db.sqlite')
    cur = con.cursor()

    cur.execute(f"DELETE FROM credit WHERE name = '{credit_name}' AND user_id = '{id}'").fetchall()
    con.commit()
    con.close()


def sent_mail(mail, name):
    port = 465

    sender, password = "bbwabank2020suppor720@yandex.ru", "qwertyuiop0987654321"

    recieve = mail
    message = f"""\
        Subject: WaBank Support for {name}
        
        Your appeal 
        will
        be considered 
        (approximately eternity)!
        
        Gladly WaBank"""

    context = ssl.create_default_context()

    print("Starting to send")
    try:
        with smtplib.SMTP_SSL("smtp.yandex.ru", port, context=context) as server:
            server.login(sender, password)
            server.sendmail(sender, recieve, message)
            return "sent email!"
    except:
        return 'Spam ERROR'


def read_sqlfile(name, table, columns, params=''):
    filename = sqlite3.connect(name)
    cur = filename.cursor()
    result = cur.execute(f"SELECT {columns} FROM {table} {params}").fetchall()
    filename.close()
    return result


def rand(n):
    r = ''
    for i in range(n):
        r += str(random.randint(0, 9))
    return r

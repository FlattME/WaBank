from flask import Flask, render_template, request, url_for, redirect
# from flask_ngrok import run_with_ngrok
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import date, datetime
import sqlite3

from data import db_session
from data.functions import rand, read_sqlfile, sent_mail, set_all, calculate_age, \
    set_credit_sum, update_transfers, set_credit_cards_sum, update_pay_off, check_credit_sum, remove_credit, my_cards
from data.classes import Users, Cards, CreditCards, PensionСards, Credits, Reviews, Сontributions
from data.forms import RegisterForm, OrderCardForm, LoginForm, AccountForm, SupportForm,\
    OrderCreditForm, TransfersForm, TopUpForm, OrderCreditCardForm, PayOffCreditForm, OrderСontributionForm, AdminForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

options = {"Кредиты": '/directions/credits',
           "Карты": '/directions/cards',
           "Вклады": '/directions/contributions',
           "Информация о банке": '/directions/information',
           "Поддержка": '/directions/support'}


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Users).get(user_id)


# Основная страница
@app.route("/")
@app.route("/index")
def index():
    db_sess = db_session.create_session()
    users = db_sess.query(Users).all()

    names = {name.id: (name.surname, name.name) for name in users}

    if current_user.is_authenticated:
        print(current_user.admin)
        cards_ = db_sess.query(Cards).filter(Cards.user_id == str(current_user.id)).all()

    return render_template("index.html", names=names, options=options)


# Аккаунт
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = AccountForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = Users()
            user.email = form.email.data
            user.password = form.password.data
            user.surname = form.surname.data
            user.name = form.name.data
            user.age = form.age.data
            user.address = form.address.data
            db_sess.merge(current_user)
            db_sess.commit()
            return redirect('/')
        return render_template('account.html', title='Личный кабинет', form=form, options=options)
    else:
        return render_template(
            'info.html', options=options,
            message='Необходимо зарегестрироваться')


# Карты пользователя
@app.route('/account/account_cards', methods=["GET", "POST"])
def account_cards():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        cards_ = [(card.name, card.sum_, card.card_number, card.secret_code, list(map(lambda x: x.split('|'), str(card.transfer_history).split(';')[1:]))) for card in
                     db_sess.query(Cards).filter(Cards.user_id == current_user.id).all()] + \
                    [(card.name, card.sum_, card.card_number, card.secret_code, list(map(lambda x: x.split('|'), str(card.transfer_history).split(';')[1:]))) for card in
                     db_sess.query(CreditCards).filter(CreditCards.user_id == current_user.id).all()] + \
                    [(card.name, card.sum_, card.card_number, card.secret_code, list(map(lambda x: x.split('|'), str(card.transfer_history).split(';')[1:]))) for card in
                     db_sess.query(PensionСards).filter(PensionСards.user_id == current_user.id).all()]
        credits_ = [(credit.name, credit.sum_, credit.percent, credit.monthly_percent, list(map(lambda x: x.split('|'), str(credit.transfer_history).split(';')[1:]))) for credit in db_sess.query(Credits).filter(Credits.user_id == current_user.id).all()]
        o = [(ow.name, ow.sum_, ow.percent, list(map(lambda x: x.split('|'), str(ow.transfer_history).split(';')[1:]) )) for ow in db_sess.query(Сontributions).filter(Сontributions.user_id == current_user.id).all()]
        print(cards_)
        print(credits_)
        print(o)

        return render_template('account_cards.html', options=options, cards_=cards_, credits_=credits_, o=o)
    else:
        return render_template(
            'info.html', options=options,
            message='Необходимо зарегестрироваться')


@app.route('/account/transfers', methods=["GET", "POST"])
def transfers():
    form = TransfersForm()
    if current_user.is_authenticated:
        db_sess = db_session.create_session()

        my_cards_ = [(card.name, card.sum_, card.card_number, card.secret_code)
                     for card in db_sess.query(Cards).filter(Cards.user_id == current_user.id).all()] + \
                    [(card.name, card.sum_, card.card_number, card.secret_code)
                     for card in db_sess.query(CreditCards).filter(CreditCards.user_id == current_user.id).all()] + \
                    [(card.name, card.sum_, card.card_number, card.secret_code)
                     for card in db_sess.query(PensionСards).filter(PensionСards.user_id == current_user.id).all()]

        all_cards = [(card.name, card.sum_, card.card_number, card.secret_code)
                     for card in db_sess.query(Cards).all()] + \
                    [(card.name, card.sum_, card.card_number, card.secret_code)
                     for card in db_sess.query(CreditCards).all()] + \
                    [(card.name, card.sum_, card.card_number, card.secret_code)
                     for card in db_sess.query(PensionСards).all()]

        form.transmitting_input.choices = [(card_[0]) for card_ in my_cards_]
        print(my_cards_)
        if form.validate_on_submit():
            for card in my_cards_:
                if card[0] == form.transmitting_input.data:
                    print(card[-1])

                    if form.transmitting_secret_code.data != str(card[-1]):
                        return render_template('transfers.html', form=form, options=options, cards_=my_cards_,
                                               message='Неверный код безопасности')

                    if not (card[1] >= form.transfer_amount.data):
                        return render_template('transfers.html', form=form, options=options,
                                               cards_=my_cards_, message='Недостаточно средств')
                    print(current_user.id)
                    if 'Дебютовая' in card[0]:
                        update_transfers('cards', card[2], form.transfer_amount.data, '-')

                    elif 'Кредитная' in card[0]:
                        update_transfers('credit_cards', card[2], form.transfer_amount.data, '-')
                    else:
                        update_transfers('pension_cards', card[2], form.transfer_amount.data, '-')

                    for al in all_cards:
                        if str(form.recipient_input.data) == str(al[2]):

                            if 'Дебютовая' in al[0]:
                                update_transfers('cards', al[2], form.transfer_amount.data, '+')
                            elif 'Кредитная' in al[0]:
                                update_transfers('credit_cards', al[2], form.transfer_amount.data, '+')
                            else:
                                update_transfers('pension_cards', al[2], form.transfer_amount.data, '+')
                    return render_template(
                        'transfers.html', form=form, options=options,
                        cards_=my_cards_, message='Перевод выполнен успешно')
            print(form.transmitting_input, form.transmitting_input.data)

        return render_template(
            'transfers.html', form=form, options=options, cards_=my_cards_)
    else:
        return render_template(
            'info.html', options=options,
            message='Сначала необходимо зарегестрироваться')


@app.route('/account/top_up', methods=["GET", "POST"])
def top_up():
    form = TopUpForm()
    if current_user.is_authenticated:
        db_sess = db_session.create_session()

        my_cards_ = [(card.name, card.sum_, card.card_number, card.secret_code)
                     for card in db_sess.query(Cards).filter(Cards.user_id == current_user.id).all()] + \
                    [(card.name, card.sum_, card.card_number, card.secret_code)
                     for card in db_sess.query(CreditCards).filter(CreditCards.user_id == current_user.id).all()] + \
                    [(card.name, card.sum_, card.card_number, card.secret_code)
                     for card in db_sess.query(PensionСards).filter(PensionСards.user_id == current_user.id).all()]

        form.transmitting_input.choices = [(card_[0]) for card_ in my_cards_]
        print(my_cards_)
        if form.validate_on_submit():
            for card in my_cards_:
                if card[0] == form.transmitting_input.data:

                    if 'Дебютовая' in card[0]:
                        update_transfers('cards', card[2], form.transfer_amount.data, '+')

                    elif 'Кредитная' in card[0]:
                        update_transfers('credits', card[2], form.transfer_amount.data, '+')
                    else:
                        update_transfers('pension_cards', card[2], form.transfer_amount.data, '+')

                    return render_template(
                        'top_up.html', form=form, options=options,
                        cards_=my_cards_, message='Пополнение выполнен успешно')
            print(form.transmitting_input, form.transmitting_input.data)

        return render_template(
            'top_up.html', form=form, options=options, cards_=my_cards_)
    else:
        return render_template(
            'info.html', options=options,
            message='Сначала необходимо зарегестрироваться')


# Данные карты (после оформления)
@app.route('/card_ready', methods=['GET', "POST"])
def card_ready(
        card_name, modifed_date, pin='', secret_code='', card_number='', credit_sum='', credit_payment='', income_='', percent=''):
    return render_template('card_ready.html', options=options, card_name=card_name, card_pin=pin,
        secret_code=secret_code, card_number=card_number, modifed_date=modifed_date,
        credit_sum=credit_sum, credit_payment=credit_payment, percent=percent, income_=income_)


# Направления
@app.route('/directions')
def directions():
    return render_template(
        'cards.html', options=options)


# Кредиты
@app.route('/directions/credits/', methods=['GET', "POST"])
def credits():
    return render_template('credits.html', options=options)


# Оформление кредита
@app.route('/directions/credits/order_credit', methods=['GET', "POST"])
def order_credit():
    if current_user.is_authenticated:
        form = OrderCreditForm()
        db_sess = db_session.create_session()

        my_cards_ = [(card.name, card.sum_, card.card_number, card.secret_code) for card in
                     db_sess.query(Cards).filter(Cards.user_id == current_user.id).all()] + \
                    [(card.name, card.sum_, card.card_number, card.secret_code) for card in
                     db_sess.query(CreditCards).filter(CreditCards.user_id == current_user.id).all()] + \
                    [(card.name, card.sum_, card.card_number, card.secret_code) for card in
                     db_sess.query(PensionСards).filter(PensionСards.user_id == current_user.id).all()]

        form.transfer_card.choices = [(card_[0]) for card_ in my_cards_]

        if form.validate_on_submit():
            percent = request.args.get('percent')
            monthly_percent = request.args.get('monthly_percent')

            form.transfer_card.choices = [(card_[0]) for card_ in my_cards_]

            if form.sum_.data < 5000 or form.sum_.data > 500000:

                return render_template(
                    'order_credit.html', title='Оформление кредита',
                    form=form, options=options, message="Неверная сумма кредита")

            c = len(db_sess.query(Credits).filter(Credits.user_id == current_user.id).all()) + 1

            if c > 2:
                return render_template(
                    'info.html', options=options, message="Нельзя оформить так много кредитов")
            g = 0

            for i in my_cards_:
                if i[0] == form.transfer_card.data:
                    g = i[-1]
            if form.transmitting_secret_code.data != g:
                return render_template(
                    'info.html', options=options, message="Неверный код безопасности")

            for card in my_cards_:
                if card[0] == form.transfer_card.data:
                    if 'Дебютовая' in card[0]:
                        update_transfers('cards', card[2], form.sum_.data, '-')
                    elif 'Кредитная' in card[0]:
                        update_transfers('credits', card[2], form.sum_.data, '-')
                    else:
                        update_transfers('pension_cards', card[2], form.sum_.data, '-')

            name = f"Кредит {c}"
            credit = Credits(
                fio=form.fio.data,
                name=name,
                sum_=form.sum_.data,
                start_sum=form.sum_.data,
                tel=form.tel.data,
                nomer=form.nomer.data,
                vidan=form.vidan.data,
                place_of_work=form.place_of_work.data,
                monthly_percent=int(monthly_percent),
                percent=int(percent),
                transfer_history='',
                transfer_card=form.transfer_card.data,
                user_id=current_user.id)

            db_sess.add(credit)
            db_sess.commit()
            return card_ready(
                name, datetime.date(datetime.now()), credit_sum=form.sum_.data,
                credit_payment=str(int(form.sum_.data) / 24), percent=percent)

        return render_template(
            'order_credit.html', title='Оформление кредита', form=form, options=options, cards_=my_cards_)
    else:
        return render_template(
            'info.html', options=options,
            message='Сначала необходимо зарегестрироваться')


# Погашение кредита

@app.route('/directions/credits/pay_off_credit', methods=['GET', "POST"])
def pay_off_credit():
    if current_user.is_authenticated:
        form = PayOffCreditForm()
        db_sess = db_session.create_session()
        my_cards = [(card.name, card.sum_, card.card_number, card.secret_code) for card in
                    db_sess.query(Cards).filter(Cards.user_id == current_user.id).all()] + \
                   [(card.name, card.sum_, card.card_number, card.secret_code) for card in
                    db_sess.query(CreditCards).filter(CreditCards.user_id == current_user.id).all()] + \
                   [(card.name, card.sum_, card.card_number, card.secret_code) for card in
                    db_sess.query(PensionСards).filter(PensionСards.user_id == current_user.id).all()]

        my_credits = [(credit.name, credit.sum_, credit.percent)
                      for credit in db_sess.query(Credits).filter(Credits.user_id == current_user.id).all()]

        form.credit_name.choices = [(card_[0]) for card_ in my_credits]
        form.pay_off_card.choices = [(card_[0]) for card_ in my_cards]
        print(21)
        if form.validate_on_submit():
            print(11)
            for card in my_cards:
                if card[0] == form.pay_off_card.data:
                    print(3)
                    if form.transmitting_secret_code.data != str(card[-1]):
                        return render_template('transfers.html', form=form, options=options, cards_=my_cards,
                                               message='Неверный код безопасности')

                    if int(form.transfer_amount.data) > card[1]:
                        return render_template(
                            'pay_off_credit.html', title='Оформление кредита',
                            form=form, options=options, message="Недостаточно средств")
                    print(0)
                    if 'Дебютовая' in card[0]:
                        update_pay_off('cards', card[0], form.credit_name.data, form.transfer_amount.data, current_user.id)
                    elif 'Пенсионная' in card[0]:
                        update_pay_off('pension_cards', card[0], form.credit_name.data, form.transfer_amount.data, current_user.id)
                    else:
                        update_pay_off('credit_cards', card[0], form.credit_name.data, form.transfer_amount.data, current_user.id)

                    credit_sum = check_credit_sum('credits', form.credit_name.data, current_user.id)[0]
                    if credit_sum <= 0:
                        remove_credit(form.credit_name.data, current_user.id)
                        return render_template(
                            'pay_off_credit.html',  options=options, form=form, my_cards=my_cards,
                            my_credits=my_credits, message='Перевод прошол успешно. Ваш кредит удален')
                    else:
                        return render_template(
                            'pay_off_credit.html', options=options, form=form, my_cards=my_cards, my_credits=my_credits,
                            message=f'Перевод прошол успешно. Вам осталость выплатить {credit_sum}')
        return render_template(
            'pay_off_credit.html', options=options, form=form, my_cards=my_cards, my_credits=my_credits)
    else:
        return render_template(
            'info.html', options=options,
            message='Сначала необходимо зарегестрироваться')


# Вклыды

@app.route('/directions/contributions', methods=['GET', "POST"])
def contributions():
    return render_template('contributions.html', options=options)


# Оформление вклада

@app.route('/directions/contribution/order_contribution', methods=['GET', "POST"])
def order_contribution():
    if current_user.is_authenticated:
        form = OrderСontributionForm()
        db_sess = db_session.create_session()

        my_cards_ = [(card.name, card.sum_, card.card_number, card.secret_code) for card in
                     db_sess.query(Cards).filter(Cards.user_id == current_user.id).all()] + \
                    [(card.name, card.sum_, card.card_number, card.secret_code) for card in
                     db_sess.query(CreditCards).filter(CreditCards.user_id == current_user.id).all()] + \
                    [(card.name, card.sum_, card.card_number, card.secret_code) for card in
                     db_sess.query(PensionСards).filter(PensionСards.user_id == current_user.id).all()]

        form.transfer_card.choices = [(card_[0]) for card_ in my_cards_]

        if form.validate_on_submit():
            percent = request.args.get('percent')
            m = int(request.args.get('m'))

            form.transfer_card.choices = [(card_[0]) for card_ in my_cards_]

            c = len(db_sess.query(Credits).filter(Credits.user_id == current_user.id).all()) + 1

            if c > 2:
                return render_template(
                    'info.html', options=options, message="Нельзя оформить так много вкладов")

            if 5000 < int(form.sum_.data) < m:
                for card in my_cards_:
                    if card[0] == form.transfer_card.data:

                        if 'Дебютовая' in card[0]:
                            update_transfers('cards', card[2], form.sum_.data, '-')
                        elif 'Кредитная' in card[0]:
                            update_transfers('credits', card[2], form.sum_.data, '-')
                        else:
                            update_transfers('pension_cards', card[2], form.sum_.data, '-')

                        name = f"Вклад {c}"
                        contribution = Сontributions(
                            fio=form.fio.data,
                            name=name,
                            sum_=form.sum_.data,
                            tel=form.tel.data,
                            nomer=form.nomer.data,
                            vidan=form.vidan.data,
                            percent=int(percent),
                            transfer_card=form.transfer_card.data,
                            transfer_history='',
                            user_id=current_user.id)

                        db_sess.add(contribution)
                        db_sess.commit()
                        income_ = (int(form.sum_.data) * int(percent))/100
                        print(percent)
                        return card_ready(
                            name, datetime.date(datetime.now()), percent=percent, income_=str(income_))
            else:
                return render_template(
                    'order_contribution.html', title='Оформление вклада', form=form, options=options, cards_=my_cards_, message='Неверная сумма')
        return render_template(
            'order_contribution.html', title='Оформление вклада', form=form, options=options, cards_=my_cards_)
    else:
        return render_template('info.html', options=options, message='Сначала необходимо зарегестрироваться')


# Карты

@app.route('/directions/cards', methods=['GET', "POST"])
def cards():
    db_sess = db_session.create_session()
    return render_template('cards.html', options=options)


# Дебютовые карты
@app.route('/directions/cards/debut_cards', methods=['GET', "POST"])
def debut_cards():
    return render_template('debut_cards.html', options=options)


# Оформление карты
@app.route('/directions/cards/order_card', methods=['GET', "POST"])
def order_card():
    form = OrderCardForm()
    if current_user.is_authenticated:

        if form.validate_on_submit():
            service_price = int(request.args.get('service_price'))
            privileges = str(request.args.get('privileges'))

            card_number = rand(16)
            pin = rand(4)
            secret_code = rand(3)

            db_sess = db_session.create_session()

            c = len(db_sess.query(Cards).filter(Cards.user_id == current_user.id).all()) + 1
            card_name = f"Дебютовая карта {c}"

            card = Cards(
                fio=form.fio.data,
                name=card_name,
                sum_=0,
                tel=form.tel.data,
                nomer=form.nomer.data,
                vidan=form.vidan.data,
                pin=pin,
                secret_code=secret_code,
                service_price=service_price,
                card_number=card_number,
                privileges=privileges,
                transfer_history='',
                user_id=current_user.id
            )

            db_sess.add(card)
            db_sess.commit()
            d = str(datetime.date(datetime.now())).split('-')
            d = date(*list(map(int, [str((int(d[0]) + 3))] + d[1:])))
            return card_ready(
                    card_name, d, pin,
                    secret_code, card_number)
        return render_template(
            'order_card.html', title='Регистрация', form=form, options=options)
    else:
        return render_template(
            'info.html', options=options,
            message='Сначала необходимо зарегестрироваться')


# Пенсионные карты
@app.route('/directions/cards/pension_cards', methods=['GET', "POST"])
def pension_cards():
    return render_template('pension_cards.html', options=options)


# Оформление пенсионной карты
@app.route('/directions/cards/order_pension_card', methods=['GET', "POST"])
def order_pension_card():
    form = OrderCardForm()
    if current_user.is_authenticated:

        if form.validate_on_submit():
            a = str(form.vidan.data).split(".")
            a[0], a[2] = a[2], a[0]
            print(a)
            print(calculate_age(a))
            if int(calculate_age(a)) >= 60:
                service_price = int(request.args.get('service_price'))
                privileges = str(request.args.get('privileges'))
                print('3')

                card_number = rand(3)
                pin = rand(4)
                secret_code = rand(16)

                db_sess = db_session.create_session()

                c = len(db_sess.query(PensionСards).filter(PensionСards.user_id == current_user.id).all()) + 1
                card_name = f"Пенсионная карта {c}"

                card = Cards(
                    fio=form.fio.data,
                    name=card_name,
                    sum_=0,
                    tel=form.tel.data,
                    nomer=form.nomer.data,
                    vidan=form.vidan.data,
                    pin=pin,
                    secret_code=secret_code,
                    service_price=service_price,
                    card_number=card_number,
                    privileges=privileges,
                    transfer_history='',
                    user_id=current_user.id
                )

                db_sess.add(card)
                db_sess.commit()
                d = str(datetime.date(datetime.now())).split('-')
                d = date(*list(map(int, [str((int(d[0]) + 3))] + d[1:])))
                return card_ready(
                    card_name, d, pin,
                    secret_code, card_number)
            else:
                return render_template(
                    'info.html', options=options,
                    message='Неподнодящий возрост для пенсионной карты. Вы можете оформить дебютовую карту')

        return render_template(
            'order_pension_card.html', title='Оформление пенсионной карты', form=form, options=options)
    else:
        return render_template(
            'info.html', options=options,
            message='Сначала необходимо зарегестрироваться')


# Кредитные карты
@app.route('/directions/cards/credit_cards', methods=['GET', "POST"])
def credit_cards():
    return render_template('credit_cards.html', options=options)


@app.route('/directions/cards/order_credit_card', methods=['GET', "POST"])
def order_credit_card():
    form = OrderCreditCardForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():

            percent = int(request.args.get('percent'))
            nonpercent = int(request.args.get('nonpercent'))
            monthly_percent = int(request.args.get('monthly_percent'))
            sum_ = int(request.args.get('sum_'))
            if not (int(form.sum_.data) < 5000 or int(form.sum_.data) > sum_):
                term = int(request.args.get('term'))

                pin = rand(4)
                secret_code = rand(3)
                card_number = rand(16)
                db_sess = db_session.create_session()

                c = len(db_sess.query(CreditCards).filter(CreditCards.user_id == current_user.id).all()) + 1
                card_name = f"Кредитная карта {c}"
                print('d')
                credit_card = CreditCards(
                    fio=form.fio.data,
                    name=card_name,
                    sum_=int(form.sum_.data),
                    start_sum=int(form.sum_.data),
                    tel=form.tel.data,
                    nomer=form.nomer.data,
                    vidan=form.vidan.data,
                    place_of_work=form.place_of_work.data,
                    monthly_percent=monthly_percent,
                    nonpercent=nonpercent,
                    percent=percent,
                    term=term,
                    pin=pin,
                    secret_code=secret_code,
                    card_number=card_number,
                    transfer_history='',
                    user_id=current_user.id
                )
                print(123)

                db_sess.add(credit_card)
                db_sess.commit()
                d = str(datetime.date(datetime.now())).split('-')
                d = date(*list(map(int, [str((int(d[0]) + term))] + d[1:])))
                print(12)
                return card_ready(card_name, d, pin, secret_code, card_number, credit_sum=str(sum_))
            return render_template('order_credit_card.html', title='Оформление кредитной карты', form=form,
                                   options=options, message=f'Сумма кредита должна быть меньше {sum_} и больше 5000')
        print('d')
        return render_template('order_credit_card.html', title='Оформление кредитной карты', form=form, options=options)
    else:
        return render_template(
            'info.html', options=options,
            message='Сначала необходимо зарегестрироваться')


# Информация о банке
@app.route('/directions/information')
def information():
    db_sess = db_session.create_session()
    users = db_sess.query(Users).all()
    names = {name.id: (name.surname, name.name) for name in users}
    return render_template('information.html', options=options)


# Служба потдержки
@app.route('/directions/support', methods=['GET', "POST"])
def support():
    return render_template('support.html', options=options)


@app.route('/directions/support/support_question', methods=['GET', 'POST'])
def support_question():
    form = SupportForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        reviews = Reviews(
            name=form.name.data,
            mail=form.email.data,
            message=form.user_message.data,
        )
        db_sess.add(reviews)
        db_sess.commit()

        if sent_mail(form.email.data, form.user_message.data) == 'Spam ERROR':
            return render_template('support_question.html', options=options, form=form,
                                   message="Мы рассмотрим выше обращение. (неверная почта или отключен спам)")
        return render_template(
            'support_question.html', options=options, form=form, message="Ваше обращение отправлено")

    return render_template(
        'support_question.html', options=options, form=form)


# Другие направления
@app.route('/directions/other_services')
def other_services():
    db_sess = db_session.create_session()
    users = db_sess.query(Users).all()
    names = {name.id: (name.surname, name.name) for name in users}
    return render_template('other_services.html', options=options)


# Авторизация
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', options=options,
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form, options=options)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register', form=form,
                                   message="Пароли не совпадают", options=options)
        db_sess = db_session.create_session()
        if db_sess.query(Users).filter(Users.email == form.email.data).first():
            return render_template('register.html', title='Register', form=form,
                                   message="Эта почта уже используется", options=options)
        user = Users(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            email=form.email.data,
            address=form.address.data,
            admin=0
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, options=options)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = AdminForm()
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        is_admin = db_sess.query(Users).filter(Users.id == current_user.id and Users.admin).all()
        print(is_admin)
        if is_admin:
            users = [((user.id, user.name, user.surname, user.address, user.email, user.admin), my_cards(user.id)) for user in db_sess.query(Users).all()]
            print(users)
            if form.check_credits_and_contributions.data:
                set_all()
                return render_template('admin.html', form=form, options=options, users=users, message='Все обновлено')

            return render_template('admin.html', form=form, options=options, users=users)
    else:
        return render_template('info.html', options=options, message='Сначала необходимо зарегестрироваться')


@app.route('/admin/rew')
def admin_rew():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        is_admin = db_sess.query(Users).filter(Users.id == current_user.id and Users.admin).all()

        if is_admin:
            rews = [(i.name, i.mail, i.message) for i in db_sess.query(Reviews).all()]
            print(rews)
            return render_template('rew.html', options=options, rews=rews)
    else:
        return render_template('info.html', options=options, message='Сначала необходимо зарегестрироваться')


@app.route('/conttrebend/<name>')
def conttrebend(name):

    if current_user.is_authenticated:

        db_sess = db_session.create_session()
        con = sqlite3.connect('db/users_db.sqlite')
        print(name)

        cur = con.cursor()
        s, f = cur.execute(f"SELECT sum_, transfer_card FROM contributions WHERE name = '{name}' AND user_id = '{current_user.id}'").fetchall()[0]
        s = int(s)
        if 'Дебютовая' in f:
            g, t = cur.execute(f"SELECT sum_, transfer_history FROM cards WHERE name = '{f}' AND user_id = '{current_user.id}'").fetchall()[0]
        elif 'Пенсионная' in f:
            g, t = cur.execute(f"SELECT sum_, transfer_history FROM pension_cards WHERE name = '{f}' AND user_id = '{current_user.id}'").fetchall()[0]
        else:
            g, t = cur.execute(f"SELECT sum_, transfer_history FROM credit_cards WHERE name = '{f}' AND user_id = '{current_user.id}'").fetchall()[0]
        cur.execute(f"DELETE FROM contributions WHERE name = '{name}' AND user_id = '{current_user.id}'").fetchall()
        print(s, f)
        print(g)
        g = int(g)

        transfer_history = str(t).split(';')
        if len(transfer_history) >= 7:
            transfer_history = transfer_history[1:] + [
                f"{str(datetime.now()).split('.')[0]}|{int(s)}|+"]
        else:
            transfer_history = transfer_history[:] + [
                f"{str(datetime.now()).split('.')[0]}|{int(s)}|+"]

        con.commit()
        con.close()
        con = sqlite3.connect('db/users_db.sqlite')

        cur = con.cursor()
        if 'Дебютовая' in f:
            cur.execute(f"UPDATE cards SET sum_ = {s + g}, transfer_history = '{';'.join(transfer_history)}' WHERE user_id = '{current_user.id}' AND name = '{f}'")
        elif 'Пенсионная' in f:
            cur.execute(f"UPDATE pension_cards SET sum_ = {s + g}, transfer_history = '{';'.join(transfer_history)}' WHERE user_id = '{current_user.id}' AND name = '{f}'")
        else:
            cur.execute(f"UPDATE credit_cards SET sum_ = {s + g}, transfer_history = '{';'.join(transfer_history)}' WHERE user_id = '{current_user.id}' AND name = '{f}'")
        con.commit()
        con.close()

        users = [((user.id, user.name, user.surname, user.address, user.email, user.admin), my_cards(user.id)) for
                    user in db_sess.query(Users).all()]
        print(users)

        return render_template('info.html', options=options, message='Вклад закрыт')
    else:
        return render_template('info.html', options=options, message='Сначала необходимо зарегестрироваться')


@app.route('/admin/block/<int:user_id>/<type_>/<card_name>/<block>')
def admin_block_user(user_id, type_, card_name, block):
    print(block)
    block = eval(block)
    print(block)
    if current_user.is_authenticated:

        db_sess = db_session.create_session()

        print(user_id, card_name, type_, block)
        is_admin = db_sess.query(Cards).filter(Users.id == user_id and Users.admin).all()

        if is_admin:

            users = [((user.id, user.name, user.surname, user.address, user.email, user.admin), my_cards(user.id)) for
                     user in db_sess.query(Users).all()]
            con = sqlite3.connect('db/users_db.sqlite')
            print(users)

            cur = con.cursor()
            # Получили результат запроса, который ввели в текстовое поле

            cur.execute(f"UPDATE {type_} SET block = {block} WHERE user_id = {user_id} AND name = {card_name}")
            con.commit()
            con.close()
            users = [((user.id, user.name, user.surname, user.address, user.email, user.admin), my_cards(user.id)) for
                     user in db_sess.query(Users).all()]
            print(users)
            if block:
                return render_template('info.html', options=options, message='Карта заблокирована')
            return render_template('info.html', options=options, message='Карта разблокирована')
    else:
        return render_template('info.html', options=options, message='Сначала необходимо зарегестрироваться')


# Обновляем данные по кредитам
def await_credit():
    if str(datetime.date(datetime.now())).split('-')[-1] == '25':
        for i in read_sqlfile("db/users_db.sqlite", 'credit_cards', '*'):
            set_credit_cards_sum(i[0], i[-2], i[11], int(i[3]), int(i[2]), i[9], i[-6])
        for i in read_sqlfile("db/users_db.sqlite", 'credit', '*'):
            set_credit_sum(i[0], i[-2], i[11], int(i[3]), int(i[2]), i[9], i[-6])


def main():
    db_session.global_init("db/users_db.sqlite")
    int(str(datetime.date(datetime.now())).split("-")[2])

    app.run()


if __name__ == '__main__':
    main()
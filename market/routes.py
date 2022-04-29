from market import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, purchasedForm, sellForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/index')
def indexPage():
    return render_template('index.html')

@app.route('/table', methods=["GET","POST"])
@login_required
def tablePage():
    purchased_form = purchasedForm()
    sell_form=sellForm()
    if request.method == 'POST':
        #purchase item logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congrates! for { p_item_object.name } of { p_item_object.price }$", category="success")
            else:
                flash(f"Not enough money for { p_item_object.name }", category="danger")
        #sell item logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congrates! You sold { s_item_object } with {s_item_object}$ price.", category="success")
            else:
                flash(f"Selling went wrong for { s_item_object }", category="danger")
        return redirect(url_for("tablePage"))
    if request.method == "GET":
        owned_item=Item.query.filter_by(owner=current_user.id)
        items = Item.query.filter_by(owner=None)
        return render_template('table.html', items=items, purchased_form=purchased_form, owned_item=owned_item, sell_form=sell_form)

@app.route('/price')
def pricePage():
    return render_template('price.html')

@app.route('/register', methods=['GET', 'POST'])
def registerPage():
    form=RegisterForm()
    if form.validate_on_submit():
        user_to_create=User(username=form.username.data,
                            emailAddress=form.email_address.data,
                            password=form.password1.data
                            )
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('tablePage'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There is an error: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def loginPage():
    form=LoginForm()
    if form.validate_on_submit():
        attempted_user=User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Well Done: {attempted_user.username}', category='success')
            return redirect(url_for('tablePage'))
        else:
            flash('Wrong info! try again', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logoutPage():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for('indexPage'))
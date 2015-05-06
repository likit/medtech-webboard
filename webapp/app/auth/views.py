from flask import render_template, request, url_for, flash, redirect
from flask.ext.login import login_user
from ..models import Customer
from .forms import LoginForm
from . import auth

@auth.route('/login')
def login():
    return render_template('auth/login.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(email=form.email.data).first()
        if customer is not None and customer.verify_password(form.password.data):
            login_user(customer, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid email or password')
    return render_template('auth/login.html', form=form)

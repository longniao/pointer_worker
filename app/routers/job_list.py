# -*- coding: utf-8 -*-

from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from app.models.account import User
from . import job_blueprint


@job_blueprint.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user is not None and user.password_hash is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash(_('You are now logged in. Welcome back!'), 'success')
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash(_('Invalid email or password.'), 'form-error')
    return render_template('auth/login.html', form=form)

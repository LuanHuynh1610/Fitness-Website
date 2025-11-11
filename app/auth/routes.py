from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.auth import bp
from app import db
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm










@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        # Redirect theo role
        if user.role == "admin":
            return redirect(url_for('admin.dashboard'))
        elif user.role == "trainer":
            return redirect(url_for('trainer.dashboard'))  
        else:
            return redirect(url_for('main.dashboard')) 
    return render_template('auth/login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # kiểm tra username/email bằng form validator đã chạy
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    # nếu GET hoặc form lỗi, render lại form với lỗi hiển thị
    return render_template('auth/register.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))




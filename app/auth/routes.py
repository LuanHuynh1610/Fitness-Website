from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.auth import bp
from app import db
from app.models import User

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # ví dụ kiểm tra đơn giản (sau này thay bằng DB)
        if username == 'admin' and password == '123':
            return redirect(url_for('main.index'))
        else:
            return render_template('login.html', message="Sai tài khoản hoặc mật khẩu!")

    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Kiểm tra cơ bản
        if password != confirm_password:
            flash('Mật khẩu không khớp!')
            return redirect(url_for('auth.register'))

        # (Sau này sẽ thêm lưu vào database)
        flash(f'Đăng ký thành công cho người dùng: {username}')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

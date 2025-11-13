from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.main import bp

@bp.route('/')
def index():
    return render_template('main/index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('main/dashboard.html')

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    message = None  # dùng để hiển thị thông báo tùy loại
    message_type = None

    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_username = request.form.get('username')
        new_email = request.form.get('email')
        new_password = request.form.get('new_password')

        # Kiểm tra mật khẩu hiện tại
        if not check_password_hash(current_user.password_hash, current_password):
            message = "❌ Mật khẩu hiện tại không đúng!"
            message_type = "error"
        else:
            # Cập nhật thông tin
            if new_username:
                current_user.username = new_username
            if new_email:
                current_user.email = new_email
            if new_password:
                current_user.password_hash = generate_password_hash(new_password)

            db.session.commit()
            message = "Thông tin của bạn đã được cập nhật thành công!"
            message_type = "success"

    return render_template('main/profile.html', user=current_user, message=message, message_type=message_type)














from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Class, User
from datetime import datetime
from app.trainer import bp

# Yêu cầu đăng nhập và đúng role
def trainer_required(func):
    from functools import wraps
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'trainer':
            flash("Bạn không có quyền truy cập trang này.")
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    return decorated_function


@bp.route('/dashboard_trainer')
@login_required
@trainer_required
def dashboard():
    return render_template('trainer/dashboard.html')


@bp.route('/manage_classes')
@login_required
@trainer_required
def manage_classes():
    classes = Class.query.filter_by(trainer_name=current_user.username).all()
    return render_template('trainer/manage_my_classes.html', classes=classes)


@bp.route('/edit_class/<int:id>', methods=['GET', 'POST'])
@login_required
@trainer_required
def edit_class(id):
    cls = Class.query.get_or_404(id)
    if cls.trainer_name != current_user.username:
        flash("Bạn không thể chỉnh sửa lớp của trainer khác.")
        return redirect(url_for('trainer.manage_classes'))

    if request.method == 'POST':
        cls.name = request.form['name']
        cls.description = request.form['description']
        cls.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        cls.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        db.session.commit()
        flash('Cập nhật lớp thành công!')
        return redirect(url_for('trainer.manage_classes'))
    return render_template('trainer/edit_my_class.html', cls=cls)
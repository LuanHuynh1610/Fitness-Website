from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.admin import bp
from app.admin.forms import CreateAdminForm
from app.models import User
from app import db

# decorator kiểm tra quyền admin
def admin_required(func):
    def wrapper(*args, **kwargs):
        if current_user.role != "admin":
            flash("Bạn không có quyền truy cập.")
            return redirect(url_for("main.index"))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


# ✅ Trang quản lý admin
@bp.route('/manage_admin')
@login_required
@admin_required
def manage_admin():
    admins = User.query.filter_by(role="admin").all()
    return render_template('admin/manage_admin.html', admins=admins)


# ✅ Thêm admin mới
@bp.route('/add_admin', methods=['GET', 'POST'])
@login_required
@admin_required
def add_admin():
    form = CreateAdminForm()
    if form.validate_on_submit():
        new_admin = User(
            username=form.username.data,
            email=form.email.data,
            role="admin"
        )
        new_admin.set_password(form.password.data)

        db.session.add(new_admin)
        db.session.commit()
        return redirect(url_for('admin.manage_admin'))

    return render_template('admin/add_admin.html', form=form)


# ✅ Xóa admin
@bp.route('/delete_admin/<int:admin_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_admin(admin_id):
    admin = User.query.get_or_404(admin_id)

    if request.method == "POST":
        db.session.delete(admin)
        db.session.commit()
        flash("Xóa admin thành công!")
        return redirect(url_for('admin.manage_admin'))

    return render_template('admin/delete_admin.html', admin=admin)

@bp.route('/')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')



@bp.route('/manage_classes')
@login_required
def manage_classes():
    return render_template('admin/manage_classes.html')

@bp.route('/manage_trainers')
@login_required
def manage_trainers():
    return render_template('admin/manage_trainers.html')

@bp.route('/manage_users')
@login_required
def manage_users():
    return render_template('admin/manage_users.html')


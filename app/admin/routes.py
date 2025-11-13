from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.admin import bp
from app.admin.forms import CreateAdminForm, CreateTrainerForm
from app.models import User
from app import db
from app.models import Class
from datetime import datetime

# decorator kiểm tra quyền admin
def admin_required(func):
    def wrapper(*args, **kwargs):
        if current_user.role != "admin":
            flash("Bạn không có quyền truy cập.")
            return redirect(url_for("main.index"))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


# Trang quản lý admin
@bp.route('/manage_admin')
@login_required
@admin_required
def manage_admin():
    admins = User.query.filter_by(role="admin").all()
    return render_template('admin/manage_admin.html', admins=admins)


#Thêm admin mới
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


# Xóa admin
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
    classes = Class.query.all()
    return render_template('admin/manage_classes.html', classes=classes)

# --- Thêm lớp học ---
@bp.route('/add_class', methods=['GET', 'POST'])
@login_required
def add_class():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        trainer_name = request.form.get('trainer_name')
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')

        if not name:
            flash('Tên lớp không được để trống!')
            return redirect(url_for('admin.add_class'))
        
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else None
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None
        new_class = Class(
            name=name,
            description=description,
            trainer_name=trainer_name,
            start_date=start_date ,
            end_date=end_date
        )
        db.session.add(new_class)
        db.session.commit()
        flash('Đã thêm lớp học mới thành công!')
        return redirect(url_for('admin.manage_classes'))

    return render_template('admin/add_class.html')

# --- Xóa lớp học ---
@bp.route('/delete_class/<int:class_id>', methods=['GET', 'POST'])
@login_required
def delete_class(class_id):
    class_to_delete = Class.query.get_or_404(class_id)
    if request.method == 'POST':
        db.session.delete(class_to_delete)
        db.session.commit()
        flash('Đã xóa lớp học thành công!')
        return redirect(url_for('admin.manage_classes'))

    return render_template('admin/delete_class.html', class_to_delete=class_to_delete)

@bp.route('/edit_class/<int:class_id>', methods=['GET', 'POST'])
@login_required
def edit_class(class_id):
    class_item = Class.query.get_or_404(class_id)

    if request.method == 'POST':
        class_item.name = request.form['name']
        class_item.description = request.form['description']
        class_item.trainer_name = request.form['trainer_name']

        # Lấy và chuyển đổi ngày
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')

        try:
            if start_date_str:
                class_item.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            if end_date_str:
                class_item.end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Ngày nhập không hợp lệ. Vui lòng nhập đúng định dạng YYYY-MM-DD.", "danger")
            return redirect(url_for('edit_class', class_id=class_id))

        # Kiểm tra logic ngày (nếu có)
        if class_item.start_date and class_item.end_date and class_item.start_date > class_item.end_date:
            flash("Ngày bắt đầu không được sau ngày kết thúc.", "warning")
            return redirect(url_for('edit_class', class_id=class_id))

        db.session.commit()
        flash('Cập nhật lớp học thành công!', 'success')
        return redirect(url_for('admin.manage_classes'))

    return render_template('admin/edit_class.html', class_item=class_item)


@bp.route('/manage_trainers')
@login_required
@admin_required
def manage_trainers():
    trainers = User.query.filter_by(role="trainer").all()
    return render_template('admin/manage_trainers.html', trainers=trainers)


#Thêm trainer mới
@bp.route('/add_trainer', methods=['GET', 'POST'])
@login_required
@admin_required
def add_trainer():
    trainer_form = CreateTrainerForm()
    
    if trainer_form.validate_on_submit():
        # Debug: xem dữ liệu form
        print("Form data:", {
            "username": trainer_form.username.data,
            "email": trainer_form.email.data,
            "password": trainer_form.password.data
        })
        
        # Kiểm tra username/email tồn tại
        existing_user = User.query.filter(
            (User.username == trainer_form.username.data) | 
            (User.email == trainer_form.email.data)
        ).first()
        if existing_user:
            flash("Username hoặc email đã tồn tại!")
            print("Existing user found:", existing_user.username, existing_user.email)
            return redirect(url_for('admin.add_trainer'))

        # Tạo trainer mới
        new_trainer = User(
            username=trainer_form.username.data,
            email=trainer_form.email.data,
            role="trainer"
        )
        new_trainer.set_password(trainer_form.password.data)

        try:
            db.session.add(new_trainer)
            db.session.commit()
            flash("Trainer đã được thêm thành công!")
            print("Trainer added:", new_trainer.username)
            return redirect(url_for('admin.manage_trainers'))
        except Exception as e:
            db.session.rollback()
            flash("Có lỗi xảy ra khi thêm trainer!")
            print("Database error:", e)

    else:
        if request.method == "POST":
            # Debug: nếu POST mà form không validate
            print("Form errors:", trainer_form.errors)
    
    return render_template('admin/add_trainer.html', trainer_form=trainer_form)

@bp.route('/delete_trainer/<int:trainer_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_trainer(trainer_id):
    trainer = User.query.get_or_404(trainer_id)

    if request.method == "POST":
        db.session.delete(trainer)
        db.session.commit()
        flash("Xóa trainer thành công!")
        return redirect(url_for('admin.manage_trainers'))

    return render_template('admin/delete_trainer.html', trainer=trainer)


@bp.route('/manage_users')
@login_required
def manage_users():
    return render_template('admin/manage_users.html')


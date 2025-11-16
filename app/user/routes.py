from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Class, UserClass
from app.user import bp
from app.models import Notification

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('user/dashboard.html')

# Trang hiển thị tất cả lớp học
@bp.route('/regist_class')
@login_required
def regist_class():
    classes = Class.query.all()
    return render_template('user/regist_class.html', classes=classes)

# Xử lý đăng ký lớp
@bp.route('/register_class/<int:class_id>')
@login_required
def register_class(class_id):
    # --- kiểm tra số lượng slot ---
    current_count = UserClass.query.filter_by(class_id=class_id).count()
    if current_count >= 10:
        flash("Lớp đã đầy (Full slot).")
        return redirect(url_for('user.regist_class'))

    # --- giữ nguyên logic cũ ---
    existing = UserClass.query.filter_by(user_id=current_user.id, class_id=class_id).first()
    if existing:
        flash("Bạn đã đăng ký lớp này rồi.")
    else:
        new_reg = UserClass(user_id=current_user.id, class_id=class_id)
        db.session.add(new_reg)
        # Gửi thông báo đến admin
        notify = Notification(
            message=f"User {current_user.username} đã đăng ký lớp có ID {class_id}"
        )
        db.session.add(notify)
        db.session.commit()
        flash("Đăng ký thành công!")

    return redirect(url_for('user.regist_class'))

# Trang hiển thị lớp học đã đăng ký
@bp.route('/user_class')
@login_required
def user_class():
    registered = (
        db.session.query(Class)
        .join(UserClass)
        .filter(UserClass.user_id == current_user.id)
        .all()
    )

    # thêm số lượng học viên mỗi lớp
    class_data = []
    for c in registered:
        count = UserClass.query.filter_by(class_id=c.id).count()
        class_data.append({
            "class": c,
            "count": count
        })

    return render_template('user/user_class.html', classes=class_data)



@bp.route('/cancel_class/<int:class_id>', methods=['POST'])
@login_required
def cancel_class(class_id):

    # Tìm bản ghi đăng ký lớp
    user_class = UserClass.query.filter_by(
        user_id=current_user.id,
        class_id=class_id
    ).first()

    if not user_class:
        flash("Bạn chưa đăng ký lớp này!")
        return redirect(url_for('user.user_classes'))

    # Xóa đăng ký
    db.session.delete(user_class)

    # Gửi thông báo đến admin
    notify = Notification(
        message=f"User {current_user.username} đã hủy lớp có ID {class_id}"
    )
    db.session.add(notify)

    db.session.commit()

    flash("Hủy lớp thành công!")
    return redirect(url_for('user.user_class'))













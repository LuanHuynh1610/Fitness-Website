from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Class, User, CheckInLog
from datetime import datetime, timedelta
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


@bp.route('/my_classes')
@login_required
def my_classes():
    if current_user.role != "trainer":
        flash("Bạn không có quyền truy cập.", "danger")
        return redirect(url_for('main.dashboard'))

    # Lấy các lớp mà trainer này phụ trách
    classes = Class.query.filter_by(trainer_name=current_user.username).all()

    return render_template('trainer/my_classes.html', classes=classes)


@bp.route('/edit_class/<int:id>', methods=['GET', 'POST'])
@login_required
@trainer_required
def edit_class(id):
    cls = Class.query.get_or_404(id)
    if cls.trainer_name != current_user.username:
        flash("Bạn không thể chỉnh sửa lớp của trainer khác.")
        return redirect(url_for('trainer.my_classes'))

    if request.method == 'POST':
        cls.name = request.form['name']
        cls.description = request.form['description']
        cls.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        cls.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        db.session.commit()
        flash('Cập nhật lớp thành công!')
        return redirect(url_for('trainer.my_classes'))
    return render_template('trainer/edit_my_class.html', cls=cls)


@bp.route("/check_qr", methods=["POST"])
def check_qr():
    data = request.json.get("qr", "")
    
    try:
        tag, trainer_id, secret = data.split(":")
    except:
        return jsonify({"message": "QR không hợp lệ!"})

    if tag != "checkin":
        return jsonify({"message": "Sai định dạng QR!"})

    trainer = User.query.get(trainer_id)
    if not trainer or trainer.qr_secret != secret:
        return jsonify({"message": "QR không thuộc về trainer này!"})

    now = datetime.utcnow()
    last_log = CheckInLog.query.filter_by(trainer_id=trainer.id).order_by(CheckInLog.id.desc()).first()

    if not last_log or now - last_log.timestamp > timedelta(seconds=30):
        log = CheckInLog(trainer_id=trainer.id, status="checkin")
    else:
        log = CheckInLog(trainer_id=trainer.id, status="checkout")

    db.session.add(log)
    db.session.commit()

    msg = "✔ Check-in thành công!" if log.status == "checkin" else "✔ Check-out thành công!"
    return jsonify({"message": msg})



@bp.route("/scan_qr")
def scan_qr():
    return render_template("trainer/scan_qr.html")







from flask import Blueprint

bp = Blueprint('admin', __name__)

from app.admin import routes  # import các route sau khi tạo blueprint
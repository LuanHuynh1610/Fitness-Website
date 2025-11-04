from flask import Blueprint

bp = Blueprint('trainer', __name__)

from app.trainer import routes  # import các route sau khi tạo blueprint
from flask import Blueprint

bp = Blueprint('auth', __name__, template_folder='templates')

from app.auth import routes  # import các route sau khi tạo blueprint
from flask import Blueprint

bp = Blueprint('main', __name__, template_folder='templates')

from app.main import routes  # import các route sau khi tạo blueprint
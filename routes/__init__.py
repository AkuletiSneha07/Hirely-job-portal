
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
jobs_bp = Blueprint('jobs', __name__)
admin_bp = Blueprint('admin', __name__)

from . import auth, jobs, admin
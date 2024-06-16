from functools import wraps
import time
import jwt
from flask import request, abort
from flask import current_app
from organization.models import User
from app import db, app
from organization.utils import generate_token
from tests.mock_user import mock_user

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            if app.config["TESTING"] == True:
                return f(mock_user(), *args, **kwargs)
            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]
            if not token:
                return {
                    "message": "Authentication Token is missing!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401
            data=jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user=(
                db.session.query(User)
                .filter(User.id == data['user_id'],User.role ==  data['role'])
                .first()
            )
            if current_user is None or not current_user.role.value or current_user.role.value == 'user':
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 401

        return f(current_user, *args, **kwargs)

    return decorated
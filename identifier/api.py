from flask import Blueprint, request, abort, jsonify, Flask
from sqlalchemy.exc import NoResultFound

from .models import LockerEntry, SandboxToken, User

api = Blueprint('api', __name__)


@api.route('/token_info', methods=['POST'])
def user_info():
    token = request.values.get('token')
    if not token:
        abort(400)

    try:
        entry = LockerEntry.query.filter_by(user_token=token).one()
        user_id = entry.user_id
    except NoResultFound:
        try:
            entry = SandboxToken.query.filter_by(token=token).one()
            user_id = entry.user_id
        except NoResultFound:
            abort(404)
            return  # because PyCharm can't tell abort() never returns

    try:
        user = User.query.filter_by(id=user_id).one()
    except NoResultFound:
        abort(500)
        return  # because PyCharm can't tell abort() never returns

    return jsonify({
        'user_id': user_id,
        'has_subscription': user.has_active_sub
    })


def init_app(app: Flask, url_prefix='/api/v1'):
    app.register_blueprint(api, url_prefix=url_prefix)

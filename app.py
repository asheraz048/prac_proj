from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from blackList import BLACKLIST
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.student import Student, StudentList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] =['access', 'refresh']
app.secret_key = 'jose'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager (app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity ==1:
        return {"is_admin":True}
    return {"is_admin":False}

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify ({
        "Description":"The token has expired",
        'Error':'token_expired'

    }),401

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.invalid_token_loader
def invalid_token_callback():
    return jsonify ({
        'Description':'Signature verification failed',
        'Error':'invalid_token'
    }
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401


api.add_resource(Student, '/student/<string:name>')
api.add_resource(StudentList, '/students')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)

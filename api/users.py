from flask import Blueprint, jsonify, request, make_response
from data import __db_session as db_session
from data.users import User
from sqlalchemy.orm import Session
from ._utils import check_exists

blueprint = Blueprint('users_api', __name__, template_folder='templates')


@blueprint.route('/api/users', methods=['GET'])
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify({'users': [
        {
            'id': user.id,
            'name': user.name,
            'surname': user.surname,
            'email': user.email,
            'age': user.age,
            'position': user.position,
            'speciality': user.speciality,
            'address': user.address
        } for user in users
    ]})


@blueprint.route('/api/users/<int:_id>', methods=['GET'])
@check_exists(User)
def get_user(user: User):
    return jsonify({'user': {
        'id': user.id,
        'name': user.name,
        'surname': user.surname,
        'email': user.email,
        'age': user.age,
        'position': user.position,
        'speciality': user.speciality,
        'address': user.address
    }})


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)

    required = ['name', 'surname', 'email']
    if not all(key in request.json for key in required):
        return make_response(jsonify({'error': 'Missing fields'}), 400)

    try:
        user = User(
            name=request.json['name'],
            surname=request.json['surname'],
            email=request.json['email'],
            age=request.json.get('age'),
            position=request.json.get('position'),
            speciality=request.json.get('speciality'),
            address=request.json.get('address')
        )
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
        return jsonify({'id': user.id})
    except Exception as e:
        print(e)
        return make_response(jsonify({'error': 'Bad request'}), 400)


@blueprint.route('/api/users/<int:_id>', methods=['PUT'])
@check_exists(User)
def edit_user(user: User):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)

    try:
        data = request.json
        for key in ['name', 'surname', 'email', 'age', 'position', 'speciality', 'address']:
            if key in data:
                setattr(user, key, data[key])
        db_sess = Session.object_session(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})
    except Exception as e:
        print(e)
        return make_response(jsonify({'error': 'Bad request'}), 400)


@blueprint.route('/api/users/<int:_id>', methods=['DELETE'])
@check_exists(User)
def delete_user(user: User):
    db_sess = Session.object_session(user)
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})

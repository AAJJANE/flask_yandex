import datetime

from flask import Blueprint, jsonify, request, make_response

from data import __db_session as db_session
from data.jobs import Jobs
from data.users import User
from sqlalchemy.orm import Session

from ._utils import check_exists

blueprint = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)

"""не знаю, права ли я на самом деле, но я считаю что на уроке добавление работы
   не работало из-за того, что work_size почему-то был во вне основного блока в json.
   Для надёжности, я решила заполнить словарь в ручную, и всё заработало :)"""


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    result = []

    for job in jobs:
        result.append({
            'job_info': {
                'job': job.job,
                'work_size': job.work_size,
                'start_date': job.start_date.isoformat(),
                'end_date': job.end_date.isoformat() if job.end_date else None,
            },
            'is_finished': job.is_finished,
            'team_leader': {
                'id': job.team_leader_obj.id,
                'name': job.team_leader_obj.name,
                'surname': job.team_leader_obj.surname
            },
            'collaborators': [user.id for user in job.collaborators_objs]
        })

    return jsonify({'jobs': result})


@blueprint.route('/api/jobs/<int:_id>', methods=['GET'])
@check_exists(Jobs)
def get_one_job(job: Jobs):
    return jsonify({
        'jobs': {
            'job_info': {
                'job': job.job,
                'work_size': job.work_size,
                'start_date': job.start_date.isoformat(),
                'end_date': job.end_date.isoformat() if job.end_date else None,
            },
            'is_finished': job.is_finished,
            'team_leader': {
                'id': job.team_leader_obj.id,
                'name': job.team_leader_obj.name,
                'surname': job.team_leader_obj.surname
            },
            'collaborators': [user.id for user in job.collaborators_objs]
        }
    })


@blueprint.route('/api/jobs/<int:_id>', methods=['DELETE'])
@check_exists(Jobs)
def delete_job(job: Jobs):
    db_sess = Session.object_session(job)
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json
                 for key in ['job', 'team_leader_id', 'work_size', 'start_date']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    try:
        db_sess = db_session.create_session()
        team_leader_id = request.json['team_leader_id']
        assert db_sess.get(User, team_leader_id)
        end_date = None
        if 'end_date' in request.json:
            end_date = datetime.datetime.fromisoformat(request.json['end_date']).date()
        collaborators = ''
        if 'collaborators' in request.json:
            collaborators = ', '.join(map(str, request.json['collaborators']))
        print(request.json.get('is_finished', 'True'))
        job = Jobs(
            team_leader=team_leader_id,
            job=request.json['job'],
            work_size=request.json['work_size'],
            start_date=datetime.datetime.fromisoformat(request.json['start_date']).date(),
            end_date=end_date,
            collaborators=collaborators,
            is_finished=1 if request.json.get('is_finished', 'True') else 0
        )
        db_sess.add(job)
        db_sess.flush()
        job_id = job.id
        db_sess.commit()
        return jsonify({'id': job_id})
    except Exception as e:
        print(e)
        return make_response(jsonify({'error': 'Bad request'}), 400)

@blueprint.route('/api/jobs/<int:_id>', methods=['PUT'])
@check_exists(Jobs)
def edit_job(job: Jobs):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)

    db_sess = Session.object_session(job)
    data = request.json

    try:
        if 'team_leader_id' in data:
            if not db_sess.get(User, data['team_leader_id']):
                return make_response(jsonify({'error': 'Invalid team_leader_id'}), 400)
            job.team_leader = data['team_leader_id']
        if 'job' in data:
            job.job = data['job']
        if 'work_size' in data:
            job.work_size = data['work_size']
        if 'start_date' in data:
            job.start_date = datetime.datetime.fromisoformat(data['start_date']).date()
        if 'end_date' in data:
            job.end_date = datetime.datetime.fromisoformat(data['end_date']).date()
        if 'is_finished' in data:
            job.is_finished = 1 if data['is_finished'] else 0
        if 'collaborators' in data:
            job.collaborators = ', '.join(map(str, data['collaborators']))

        db_sess.commit()
        return jsonify({'success': 'OK'})
    except Exception as e:
        print(e)
        return make_response(jsonify({'error': 'Bad request'}), 400)


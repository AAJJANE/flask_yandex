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

JOB_ATTRS = (
    'id', 'job', 'work_size', 'start_date', 'end_date', 'is_finished',
    'team_leader_obj.id', 'team_leader_obj.name', 'team_leader_obj.surname',
    'team_leader_obj.age', 'team_leader_obj.position', 'team_leader_obj.speciality',
    'team_leader_obj.address', 'team_leader_obj.email', 'team_leader_obj.modified_date',
    'collaborators_objs.id'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify({
        'jobs': [job.to_dict(only=JOB_ATTRS) for job in jobs]
    })


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

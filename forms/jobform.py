from typing import Type

from wtforms import SubmitField
from wtforms.form import Form
from wtforms.validators import DataRequired, NumberRange
from wtforms_sqlalchemy.orm import model_form

from sqlalchemy.orm import Session

from data import jobs, __db_session

FIELD_ARGS = {
    'team_leader_obj': {
        'label': "Team leader",
        'validators': [DataRequired()],
    },
    'collaborators_objs': {
        'label': 'Collaborators'
    },
    'job': {
        'validators': [DataRequired()],
    },
    'work_size': {
        'validators': [DataRequired(), NumberRange(min=0)],
    },
    'start_date': {
        'validators': [DataRequired()],
    },
}


def JobFormFactory(session: Session | None = None) -> Type[Form]:
    session = session or __db_session.create_session()

    class JobForm(model_form(jobs.Jobs, session, field_args=FIELD_ARGS)):
        submit = SubmitField('Done')

    return JobForm

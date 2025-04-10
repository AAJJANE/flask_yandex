from typing import Type

from wtforms import SubmitField
from wtforms.form import Form
from wtforms.validators import DataRequired, NumberRange
from wtforms_sqlalchemy.orm import model_form

from sqlalchemy.orm import Session

from data import departments, __db_session

FIELD_ARGS = {
    'team_leader_obj': {
        'label': "Team leader",
        'validators': [DataRequired()],
    },
    'members_objs': {
        'label': 'Members'
    },
    'email': {
        'validators': [DataRequired()],
    }
}


def DepartmentFormFactory(session: Session | None = None) -> Type[Form]:
    session = session or __db_session.create_session()

    class DepartmentForm(model_form(departments.Department, session, field_args=FIELD_ARGS)):
        submit = SubmitField('Done')

    return DepartmentForm

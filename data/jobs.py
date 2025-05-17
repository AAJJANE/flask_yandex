import sys

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .__db_session import SqlAlchemyBase, create_session


class Jobs(SqlAlchemyBase, SerializerMixin):
    from .users import User

    __tablename__ = 'jobs'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    team_leader = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=True)
    job = sa.Column(sa.String, nullable=True)
    work_size = sa.Column(sa.Integer, nullable=True)
    start_date = sa.Column(sa.Date, nullable=True)
    end_date = sa.Column(sa.Date, nullable=True)
    is_finished = sa.Column(sa.Boolean, nullable=True, default=False)
    price = sa.Column(sa.DECIMAL(2), nullable=True)

    team_leader_obj = orm.relationship(User,
                                       backref="jobs_team_leader")
    collaborators_objs = orm.relationship("User",
                                          secondary="jobs_user",
                                          backref="jobs_collaborator")

    @property
    def collaborators(self) -> str:
        return ', '.join(str(user.id) for user in self.collaborators_objs)

    @collaborators.setter
    def collaborators(self, collaborators: str) -> None:
        from .users import User

        db_sess = orm.object_session(self) or create_session()
        try:
            new_collaborators_objs = [
                db_sess.get(User, _id)
                for _id in map(int, collaborators.split(', '))
            ]
            self.collaborators_objs.clear()
            self.collaborators_objs = new_collaborators_objs
        except Exception as e:
            print('Error:', e, file=sys.stderr)
            db_sess.rollback()

    def __str__(self) -> str:
        return f'<job {self.id}: {self.job}>'

    def __repr__(self) -> str:
        return self.__str__()

    def __int__(self) -> int:
        return self.id


jobs_user = sa.Table(
    'jobs_user',
    SqlAlchemyBase.metadata,
    sa.Column('jobs', sa.Integer, sa.ForeignKey('jobs.id'), primary_key=True),
    sa.Column('users', sa.Integer, sa.ForeignKey('users.id'), primary_key=True)
)

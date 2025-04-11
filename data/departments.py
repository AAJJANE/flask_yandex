import sys

import sqlalchemy as sa
from sqlalchemy import orm

from .__db_session import SqlAlchemyBase, create_session


class Department(SqlAlchemyBase):
    __tablename__ = 'departments'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, unique=True, nullable=False)
    chief = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    email = sa.Column(sa.String, index=True, unique=True, nullable=False)

    chief_obj = orm.relationship('User', backref="departments_chief")
    members_objs = orm.relationship("User",
                                    secondary="department_user",
                                    backref="departments_member")
    jobs = orm.relationship("Jobs", back_populates="department")

    @property
    def members(self) -> str:
        return ', '.join(str(user.id) for user in self.members_objs)

    @members.setter
    def collaborators(self, members: str) -> None:
        from .users import User

        db_sess = orm.object_session(self) or create_session()
        try:
            new_members_objs = [
                db_sess.get(User, _id)
                for _id in map(int, members.split(', '))
            ]
            self.members_objs.clear()
            self.members_objs = new_members_objs
        except Exception as e:
            print('Error:', e, file=sys.stderr)
            db_sess.rollback()

    def __str__(self) -> str:
        return f'Department {self.id}: {self.title}'

    def __repr__(self) -> str:
        return self.__str__()


department_user = sa.Table(
    'department_user',
    SqlAlchemyBase.metadata,
    sa.Column('department', sa.Integer, sa.ForeignKey('departments.id'), primary_key=True),
    sa.Column('user', sa.Integer, sa.ForeignKey('users.id'), primary_key=True)
)
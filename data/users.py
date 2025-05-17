import datetime
import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .__db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    surname = sa.Column(sa.String, nullable=True)
    name = sa.Column(sa.String, nullable=True)
    age = sa.Column(sa.Integer, nullable=True)
    position = sa.Column(sa.String, nullable=True)
    speciality = sa.Column(sa.String, nullable=True)
    address  = sa.Column(sa.String, nullable=True)
    email = sa.Column(sa.String, index=True, unique=True, nullable=True)
    hashed_password = sa.Column(sa.String, nullable=True)
    modified_date = sa.Column(sa.DateTime, default=datetime.datetime.now)

    def set_password(self, password: str) -> None:
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.hashed_password, password)

    def __str__(self) -> str:
        return self.fullname

    def __repr__(self) -> str:
        return f'<User {self.id}: {self.surname} {self.name}>'

    def __int__(self) -> int:
        return self.id

    @property
    def fullname(self) -> str:
        return f'{self.name} {self.surname}'

    def is_admin(self) -> bool:
        return self.id == 1

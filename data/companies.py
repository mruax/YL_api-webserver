import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Company(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'companies'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True, unique=True,
                           nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    phone_number = sqlalchemy.Column(sqlalchemy.String, unique=True)
    post_address = sqlalchemy.Column(sqlalchemy.String, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String)
    INN = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=False)
    KPP = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=False)
    ORGN = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=False)
    OKPO = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=False)

    creator = sqlalchemy.Column(sqlalchemy.String, ForeignKey('users.login'))

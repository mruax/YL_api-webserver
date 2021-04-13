import sqlalchemy
from flask_login import UserMixin
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
    INN = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    KPP = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    ORGN = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    OKPO = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    # name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # login = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    # hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    # email = sqlalchemy.Column(sqlalchemy.String,
    #                           index=True, unique=True, nullable=True)
    # modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
    #                                   default=datetime.datetime.now,
    #                                   nullable=True)
    # jobs = orm.relation("Jobs", back_populates='user')
    # news = orm.relation("News", back_populates='user')
    # permissions = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # def __repr__(self):
    #     print(f"0")

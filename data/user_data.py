import sqlalchemy
import datetime
from data import db_session
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.dialects.postgresql import UUID
import uuid


class UserData(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "user_data"

    uuid = sqlalchemy.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    first_name = sqlalchemy.Column(sqlalchemy.String)
    last_name = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)
    gender = sqlalchemy.Column(sqlalchemy.String)
    date_of_birthday = sqlalchemy.Column(sqlalchemy.Date)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_boss = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    date_of_creation = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

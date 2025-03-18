import sqlalchemy
from data import db_session
from data.db_session import SqlAlchemyBase
from data.user_data import UserData
from data.user_login_data import UserLoginData
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Message(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'message'

    uuid = sqlalchemy.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user = sqlalchemy.Column(UUID(as_uuid=True))
    is_gpt = sqlalchemy.Column(sqlalchemy.Boolean)
    message = sqlalchemy.Column(sqlalchemy.String)

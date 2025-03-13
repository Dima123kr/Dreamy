import sqlalchemy
from data import db_session
from data.db_session import SqlAlchemyBase
from data.user_data import UserData
from data.user_login_data import UserLoginData
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
import uuid


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'user'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    uuid = sqlalchemy.Column(UUID(as_uuid=True), default=uuid.uuid4)

    def get_login_data(self, db_sess=None):
        if not db_sess:
            db_sess = db_session.create_session()
        user_login_data = db_sess.query(UserLoginData).get(self.uuid)
        return user_login_data

    def get_data(self, db_sess=None):
        if not db_sess:
            db_sess = db_session.create_session()
        user_data = db_sess.query(UserData).get(self.uuid)
        return user_data

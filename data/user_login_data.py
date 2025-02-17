import sqlalchemy
from data import db_session
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.dialects.postgresql import UUID
import uuid
from werkzeug.security import generate_password_hash, check_password_hash


class UserLoginData(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "user_password_data"

    uuid = sqlalchemy.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    email = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

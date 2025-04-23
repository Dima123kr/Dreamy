import datetime

import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.dialects.postgresql import UUID
import uuid
from flask_login import current_user


class Diary(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'diary'

    uuid = sqlalchemy.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    try:
        user = sqlalchemy.Column(UUID(as_uuid=True), default=current_user.uuid)
    except Exception as err:
        user = sqlalchemy.Column(UUID(as_uuid=True))
    day = sqlalchemy.Column(sqlalchemy.Date, default=datetime.date.today())
    brief_notes = sqlalchemy.Column(sqlalchemy.Text)
    sleep_start = sqlalchemy.Column(sqlalchemy.Time)
    sleep_end = sqlalchemy.Column(sqlalchemy.Time)
    sleep_imagination = sqlalchemy.Column(sqlalchemy.Text)
    condition_before = sqlalchemy.Column(sqlalchemy.Integer)
    condition_after = sqlalchemy.Column(sqlalchemy.Integer)
    result = sqlalchemy.Column(sqlalchemy.Text)

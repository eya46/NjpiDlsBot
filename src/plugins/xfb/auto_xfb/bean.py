from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from db import db


class AutoPower(db.Model):
    __tablename__ = "auto_power"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    room: str = Column(String)

    type: str = Column(String)
    from_id: str = Column(String)
    user_id: str = Column(String)

    status: bool = Column(Boolean, default=True)
    times: int = Column(Integer, default=0)
    limit: int = Column(Integer, default=9999)

    time: int = Column(Integer)

    last_action_time: datetime = Column(DateTime, default=datetime(1999, month=1, day=1))
    update_time: datetime = Column(DateTime, default=datetime.now)

    def __str__(self) -> str:
        return f"AutoPower({self.room}:{self.status})"

    def __repr__(self):
        return self.__str__()

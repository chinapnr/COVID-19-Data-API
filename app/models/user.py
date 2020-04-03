from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean

from app.db.session import Session
from app.models import Base


class CovidUser(Base):
    __tablename__ = 'covid_user'
    id = Column(Integer, autoincrement=True, primary_key=True, comment="主键")
    create_time = Column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    update_time = Column(DateTime, default=datetime.now, nullable=False, comment="修改时间")
    email = Column(String(100), comment="邮箱地址")
    token = Column(String(255), comment="Token")
    status = Column(Boolean, default=True, nullable=False, comment="状态")

    @staticmethod
    def add_user(*, db: Session, email: str, token: str):
        try:
            new_user = CovidUser(email=email, token=token)
            db.add(new_user)
            db.commit()
        except Exception as _:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def update_user(*, db: Session, condition: dict, data: dict):
        try:
            result = Session.query(CovidUser).filter_by(**condition).update(data)
            db.commit()
            return result
        except Exception as _:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def get_user(*, db: Session, condition: dict):
        try:
            result = db.query(CovidUser).filter_by(**condition).all()
            return result
        except Exception as _:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def get_all_user(*, db):
        try:
            result = db.query(CovidUser).all()
            return result
        except Exception as _:
            db.rollback()
            raise
        finally:
            db.close()

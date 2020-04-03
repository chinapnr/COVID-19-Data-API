from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from app.db.session import Session
from app.models import Base


class Captcha(Base):
    __tablename__ = 'covid_captcha'
    id = Column(Integer, autoincrement=True, primary_key=True, comment="主键")
    create_time = Column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    update_time = Column(DateTime, default=datetime.now, nullable=False, comment="修改时间")
    captcha = Column(String(255), comment="验证码")
    session_id = Column(String(255), comment="session id")
    expiration = Column(String(255), comment="过期时间")

    @staticmethod
    def get_captcha_by_session(*, db: Session, session: str, ):
        try:
            result = db.query(Captcha).filter_by(
                session_id=session
            ).order_by(
                Captcha.id.desc()
            ).first()
            return result
        except Exception as _:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def add_captcha(*, db: Session, captcha: str, session_id: str, expiration: str):
        try:
            new_captcha = Captcha(captcha=captcha, session_id=session_id, expiration=expiration)
            db.add(new_captcha)
            db.commit()
        except Exception as _:
            db.rollback()
            raise
        finally:
            db.close()

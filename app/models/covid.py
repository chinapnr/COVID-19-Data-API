import datetime

from sqlalchemy import Column, Integer, String, Date, and_, func

from app.db.session import Session
from app.models import Base


class Covid19(Base):
    __tablename__ = 'covid19'
    seq_id = Column(Integer, primary_key=True)
    continents_en = Column(String(100), comment="洲英文名")
    continents_ch = Column(String(100), comment="洲中文名")
    country_en = Column(String(100), comment="国家英文名")
    country_ch = Column(String(100), comment="国家中文名")
    province_en = Column(String(100), comment="省份英文名")
    province_ch = Column(String(100), comment="省份中文名")
    confirmed = Column(Integer, comment="确诊人数")
    confirmed_add = Column(Integer, comment="确诊新增")
    deaths = Column(Integer, comment="死亡人数")
    deaths_add = Column(Integer, comment="死亡新增")
    recovered = Column(Integer, comment="治愈数")
    recovered_add = Column(Integer, comment="治愈新增")
    update_date = Column(Date, comment="更新日期")

    @staticmethod
    def get_all(db: Session):
        try:
            result = db.query(Covid19).all()
            return result
        except Exception as _:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def infection_daily_data(*, db: Session, country: str, ):
        try:
            result = db.query(Covid19).filter_by(
                country_en=country,
                update_date=datetime.date.today()
            ).group_by(Covid19.province_en).all()
            db.commit()
            return result
        except Exception as _:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def infection_area_data(*, db: Session, stime: str, etime: str):
        try:
            result = db.query(
                Covid19.continents_en,
                Covid19.continents_ch,
                Covid19.country_en,
                Covid19.country_ch,
                Covid19.province_ch,
                Covid19.province_en
            ).filter(
                Covid19.update_date.between(stime, etime)
            ).group_by(Covid19.continents_en, Covid19.country_en, Covid19.province_en).all()
            return result
        except Exception as _:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def infection_country_data(*, db: Session, country: str, stime: str, etime: str):
        try:
            result = db.query(
                Covid19.country_en, Covid19.country_ch, Covid19.province_en, Covid19.province_ch,
                func.sum(Covid19.confirmed_add).label("sum_confirmed"),
                func.sum(Covid19.deaths_add).label("sum_deaths"),
                func.sum(Covid19.recovered_add).label("sum_recovered"),
            ).filter(
                and_(Covid19.country_en == country, Covid19.update_date.between(stime, etime))
            ).group_by(Covid19.province_en).all()
            return result
        except Exception as _:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def infection_country_detail_data(*, db: Session, country: str, stime: str, etime: str):
        try:
            result = db.query(Covid19).filter(
                and_(Covid19.country_en == country, Covid19.update_date.between(stime, etime))
            ).all()
            return result
        except Exception as _:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def infection_city_data(*, db: Session, city: str, stime: str, etime: str):
        try:
            result = db.query(
                Covid19.country_en, Covid19.country_ch, Covid19.province_en, Covid19.province_ch,
                func.sum(Covid19.confirmed_add).label("sum_confirmed"),
                func.sum(Covid19.deaths_add).label("sum_deaths"),
                func.sum(Covid19.recovered_add).label("sum_recovered"),
            ).filter(
                and_(Covid19.province_en == city, Covid19.update_date.between(stime, etime)
                     )
            ).group_by(Covid19.province_en).all()
            return result
        except Exception as _:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def infection_city_detail_data(*, db: Session, city: str, stime: str, etime: str):
        try:
            result = db.query(Covid19).filter(
                and_(Covid19.province_en == city, Covid19.update_date.between(stime, etime)
                     )
            ).group_by(Covid19.update_date).all()
            return result
        except Exception as _:
            db.rollback()
            raise
        finally:
            db.close()

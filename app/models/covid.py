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
    def get_infection_country_data(*, db: Session, country: str, stime: str, etime: str):
        try:
            result = db.query(
                func.sum(Covid19.confirmed_add).label("confirmed_add"),
                func.sum(Covid19.deaths_add).label("deaths_add"),
                func.sum(Covid19.recovered_add).label("recovered_add"),
            ).filter(
                and_(Covid19.country_en == country, Covid19.update_date.between(stime, etime))
            ).all()
            return result
        except Exception as _:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def get_infection_country_city_data(*, db: Session, country: str, stime: str, etime: str):
        try:
            result = db.query(
                Covid19.province_en,
                func.sum(Covid19.confirmed_add).label("confirmed_add"),
                func.sum(Covid19.deaths_add).label("deaths_add"),
                func.sum(Covid19.recovered_add).label("recovered_add"),
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
    def get_infection_city_data(*, db: Session, city: str, stime: str, etime: str, country: str):
        try:
            if country:
                # 查询条件中有国家
                filters = and_(
                    Covid19.province_en == city,
                    Covid19.update_date.between(stime, etime),
                    Covid19.country_en == country
                )
            else:
                # 查询条件中无国家
                filters = and_(Covid19.province_en == city, Covid19.update_date.between(stime, etime))

            result = db.query(
                func.sum(Covid19.confirmed_add).label("confirmed_add"),
                func.sum(Covid19.deaths_add).label("deaths_add"),
                func.sum(Covid19.recovered_add).label("recovered_add"),
            ).filter(
                and_(filters)
            ).all()
            return result
        except Exception as _:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def get_infection_global_data(*, db: Session, stime: str, etime: str):
        try:
            result = db.query(
                Covid19.country_en,
                func.sum(Covid19.confirmed_add).label("confirmed_add"),
                func.sum(Covid19.deaths_add).label("deaths_add"),
                func.sum(Covid19.recovered_add).label("recovered_add")
            ).filter(
                Covid19.update_date.between(stime, etime)
            ).group_by(Covid19.country_en).all()
            return result
        except Exception as _:
            db.rollback()
            raise
        finally:
            db.close()

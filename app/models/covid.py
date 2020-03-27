from sqlalchemy import Column, Integer, String, Date

from app.db.session import Session
from app.models.base import Base


class Covid19(Base):
    seq_id = Column(Integer, primary_key=True)
    continents_en = Column(String(100), comment="洲英文名")
    continents_ch = Column(String(100), comment="洲中文名")
    country_en = Column(String(100), comment="国家英文名")
    country_ch = Column(String(100), comment="国家英文名")
    province_en = Column(String(100), comment="国家英文名")
    province_ch = Column(String(100), comment="国家英文名")
    confirmed = Column(Integer, comment="确诊人数")
    confirmed_add = Column(Integer, comment="确诊新增")
    deaths = Column(Integer, comment="死亡人数")
    deaths_add = Column(Integer, comment="死亡新增")
    recovered = Column(Integer, comment="治愈数")
    recovered_add = Column(Integer, comment="治愈新增")
    update_date = Column(Date, comment="更新日期")

    @staticmethod
    def get_all(db: Session):
        return db.query(Covid19).all()
from sqlalchemy import Column, Integer, String, Date, and_

from app.db.session import Session, engine
from app.models import Base


class Population(Base):
    __tablename__ = 'country_population'
    seq_id = Column(Integer, autoincrement=True, primary_key=True, comment="主键")
    country_en = Column(String(255), comment="国家英文名")
    country_ch = Column(String(255), comment="国家中文名")
    population_num = Column(Integer, comment="人口数量")
    update_date = Column(Date, comment="更新日期")

    @staticmethod
    def get_population(*, db: Session, country: str):
        try:
            if country:
                filters = and_(
                    Population.country_en == country
                )
            else:
                filters = and_(1==1)
            result = db.query(Population).filter(filters).all()
            return result
        except Exception as _:
            db.rollback()
            raise
        finally:
            db.close()


if __name__ == '__main__':
    Base.metadata.create_all(engine)

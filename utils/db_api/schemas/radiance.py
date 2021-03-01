from sqlalchemy import Integer, Column, BigInteger, String, sql, ForeignKey, UniqueConstraint

from utils.db_api.db_gino import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'users_radiance'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(100))
    tg_id = Column(BigInteger, unique=True)
    referral = Column(BigInteger)

    query: sql.Select


class RadianceImg(TimedBaseModel):
    __tablename__ = 'radiance_img'
    id = Column(BigInteger, primary_key=True)
    photo_id = Column(String(2000))
    year = Column(Integer)
    month = Column(String)
    owner_id = Column(Integer, ForeignKey('users_radiance.tg_id'))
    state = Column(String(200))
    __table_args__ = UniqueConstraint('year', 'month', 'owner_id')

    query: sql.Select

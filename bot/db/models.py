from sqlalchemy import Column, Integer, BigInteger, String, Float, DateTime, func

from bot.db.base import Base


class ProductModel(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    photo_url = Column(String)
    price = Column(Float)
    description = Column(String)

    def __repr__(self):
        return (f"<Product(id={self.id}, name='{self.name}', "
                f"photo_url='{self.photo_url[:15]}...', price={self.price}, "
                f"description='{self.description[:10]}...')>")


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    name = Column(String)
    username = Column(String)
    date_registered = Column(DateTime, default=func.now())

    def __repr__(self):
        return (f"<User(id={self.id}, telegram_id={self.telegram_id}, "
                f"name='{self.name}', username='{self.username}', "
                f"date_registered={self.date_registered})>")

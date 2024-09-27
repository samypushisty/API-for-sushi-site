from datafunctions import naive_utcnow
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, CheckConstraint
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# таблица с пользователями
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=naive_utcnow())


# таблица с едой
class Food(Base):
    __tablename__ = "food"
    id = Column(Integer, primary_key=True)
    image_url = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False, unique=True)
    body = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    type = Column(String, nullable=False)

    __table_args__ = (
        CheckConstraint("type IN ('sushi', 'drink', 'sauce')", name='check_valid_type'),
    )


# таблица с сетами
class Set(Base):
    __tablename__ = "set"
    id = Column(Integer, primary_key=True)
    image_url = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)


# таблица с новостями
class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    body = Column(String, nullable=False)


# таблица с историей покупок
class UsersHistory(Base):
    __tablename__ = "users_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    food_id = Column(Integer, ForeignKey("food.id"))
    енз


# лист избранного
class UsersFavoriteFood(Base):
    __tablename__ = "users_favorite_food"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    food_id = Column(Integer, ForeignKey("food.id"))


class UsersFavoriteSet(Base):
    __tablename__ = "users_favorite_set"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    set_id = Column(Integer, ForeignKey("set.id"))


# еда в сете
class FoodInSet(Base):
    __tablename__ = "food_in_set"

    id = Column(Integer, primary_key=True)
    set_id = Column(Integer, ForeignKey("set.id"))
    food_id = Column(Integer, ForeignKey("food.id"))


# адреса пользователя
class UserAddress(Base):
    __tablename__ = "user_address"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    address = Column(String, nullable=False)

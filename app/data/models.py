from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    genres = Column(String)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), index=True, nullable=False)
    rating = Column(Float, nullable=False)
    timestamp = Column(Integer)

def init_db(url="sqlite:///recommender.db"):
    engine = create_engine(url)
    Base.metadata.create_all(engine)
    return engine

if __name__ == "__main__":
    init_db()
    print("DB created")

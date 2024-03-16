import sqlalchemy
from sqlalchemy.orm import Session, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Chat(Base):
    __tablename__ = "chats"
    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    message = sqlalchemy.Column(sqlalchemy.String)
    detected_tag = sqlalchemy.Column(sqlalchemy.String)


class Prakriti(Base):
    __tablename__ = "dataset"
    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    body_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    body_width = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    height = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    bone_structure = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    complexion = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    general_feel_of_skin = sqlalchemy.Column(
        sqlalchemy.Integer, nullable=False)
    texture_of_skin = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    hair_color = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    appearance_of_hair = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    shape_of_face = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    eyes = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    eyelashes = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    blinking_of_eyes = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    cheeks = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    nose = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    teeth_and_gums = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    lips = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    nails = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    appetite = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    liking_tastes = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    dosha = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)


def initDB() -> Session:
    engine = sqlalchemy.create_engine("sqlite:///prakriti.db")
    session = Session(engine)
    Base.metadata.create_all(engine)
    return session

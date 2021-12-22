import datetime
from sqlalchemy import Index, Column, Integer, String, Sequence, DateTime, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, relationship, backref


Base = declarative_base()


def initialize(dbname):
    engine = create_engine('sqlite:///' + dbname, echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def write_to_db(session, new_entries):
    dict = {entry.link : entry for entry in new_entries}
    for entry in session.query(AlbumType.album_id).filter(AlbumType.album_id.in_(dict.keys())).all():
        session.merge(dict.pop(entry.link))
    session.add_all(dict.values())
    session.commit()


def read_db(session):
    for instance in session.query(AlbumType).order_by(AlbumType.id):
        print(instance)


class AlbumType(Base):
    __tablename__ = "album"

    id = Column(Integer, Sequence("id_seq"), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    last_updated_at = Column(DateTime, onupdate=datetime.datetime)
    album_id = Column(String, primary_key=True)
    upload_date = Column(String)
    title = Column(String)
    n_media = Column(String)
    model = Column(String)
    tags = Column(String)

    def __repr__(self):
        return f"<Album(title={self.title}, tags={self.tags})>"


class ScriptType(Base):
    __table__name = "script"
    
    id = Column(Integer, Sequence("id_seq"), unique=True, index=True, primary_key=True)
    album_id = Column(String, ForeignKey("AlbumType.album_id"))
    media_id = Column(String)
    media_type = Column(String)
    model = Column(String)
    tags = Column(String)
    
    def __repr__(self):
        return f"<Media(id={self.media_id}, type={self.media_type}, tags={self.tags})>"
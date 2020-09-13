from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


Engine = create_engine(
    "postgresql://db_user:secret@db:5432/cc",
    encoding="utf-8",
    echo=True,
)

Session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=True,
        bind=Engine
    )
)

ModelBase = declarative_base()

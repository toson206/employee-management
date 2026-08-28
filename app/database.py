from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:1@localhost:5432/employee_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    from . import models
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    with engine.connect() as connection:
        print("Kết nối PostgreSQL thành công!")
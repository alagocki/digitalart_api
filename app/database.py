from sqlmodel import Session, SQLModel, create_engine
from pathlib import Path
import os

engine = create_engine("postgresql+psycopg2://digitalart:digitalart@db:5432/digitalart")


def get_db():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def shutdown():
    cwd = Path.cwd().resolve()
    db_file = [file for file in os.listdir() if file.endswith(".db")][0]
    os.remove(os.path.join(cwd, db_file))


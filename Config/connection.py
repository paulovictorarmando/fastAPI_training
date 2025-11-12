from sqlmodel import SQLModel, create_engine, Session
from Config.settings import ENV

engine = create_engine(ENV.DATABASE_URL, echo=True)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
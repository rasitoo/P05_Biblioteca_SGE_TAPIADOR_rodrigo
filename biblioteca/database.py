#Crear engine de sqlalchemy sacado de https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#create-the-engine
from sqlmodel import SQLModel, create_engine, Session

class Database:
    def __init__(self, db_name):
        self.engine = create_engine(f"sqlite:///{db_name}", echo=False)

    def init_db(self):
        SQLModel.metadata.create_all(self.engine)

    def get_session(self):
        with Session(self.engine) as session:
            yield session
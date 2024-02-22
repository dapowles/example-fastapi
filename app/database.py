from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from .config import settings

sql_url = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(sql_url, echo=True)

local_session = sessionmaker(autocommit = False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg.connect(host = 'localhost', dbname='fastapi', row_factory=dict_row, 
#                             user='postgres', password='1i2z3e4A')
#         cur = conn.cursor()
#         print('db connection succeeded')
#         break
#     except Exception as error:
#         print(error)  
#         time.sleep(2)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import dbusername, dbpassword, dbname, dbhost
 
# SQL_ALCHEMY_DB_URL = 'sqlite:///./akj.db'
# SQL_ALCHEMY_DB_URL = 'mysql://root:root@localhost/app_jyotish_db'

# SQL_ALCHEMY_DB_URL = 'mysql://'+dbusername+':'+dbpassword+'@'+dbhost+'/'+dbname

SQL_ALCHEMY_DB_URL = 'mysql://deluser:Sysadmin#$987@13.233.156.171/app_jyotish_db'

engine = create_engine(SQL_ALCHEMY_DB_URL, encoding='latin1', echo=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,) 


Base = declarative_base()


def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
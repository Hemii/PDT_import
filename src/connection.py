from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# create an engine
engine = create_engine('postgresql://root:root@localhost:54378/pdt')

Session = sessionmaker(bind=engine)

Base = declarative_base()
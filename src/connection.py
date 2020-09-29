from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# create an engine
engine = create_engine('postgresql://root:root@localhost:54378/sqlalchemy')

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgresql://nrdhmlja:Wns0JwGi7_J-CaDAAKC9-LmUVKTtJo38@balarama.db.elephantsql.com:5432/nrdhmlja')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
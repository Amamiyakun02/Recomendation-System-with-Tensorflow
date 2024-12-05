import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import dotenv
import os

dotenv.load_dotenv('.env.local')
engine = sqlalchemy.create_engine(f"mysql+pymysql://"+os.getenv("DATABASE_URL"))
Base = declarative_base()

Base.metadata.create_all(engine)

# engine = engine.connect()
Session = sessionmaker(bind=engine)

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import dotenv
import os

# dotenv.load_dotenv('.env.local')
dotenv.load_dotenv('.env.production')
db_user = os.getenv('DB_USER')
db_host = os.getenv('DB_HOST')
db_pass = os.getenv('DB_PASS')
db_name = os.getenv('DB_NAME')
# engine = sqlalchemy.create_engine(f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}")
engine = sqlalchemy.create_engine(f"mysql+pymysql://{os.getenv('DATABASE_CLOUD_URL')}")
Base = declarative_base()

Base.metadata.create_all(engine)

# engine = engine.connect()
Session = sessionmaker(bind=engine)

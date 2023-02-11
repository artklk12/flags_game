from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://user:VCfyJqOKU7K64urnaUPLpB1lHxZVlEXu@dpg-cfjvad9mbjsn9ea1t83g-a.frankfurt-postgres.render.com/flags"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

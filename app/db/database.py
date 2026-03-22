from app.db.data import employers_data, jobs_data
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from app.db.models import Base,Employer, Job
from app.settings.config import DATABASE_URL
from dotenv import load_dotenv
import os

# for local
# load_dotenv()
# DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def prepare_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = Session()

    for employer in employers_data:
    # ** → unpacking the dictionary
        emp = Employer(**employer)
        session.add(emp)

    for job in jobs_data:
        job = Job(**job)
        session.add(job)
    
    session.commit()
    session.close()
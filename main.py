from graphene import Field, Int, Schema, ObjectType, String, List
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_graphiql_handler, make_playground_handler
from sqlalchemy import create_engine, Column, Integer, String as saString, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from dotenv import load_dotenv
import os

# for local
load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)

Base = declarative_base()

Session = sessionmaker(bind=engine)

class Employer(Base):
    __tablename__ = "employers"

    id = Column(Integer, primary_key=True)
    name = Column(saString)
    contact_email = Column(saString)
    industry = Column(saString)
    jobs = relationship("Job", back_populates="employer")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    title = Column(saString)
    description = Column(saString)
    employer_id = Column(Integer, ForeignKey("employers.id"))
    employer = relationship("Employer", back_populates="jobs")

# static data
employers_data = [
    {"id": 1, "name": "Google", "contact_email": "info@google.com", "industry": "Technology"},
    {"id": 2, "name": "Apple", "contact_email": "info@apple.com", "industry": "Technology"},
    {"id": 3, "name": "Microsoft", "contact_email": "info@microsoft.com", "industry": "Finance"}
]

jobs_data = [
    {"id": 1, "title": "Software Engineer", "description": "Develop web applications", "employer_id": 1},
    {"id": 2, "title": "Product Manager", "description": "Manage product development", "employer_id": 2},
    {"id": 3, "title": "Financial Analyst", "description": "Analyze financial data", "employer_id": 3},
    {"id": 4, "title": "Marketing Manager", "description": "Manage marketing campaigns", "employer_id": 1},
]

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

class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List(lambda: JobObject)

    @staticmethod
    def resolve_jobs(root, info):
        return [job for job in jobs_data if job["employer_id"] == root.id]

class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject)

    @staticmethod
    def resolve_employer(root, info):
        return next((employer for employer in employers_data if employer["id"] == root.employer_id), None)

class Query(ObjectType):
    jobs = List(JobObject)
    employers = List(EmployerObject)

    @staticmethod
    def resolve_jobs(root, info):
        return jobs_data
    
    @staticmethod
    def resolve_employers(root, info):
        return employers_data

schema = Schema(query=Query)

app = FastAPI()

@app.on_event("startup")
def startup_event():
    prepare_database()

app.mount("/graphql", GraphQLApp(
    schema=schema,
    on_get=make_graphiql_handler()
))

app.mount("/graphql-p", GraphQLApp(
    schema=schema,
    on_get=make_playground_handler()
))
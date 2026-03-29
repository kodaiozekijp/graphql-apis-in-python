import strawberry
from app.db.models import Job
from app.db.database import Session
from app.gql.types import JobType

@strawberry.type
class Mutation:

    @strawberry.mutation
    def add_job(self, title: str, description: str, employer_id: int) -> JobType:
        with Session() as session:
            job = Job(title=title, description=description, employer_id=employer_id)
            session.add(job)
            session.commit()
            session.refresh(job)
            return job

    @strawberry.mutation
    def udpate_job(self, job_id: int, title: str = None, description: str = None, employer_id: int = None) -> JobType:
        with Session() as session:
            job = session.query(Job).filter(Job.id == job_id).first()
            if not job:
                raise Exception("Job not found")
            if title:
                job.title = title
            if description:
                job.description = description
            if employer_id:
                job.employer_id = employer_id
            session.commit()
            session.refresh(job)
            return job
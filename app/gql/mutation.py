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

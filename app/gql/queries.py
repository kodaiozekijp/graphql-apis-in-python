from typing import List
from app.gql.types import JobType, EmployerType
from app.db.models import Job, Employer
from app.db.database import Session
from sqlalchemy.orm import joinedload
import strawberry
from strawberry.types import Info

@strawberry.type
class Query:
    # jobs = List(JobObject)
    # employers = List(EmployerObject)

    @strawberry.field
    def employers(self, info: Info) -> List[EmployerType]:
        return Session().query(Employer).options(joinedload(Employer.jobs)).all()

    @strawberry.field
    def jobs(self, info: Info) -> List[JobType]:
        return Session().query(Job).options(joinedload(Job.employer)).all()
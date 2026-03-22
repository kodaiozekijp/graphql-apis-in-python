import strawberry
from typing import Optional, List

@strawberry.type
class EmployerType:
    id : int
    name : str
    contact_email : str
    industry : str
    jobs : List["JobType"]

    # @staticmethod
    # def resolve_jobs(root, info):
    #     return [job for job in jobs_data if job["employer_id"] == root.id]

@strawberry.type
class JobType:
    id : int
    title : str
    description : str
    employer_id : int
    employer : Optional[EmployerType]

    # @staticmethod
    # def resolve_employer(root, info):
    #     return next((employer for employer in employers_data if employer["id"] == root.employer_id), None)
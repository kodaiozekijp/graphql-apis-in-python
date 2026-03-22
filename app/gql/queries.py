from graphene import ObjectType, List
from app.gql.types import JobObject, EmployerObject
from app.db.data import jobs_data, employers_data

class Query(ObjectType):
    jobs = List(JobObject)
    employers = List(EmployerObject)

    @staticmethod
    def resolve_jobs(root, info):
        return jobs_data
    
    @staticmethod
    def resolve_employers(root, info):
        return employers_data
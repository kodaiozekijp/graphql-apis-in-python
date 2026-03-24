from fastapi import FastAPI
from app.gql.mutation import Mutation
from app.gql.queries import Query
from app.db.database import prepare_database
from app.db.models import Employer, Job
from app.db.database import Session
import strawberry
from contextlib import asynccontextmanager
from strawberry.fastapi import GraphQLRouter

@asynccontextmanager
async def lifespan(app: FastAPI):
    prepare_database()
    yield

app = FastAPI(lifespan=lifespan)

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema=schema)

app.include_router(graphql_app, prefix="/graphql")

# @app.on_event("startup")
# def startup_event():
#     prepare_database()

@app.get("/employers")
def get_employers():
    session = Session()
    employers = session.query(Employer).all()
    session.close()
    return employers

@app.get("/jobs")
def get_jobs():
    with Session() as session:
        return session.query(Job).all()

# app.mount("/graphql", GraphQLApp(
#     schema=schema,
#     on_get=make_graphiql_handler()
# ))

# app.mount("/graphql-p", GraphQLApp(
#     schema=schema,
#     on_get=make_playground_handler()
# ))
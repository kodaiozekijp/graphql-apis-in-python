from os import name
from graphene import List, Schema, ObjectType, String, Int, Field, Mutation

# class Query(ObjectType):
#     hello = String(name=String(default_value="World"))

#     def resolve_hello(self, info, name):
#         return f"Hello {name}"

class UserType(ObjectType):
    id = Int()
    name = String()
    age = Int()

class Query(ObjectType):
    # dummy data store
    users = [
        {"id": 1, "name": "Andy Doe", "age": 25},
        {"id": 2, "name": "Bobby Doe", "age": 26},
        {"id": 3, "name": "Cindy Doe", "age": 27},
        {"id": 4, "name": "Danny Doe", "age": 28}
    ]

    user = Field(UserType, user_id=Int())
    users_by_min_age = List(UserType, min_age=Int())

    @staticmethod
    def resolve_user(root, info, user_id):
        print(root)
        matched_users = [user for user in Query.users if user["id"] == user_id]
        return matched_users[0] if matched_users else None

    @staticmethod
    def resolve_users_by_min_age(root, info, min_age):
        return [user for user in Query.users if user["age"] >= min_age]

class CreateUser(Mutation):
    class Arguments:
        name = String()
        age = Int()

    user = Field(UserType)

    @staticmethod
    def mutate(root, info, name, age):
        user = {"id": len(Query.users) + 1, "name": name, "age": age}
        Query.users.append(user)
        return CreateUser(user=user)

class UpdateUser(Mutation):
    class Arguments:
        user_id = Int(required=True)
        name = String()
        age = Int()

    user = Field(UserType)
    
    @staticmethod
    def mutate(root, info, user_id, name=None, age=None):
        user = None
        for u in Query.users:
            if u["id"] == user_id:
                user = u
                break
            
        if not user:
                return None
            
        if name is not None:
                user["name"] = name
            
        if age is not None:
                user["age"] = age

        return UpdateUser(user=user)

class DeleteUser(Mutation):
    class Arguments:
        user_id = Int(required=True)

    user = Field(UserType)

    @staticmethod
    def mutate(root, info, user_id):
        user = None
        
        for idx,u in enumerate(Query.users):
            if u["id"] == user_id:
                user = u
                del Query.users[idx]
                break
        
        if not user:
            return None
        
        return DeleteUser(user=user)

class Mutation(ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

schema = Schema(query=Query, mutation=Mutation)

# gql = '''
# {
#     # hello(name: "grahql")
# }
# '''

gql = '''
query{
    user(userId: 1) {
        id
        name
        age
    }
}
'''

# gql_2 = '''
# query {
#     usersByMinAge(minAge: 26) {
#         id
#         name
#         age
#     }
# }
# '''

# gql = '''
# mutation {
#     createUser(name: "Ethan Doe", age: 29) {
#         user {
#             id
#             name
#             age
#         }
#     }
# }
# '''

# gql_update = '''
# mutation {
#     updateUser(userId: 1, name: "Update user", age: 100) {
#         user {
#             id
#             name
#             age
#         }
#     }
# }
# '''

gql_delete = '''
mutation {
    deleteUser(userId: 1) {
        user {
            id
            name
            age
        }
    }
}
'''

if __name__ == '__main__':
    result = schema.execute(gql, root_value="another value")
    print(result)
    result = schema.execute(gql_delete, root_value="another value")
    print(result)
    result = schema.execute(gql, root_value="another value")
    print(result)
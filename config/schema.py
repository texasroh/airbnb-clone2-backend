import strawberry
from rooms import schema as rooms_schema
from users import schema as users_schema


@strawberry.type
class Query(rooms_schema.Query):
    pass


@strawberry.type
class Mutation(users_schema.Mutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)

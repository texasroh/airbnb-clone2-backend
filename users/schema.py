import strawberry
from . import mutations


@strawberry.type
class Mutation:
    log_in: bool = strawberry.mutation(resolver=mutations.log_in)
    log_out: bool = strawberry.mutation(resolver=mutations.log_out)

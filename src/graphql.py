from ariadne import QueryType, ObjectType
from flask import g
import os

ACCESS_TOKEN_TIMEOUT = os.environ["ACCESS_TOKEN_TIMEOUT"]

query = QueryType()

@query.field("me")
def resolve_me(_, info):
    request = info.context
    accessToken = request.headers.get("Authorization").split(" ")[1]

    

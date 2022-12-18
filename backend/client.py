from ariadne import make_executable_schema, load_schema_from_path, \
    snake_case_fallback_resolvers, upload_scalar
from starlette.middleware.cors import CORSMiddleware
from ariadne.asgi import GraphQL
from ariadne.asgi.handlers import GraphQLTransportWSHandler

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(type_defs, upload_scalar)

app = CORSMiddleware(GraphQL(schema, debug=True, websocket_handler=GraphQLTransportWSHandler(),), allow_origins=['*'], allow_methods=("GET", "POST", "OPTIONS"))
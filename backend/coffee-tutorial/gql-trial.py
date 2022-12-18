from flask import Flask, request, jsonify
from flask_cors import CORS
from ariadne import QueryType, MutationType, graphql_sync, make_executable_schema, gql, load_schema_from_path
from ariadne.constants import PLAYGROUND_HTML
from model import query, mutation

type_defs = gql(load_schema_from_path("./schema.graphql"))
schema = make_executable_schema(type_defs,query,mutation)


app = Flask(__name__)
# CORS(app)
cors = CORS(app, resources={r"/graphql": {"origins": "*"}})

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == '__main__':
  app.run()
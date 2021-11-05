from flask import Flask, request, jsonify
from ariadne import gql, make_executable_schema, load_from_schema
from ariadne.constants import PLAYGROUND_HTML

from graphql import query

schema = make_executable_schema(load_schema_from_path("../schema.graphql"), query)
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("graphql", methods = ["GET", "POST"])
def graphql():
    if request.method == "POST":
        data = request.get_json()

        success, result = graphql_sync(
            schema,
            data,
            context_value=requst,
            debug=app.debug
        )
        
        status_code = 200 if success else 400
        return jsonify(result), status_code
    else:
        return PLAYGROUND_HTML, 200
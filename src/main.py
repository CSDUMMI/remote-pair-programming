import os
import uuid
from flask import Flask, request, jsonify, g
from Crypto.Hash import SHA256, get_random_bytes
from ariadne import gql, make_executable_schema, load_from_schema, graphql_sync
from ariadne.constants import PLAYGROUND_HTML

from graphql import query
import database as db

schema = make_executable_schema(load_schema_from_path("../schema.graphql"), query)
app = Flask(__name__)

g["accessTokens"] = dict()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    name = request.form["name"]
    password = request.form["password"]

    user = db.User.get(db.User.name == name)
    
    if user.password_hash == SHA256.new(data = password.encode("utf-8") + user.password_salt).digest():
        accessToken = get_random_bytes(16).decode("utf-8")
        g["accessTokens"][accessToken] = {
            "time": time.time(),
            "id": user.id,
        }
        return accessToken, 200
    else:
        return "401 Unauthorized", 401

@app.route("/signup", methods=["POST"])
def signup():
    name = request.form["name"]
    password = request.form["password"]
    languages = request.form.get("languages", default = ["eng", "deu"])

    password_salt = generate_random_bytes(32)

    password_hash = SHA256.new(password.encode("utf-8") + password_salt).digest()

    user = db.User.create(
        id = uuid.uuid4(),
        name = name,
        languages = languages,
        password_hash = password_hash,
        password_salt = password_salt,
    )

    return "signed up", 200

@app.route("graphql", methods = ["GET", "POST"])
def graphql():
    if request.method == "POST":
        accessToken = request.headers.get("Authorization").split(" ")[1]

        if g["accessTokens"][accessToken]["time"] - time.time() > ACCESS_TOKEN_TIMEOUT:
            return "401 Unauthorized", 401

        data = request.get_json()

        success, result = graphql_sync(
            schema,
            data,
            context_value={ 
                request: request,
                user: g["accessToken"][accessToken]["id"],
            },
            debug=app.debug
        )
        
        status_code = 200 if success else 400
        return jsonify(result), status_code
    else:
        return PLAYGROUND_HTML, 200
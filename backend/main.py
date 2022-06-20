# main file just like in the ML project to initializing the project
from flask import Flask
from flask_restx import Api
from models import Recipe,User
from exts import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from recipes import recipe_ns
from auth import auth_ns
# from flask_cors import CORS

def create_app(config):
    app=Flask(__name__,static_url_path='/',static_folder='./client/build')
    # config param can hold either DevConfig,ProdConfig or TestConfig(UATConfig,OATConfig) values
    app.config.from_object(config)

    # CORS(app)

    # registers SQL_ALCHEMY to work with our application
    db.init_app(app)

    # to integrate flask_migrate with our application
    migrate=Migrate(app,db)
    JWTManager(app)

    # this is the path to our swagger document.
    api=Api(app,doc='/docs')

    # adding recipie and auth namespaces for ref
    api.add_namespace(recipe_ns)
    api.add_namespace(auth_ns)

    # default index route
    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    @app.errorhandler(404)
    def not_found(err):
        return app.send_static_file('index.html')

    # used in python shell and uses SQLAlchemy engine to create Recipe db a model serializer
    @app.shell_context_processor
    def make_shell_context():
        return{
            "db":db,
            "Recipe":Recipe,
            "user":User
        }


    return app

# After testing the main app by running python main.py on terminal and using 
# http://127.0.0.1:5000/docs we see our swagger document.
# Testing my API on Insomnia testing tool since dont have selenium as it requires potential enterprise leve setup for SaaS
# server and IDE etc 
# inside insomnia create a new request called fetch which is a GET request in the GET type localhost:5000/fetch and press
# enter we get preview {"message":"fetching resources"}
# at this point we have created our first API
# We will be creating our database model at this point

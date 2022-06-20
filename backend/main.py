#main file just like in the ML project to initializing the project

from ast import Delete
from datetime import date
from dis import Instruction
from unicodedata import category
from flask import Flask,request
from flask_restx import Api,Resource,fields
from config import DevConfig
from  models import Recipe
from exts import db

app=Flask(__name__)
app.config.from_object(DevConfig)

# registers SQL_ALCHEMY to work with our application
db.init_app(app)

# this is the path to our swagger document.
api=Api(app,doc='/docs')

# basically in the name of serializer we are mapping our tables to a jason object
recipe_model=api.model(
    "Recipe",
    {
        "id":fields.Integer(),
        "name":fields.String(),
        "ingredients":fields.String(),
        "instructions":fields.String(),
        "serving_size":fields.String(),
        "category":fields.String(),
        "notes":fields.String(),
        "date_added":fields.String(),
        "date_modified":fields.String()
    }
)

@api.route('/fetch')
class FetchResource(Resource):
    def get(self):
        return {"message":"fetching resources"}

#Creating various CRUD Routes:

@api.route('/recipes')
class CookingRecipes(Resource):
    @api.marshal_list_with(recipe_model)
    def get(self):
        """Get all recipes from db (Read all operation)"""
        recipes=Recipe.query.all() #which returns a SQLAlchemy object and we convert it to JSON using marshal serializer model. Goto insomnia and test the API using a new GET request "Get_All_Recipes"
        
        return recipes


    @api.marshal_with(recipe_model)
    def post(self):
        """Create a new recipe (add/Create operation)"""
        #here we are going to use the flask request method to create a new row by acquiring data that comes as request from client.
        data=request.get_json()

        new_recipe=Recipe(
            name=data.get('name'),
            ingredients=data.get('ingredients'),
            instructions=data.get('instructions'),
            serving_size=data.get('serving_size'),
            category=data.get('category'),
            notes=data.get('notes'),
            date_added=data.get('date_added'),
            date_modified=data.get('date_modified'),
        )

        new_recipe.save()
        # returning the new recipe created with success status code. And test it in insomnia as a new POST request
        return new_recipe,201

@api.route('/recipe/<int:id>')
class CookingRecipes(Resource):
    def get(self,id):
        """Get a recipe by id(Read one operation)"""
        pass

    def put(self,id):
        """update a recipe by id(Update operation)"""
        pass

    def delete(self,id):
        """delete a recipe by id(delete operation)"""
        pass

# used in python shell and uses SQLAlchemy engine to create Recipe db
@app.shell_context_processor
def make_shell_context():
    return{
        "db":db,
        "Recipe":Recipe
    }


if __name__== '__main__':
    app.run()

# After testing the main app by running python main.py on terminal and using 
# http://127.0.0.1:5000/docs we see our swagger document.
# Testing my API on Insomnia testing tool since dont have selenium as it requires potential enterprise leve setup for SaaS
# server and IDE etc 
# inside insomnia create a new request called fetch which is a GET request in the GET type localhost:5000/fetch and press
# enter we get preview {"message":"fetching resources"}
# at this point we have created our first API
# We will be creating our database model at this point

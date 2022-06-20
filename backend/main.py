# main file just like in the ML project to initializing the project
from os import access
from flask import Flask, jsonify,request,jsonify
from flask_restx import Api,Resource,fields
import jwt
from config import DevConfig
from models import Recipe,User
from exts import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager,create_access_token,create_refresh_token,jwt_required
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)
app.config.from_object(DevConfig)

# registers SQL_ALCHEMY to work with our application
db.init_app(app)

# to integrate flask_migrate with our application
migrate=Migrate(app,db)

JWTManager(app)

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

signup_model=api.model(
    'SignUp',
    {
        "username":fields.String(),
        "email":fields.String(),
        "password":fields.String()
    }
)

signin_model=api.model(
    'SignIn',
    {
        "username":fields.String(),
        "password":fields.String()
    }
)


@api.route('/fetch')
class FetchResource(Resource):
    def get(self):
        return {"message":"fetching resources"}

# Creating routes for User LOGIN -> using JWT 
@api.route('/signup')
@api.expect(signup_model)
class SignUp(Resource):
    # @api.marshal_with(signup_model)
    def post(self):
        # this data is the data sent by client using the post method.
        # here we are going to make use of werkzeug library to check and encrypt our password using hash code
        data=request.get_json()

        # exception handling if user already exists in db
        # getting from client request
        username=data.get('username') 
        # getting from querying the database
        db_user=User.query.filter_by(username=username).first() 

        if db_user is not None:
            return jsonify({"message":f"User with username {username} is taken."})

        new_user=User(
            username=data.get('username'),
            email=data.get('email'),
            password=generate_password_hash(data.get('password'))
        )

        new_user.save()

        # lets check the API in Insomnia 
        # instead of returning new user object with credentials we will simply return success message
        # return new_user,201 
        return jsonify({"message":"User Successfully created"})

@api.route('/signin')
@api.expect(signin_model)
class SignIn(Resource):
    def post(self):
        data=request.get_json()

        username=data.get('username')
        password=data.get('password')

        db_user=User.query.filter_by(username=username).first()

        # Now to check if the user exists in the db and authenticate the user.
        # we will be using two additional functions 
        if db_user and check_password_hash(db_user.password,password):

            access_token=create_access_token(identity=db_user.username)
            refresh_token=create_refresh_token(identity=db_user.username)

            return jsonify({
                "access token":access_token,"refresh_token":refresh_token
            })


# Creating various CRUD Routes:

@api.route('/recipes')
class CookingRecipes(Resource):
    @api.marshal_list_with(recipe_model)
    def get(self):
        """Get all recipes from db (Read all operation)"""
        recipes=Recipe.query.all() #which returns a SQLAlchemy object and we convert it to JSON using marshal serializer model which is a decorator. Goto insomnia and test the API using a new GET request "Get_All_Recipes"
        
        return recipes


    @api.marshal_with(recipe_model)
    # the expect decorator helps with showing the payload for a given contract model.
    @api.expect(recipe_model)
    @jwt_required()
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

    @api.marshal_with(recipe_model)
    def get(self,id):
        """Get a recipe by id(Read one operation)"""
        recipe=Recipe.query.get_or_404(id) # the query checks for a recipe with given id and if not found returns a 404 error
        # create a new GET request in insomnia (get_one_recipe) and localhost:5000/recipe/1. We should get a recipe with id 1
          
        return recipe

    @api.marshal_with(recipe_model)
    @jwt_required()
    def put(self,id):
        """update a recipe by id(Update operation)"""
        # first we check if the recipe that is queried for update exists in the database
        recipe_to_update=Recipe.query.get_or_404(id)
        #next we fetch the data sent as request by the client and update the target recipe in the database
        mod_data=request.get_json()
        # for update operation we will not use or allow date_added to be part of request object or query object.
        #date_added is created by default by the model system at time of creation of the recipe just like id.
        recipe_to_update.update(mod_data.get('name'),mod_data.get('ingredients'),mod_data.get('instructions'),mod_data.get('serving_size'),mod_data.get('category'),mod_data.get('notes'),mod_data.get('date_modified'))

        #lets test it in insomnia using new put request update_a_recipe. here date modified should take in system date time to reflect the current time of update operation.

        return recipe_to_update

    @api.marshal_with(recipe_model)
    @jwt_required()
    def delete(self,id):
        """delete a recipe by id(delete operation)"""
        recipe_to_delete=Recipe.query.get_or_404(id)
        recipe_to_delete.delete()
        # next we test our delete operation in insomnia with a delete_a_recipe DELETE request
        return recipe_to_delete

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

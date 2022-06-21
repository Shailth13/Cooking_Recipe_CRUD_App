from flask_restx import Namespace,Resource,fields
from models import Recipe
from flask_jwt_extended import jwt_required
from flask import request
import datetime


recipe_ns=Namespace('recipe',description="A namespace for Recipes")


# basically in the name of serializer we are mapping our tables to a jason object
recipe_model=recipe_ns.model(
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

@recipe_ns.route('/fetch')
class FetchResource(Resource):
    def get(self):
        return {"message":"fetching resources"}

# Creating various CRUD Routes:

@recipe_ns.route('/recipes')
class CookingRecipes(Resource):

    @recipe_ns.marshal_list_with(recipe_model)
    def get(self):
        """Get all recipes from db (Read all operation)"""
        recipes=Recipe.query.all() #which returns a SQLAlchemy object and we convert it to JSON using marshal serializer model which is a decorator. Goto insomnia and test the API using a new GET request "Get_All_Recipes"

        return recipes


    @recipe_ns.marshal_with(recipe_model)
    @recipe_ns.expect(recipe_model)
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
            date_added=datetime.datetime.now(),
            date_modified='',
        )

        new_recipe.save()
        # returning the new recipe created with success status code. And test it in insomnia as a new POST request

        return new_recipe,201




@recipe_ns.route('/recipe/<int:id>')
class CookingRecipes(Resource):

    @recipe_ns.marshal_with(recipe_model)
    def get(self,id):
        """Get a recipe by id(Read one operation)"""
        recipe=Recipe.query.get_or_404(id) # the query checks for a recipe with given id and if not found returns a 404 error
        # create a new GET request in insomnia (get_one_recipe) and localhost:5000/recipe/1. We should get a recipe with id 1

        return recipe


    @recipe_ns.marshal_with(recipe_model)
    @jwt_required()
    def put(self,id):
        """update a recipe by id(Update operation)"""
        # first we check if the recipe that is queried for update exists in the database
        recipe_to_update=Recipe.query.get_or_404(id)
        #next we fetch the data sent as request by the client and update the target recipe in the database
        mod_data=request.get_json()
        # for update operation we will not use or allow date_added to be part of request object or query object.
        #date_added is created by default by the model system at time of creation of the recipe just like id.
        recipe_to_update.update(mod_data.get('name'),mod_data.get('ingredients'),mod_data.get('instructions'),mod_data.get('serving_size'),mod_data.get('category'),mod_data.get('notes'),datetime.datetime.now())

        #lets test it in insomnia using new put request update_a_recipe. here date modified should take in system date time to reflect the current time of update operation.

        return recipe_to_update


    @recipe_ns.marshal_with(recipe_model)
    @jwt_required()
    def delete(self,id):
        """delete a recipe by id(delete operation)"""
        recipe_to_delete=Recipe.query.get_or_404(id)
        recipe_to_delete.delete()
        # next we test our delete operation in insomnia with a delete_a_recipe DELETE request
        return recipe_to_delete
from flask_restx import Resource,Namespace,fields
from models import User
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import (
create_access_token,create_refresh_token,
get_jwt_identity,
jwt_required)
from flask import Flask,request,jsonify,make_response


auth_ns=Namespace('auth',description="A namespace for our User Authentication")



signup_model=auth_ns.model(
    'SignUp',
    {
        "username":fields.String(),
        "email":fields.String(),
        "password":fields.String()
    }
)


signin_model=auth_ns.model(
    'SignIn',
    {
        'username':fields.String(),
        'password':fields.String()
    }
)

# Creating routes for User LOGIN -> using JWT 
@auth_ns.route('/signup')

class SignUp(Resource):
    # @api.marshal_with(signup_model)
    @auth_ns.expect(signup_model)
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

@auth_ns.route('/signin')

class SignIn(Resource):
    @auth_ns.expect(signin_model)
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

        else:
            return jsonify({"message":"Invalid username or password"})


@auth_ns.route('/refresh')
class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):

        current_user=get_jwt_identity()

        new_access_token=create_access_token(identity=current_user)

        return make_response(jsonify({"access_token":new_access_token}),200)
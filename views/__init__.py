from flask import Blueprint
from flask_restx import Api
import flask_praetorian

# import namespaces
from .owners import api_owner
from .pets import api_pet
from .users import api_user

# one blueprint (Flask) for all the resources
blueprint = Blueprint('PetZilla', __name__)
api = Api(blueprint, title="PetZilla", version="1.0", description="Caring for big pets", doc="/docs")
flask_praetorian.PraetorianError.register_error_handler_with_flask_restx(api_pet)

# every resource in a namespace (RestX)
api.add_namespace(api_user, path='/user')
api.add_namespace(api_pet, path='/pet')
api.add_namespace(api_owner, path='/owner')

from flask import Blueprint
from flask_restx import Api
#import flask_praetorian

# import namespaces
from .users import api_user
from .players import api_player
from .teams import api_team
from .localities import api_location
from .regions import api_region
from .countries import api_country

# one blueprint (Flask) for all the resources
blueprint = Blueprint('PetZilla', __name__)
api = Api(blueprint, title="PetZilla", version="1.0", description="Caring for big pets", doc="/docs")
#flask_praetorian.PraetorianError.register_error_handler_with_flask_restx(api_pet)

# every resource in a namespace (RestX)
api.add_namespace(api_user, path='/user')
api.add_namespace(api_player, path='/player')
api.add_namespace(api_team, path='/team')
api.add_namespace(api_location, path='/location')
api.add_namespace(api_region, path='/region')
api.add_namespace(api_country, path='/country')

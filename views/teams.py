from flask import request
from flask_restx import abort, Resource, Namespace
from model import Team, db, TeamSchema

# namespace declaration
api_team = Namespace("Teams", "Teams management")

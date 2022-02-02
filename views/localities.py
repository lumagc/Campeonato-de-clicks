from flask import request
from flask_restx import abort, Resource, Namespace

from model import Location, db, LocationSchema
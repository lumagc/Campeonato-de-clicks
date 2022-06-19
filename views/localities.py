import flask_praetorian
import sqlalchemy
from flask import request, jsonify
from flask_restx import abort, Resource, Namespace
from model import Location, db, LocationSchema

# namespace declaration
api_location = Namespace("Location", "Location management")

@api_location.route("/<location_id>")
class LocationController(Resource):
    @flask_praetorian.auth_required
    def get(self, location_id):
        location = Location.query.get_or_404(location_id)
        return LocationSchema().dump(location)

    # roles accepted (user with one of these roles)
    @flask_praetorian.roles_accepted("admin", "editor")
    def delete(self, location_id):
        location = Location.query.get_or_404(location_id)
        db.session.delete(location)
        db.session.commit()
        return f"Deleted pet {location_id}", 204

    @flask_praetorian.roles_accepted("admin", "editor")
    def put(self, location_id):
        new_location = LocationSchema().load(request.json)
        if str(new_location.id) != location_id:
            abort(400, "id mismatch")
        db.session.commit()
        return LocationSchema().dump(new_location)


@api_location.route("/")
class LocationListController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        return LocationSchema(many=True).dump(Location.query.all())

    @flask_praetorian.roles_accepted("admin", "editor")
    def post(self):
        location = LocationSchema().load(request.json)
        db.session.add(location)
        db.session.commit()
        return LocationSchema().dump(location), 201

@api_location.route("/points/<location_id>")
class LocationController(Resource):
    @flask_praetorian.auth_required
    def get(self, location_id):
        query = sqlalchemy.text('SELECT L.name, SUM(P.points) AS points FROM player P INNER JOIN location L ON L.id WHERE L.id = ' + location_id + ' GROUP BY L.name')
        data = db.session.execute(query)
        return jsonify({r['name'] : r['points'] for r in data})

@api_location.route("/points/")
class LocationListController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        query = sqlalchemy.text('SELECT L.name, SUM(P.points) AS points FROM player P INNER JOIN location L ON L.id = P.location_id GROUP BY L.name ORDER BY points desc')
        data = db.session.execute(query)
        return jsonify({d['name'] : d['points'] for d in data})
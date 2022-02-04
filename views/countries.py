import flask_praetorian
from flask import request
from flask_restx import abort, Resource, Namespace
from model import Country, db, CountrySchema

# namespace declaration
api_country = Namespace("Countries", "Countries management")

@api_country.route("/<country_id>")
class CountryController(Resource):
    @flask_praetorian.auth_required
    def get(self, country_id):
        country = Country.query.get_or_404(country_id)
        return CountrySchema().dump(country)

    # roles accepted (user with one of these roles)
    @flask_praetorian.roles_accepted("admin", "editor")
    def delete(self, country_id):
        country = Country.query.get_or_404(country_id)
        db.session.delete(country)
        db.session.commit()
        return f"Deleted country {country_id}", 204

    @flask_praetorian.roles_accepted("admin", "editor")
    def put(self, country_id):
        new_country = CountrySchema().load(request.json)
        if str(new_country.id) != country_id:
            abort(400, "id mismatch")
        db.session.commit()
        return CountrySchema().dump(new_country)


@api_country.route("/")
class CountryListController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        return CountrySchema(many=True).dump(Country.query.all())

    @flask_praetorian.roles_accepted("admin", "editor")
    def post(self):
        country = CountrySchema().load(request.json)
        db.session.add(country)
        db.session.commit()
        return CountrySchema().dump(country), 201
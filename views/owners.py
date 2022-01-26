import flask_praetorian
from flask import request
from flask_restx import abort, Resource, Namespace

from model import Owner, db, OwnerSchema

# namespace declaration
api_owner = Namespace("Owners", "Owners management")

# Controller detailed comments in: users.py


@api_owner.route("/<owner_id>")
class OwnerController(Resource):
    @flask_praetorian.auth_required
    def get(self, owner_id):
        owner = Owner.query.get_or_404(owner_id)
        return OwnerSchema().dump(owner)

    @flask_praetorian.roles_accepted("admin", "editor")
    def delete(self, owner_id):
        owner = Owner.query.get_or_404(owner_id)
        db.session.delete(owner)
        db.session.commit()
        return f"Deleted owner {owner_id}", 204

    @flask_praetorian.roles_accepted("admin", "editor")
    def put(self, owner_id):
        new_owner = OwnerSchema().load(request.json)
        if str(new_owner.id) != owner_id:
            abort(400, "id mismatch")
        db.session.commit()
        return OwnerSchema().dump(new_owner)


@api_owner.route("/")
class OwnerListController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        return OwnerSchema(many=True).dump(Owner.query.all())

    @flask_praetorian.roles_accepted("admin", "editor")
    def post(self):
        owner = OwnerSchema().load(request.json)
        db.session.add(owner)
        db.session.commit()
        return OwnerSchema().dump(owner), 201

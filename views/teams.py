import flask_praetorian
from flask import request
from flask_restx import abort, Resource, Namespace
from model import Team, db, TeamSchema

# namespace declaration
api_team = Namespace("Teams", "Teams management")

@api_team.route("/<team_id>")
class TeamController(Resource):
    @flask_praetorian.auth_required
    def get(self, team_id):
        team = Team.query.get_or_404(team_id)
        return TeamSchema().dump(team)

    @flask_praetorian.roles_accepted("admin", "editor")
    def delete(self, team_id):
        team = Team.query.get_or_404(team_id)
        db.session.delete(team)
        db.session.commit()
        return f"Deleted team {team_id}", 204

    @flask_praetorian.roles_accepted("admin", "editor")
    def put(self, team_id):
        new_team = TeamSchema().load(request.json)
        if str(new_team.id) != team_id:
            abort(400, "id mismatch")
        db.session.commit()
        return TeamSchema().dump(new_team)


@api_team.route("/")
class TeamListController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        return TeamSchema(many=True).dump(Team.query.all())

    @flask_praetorian.roles_accepted("admin", "editor")
    def post(self):
        team = TeamSchema().load(request.json)
        db.session.add(team)
        db.session.commit()
        return TeamSchema().dump(team), 201

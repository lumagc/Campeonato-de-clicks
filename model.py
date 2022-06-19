from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy_utils import database_exists

# instantiate SQLAlchemy object
db = SQLAlchemy()


def init_db(app, guard, testing=False):
    """
    Initializes database

    :param app: flask app
    :param guard: praetorian object for password hashing if seeding needed
    """
    db.init_app(app)
    if testing or not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        # if there is no database file
        # migrate model
        db.create_all(app=app)
        # seed data
        seed_db(app, guard)


def seed_db(app, guard):
    """
    Seeds database with test data

    :param app: flask app
    :param guard: praetorian object for password hashing
    """
    # when using app var in function, we need to use app_context
    with app.app_context():
        # lists of model objects for db seed
        roles = [
            Role(name="admin"),
            Role(name="editor"),
            Role(name="user")
        ]
        users = [
            User(username="juan", email="juan@a.a",
                 hashed_password=guard.hash_password("pestillo"),
                 roles=[roles[1]]),
            User(username="maria", email="maria@a.a",
                 hashed_password=guard.hash_password("pestillo"),
                 roles=[roles[0]]),
            User(username="ana", email="ana@a.a",
                 hashed_password=guard.hash_password("pestillo"),
                 roles=[roles[0], roles[1]]),
            User(username="selena", email="selena@a.a",
                 hashed_password=guard.hash_password("pestillo"),
                 roles=[roles[2]]),
            User(username="lual", email="lual@clic.com",
                 hashed_password=guard.hash_password("pestillo"),
                 roles=[roles[0]]),
            User(username="antojo", email="antojo@clic.com",
                 hashed_password=guard.hash_password("pestillo"),
                 roles=[roles[2]]),
        ]

        # Definimos los jugadores
        teams = [
            Team(name="Los pejelagartos"),
            Team(name="Rotísimos")
        ]

        regions = [
            Region(name="Cádiz", country_id=1),
            Region(name="Berlín", country_id=2)
        ]

        localities = [
            Location(name="Chiclana de la Frontera", region_id=1),
            Location(name="Frankfurt", region_id=2)
        ]

        players = [
            Player(name="Lucía Gutiérrez", user=users[4], points=100, location_id=1, teams=[teams[1]]),
            Player(name="Antonio González", user=users[5], points=30, location_id=2, teams=[teams[0]])
        ]

        countries = [
            Country(name="España"),
            Country(name="Alemania")
        ]

        # Añadimos los jugadores, equipos, localidades, regiones y paises definidos en la BD
        for player in players:
            db.session.add(player)
        for team in teams:
            db.session.add(team)
        for location in localities:
            db.session.add(location)
        for region in regions:
            db.session.add(region)
        for country in countries:
            db.session.add(country)

        # commit changes in database
        db.session.commit()


# table for N:M relationship
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
                       )

# table for N:M relationship team to player
teams_players = db.Table('teams_players',
                         db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True),
                         db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True)
                         )


# classes for model entities
class User(db.Model):
    """
    User entity

    Store user data
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # se puede declarar la relación en ambos lados usando backref
    # si se usara back_populates es necesario declararla en ambos lados
    # user = db.relationship("Owner", backref=db.backref("user", uselist=False))

    # from praetorian example
    hashed_password = db.Column(db.Text)
    # M:N relationship
    roles = db.relationship('Role', secondary=roles_users)
    is_active = db.Column(db.Boolean, default=True, server_default="true")

    # this enable this entity as user entity in praetorian
    @property
    def identity(self):
        """
        *Required Attribute or Property*

        flask-praetorian requires that the user class has an ``identity`` instance
        attribute or property that provides the unique id of the user instance
        """
        return self.id

    @property
    def rolenames(self):
        """
        *Required Attribute or Property*

        flask-praetorian requires that the user class has a ``rolenames`` instance
        attribute or property that provides a list of strings that describe the roles
        attached to the user instance
        """
        # try:
        #     return self.roles.split(",")
        # except Exception:
        #     return []
        return [role.name for role in self.roles]

    @property
    def password(self):
        """
        *Required Attribute or Property*

        flask-praetorian requires that the user class has a ``password`` instance
        attribute or property that provides the hashed password assigned to the user
        instance
        """

        return self.hashed_password

    @classmethod
    def lookup(cls, username):
        """
        *Required Method*

        flask-praetorian requires that the user class implements a ``lookup()``
        class method that takes a single ``username`` argument and returns a user
        instance if there is one that matches or ``None`` if there is not.
        """
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id_user):
        """
        *Required Method*

        flask-praetorian requires that the user class implements an ``identify()``
        class method that takes a single ``id`` argument and returns user instance if
        there is one that matches or ``None`` if there is not.
        """
        return cls.query.get(id_user)

    def is_valid(self):
        return self.is_active

    # specify string for repr
    def __repr__(self):
        return f"<User {self.username}>"


class Role(db.Model):
    """
    Role entity

    Store roles data
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return f"<Role {self.name}>"


# Necesitamos el modelo Player para ello creamos su respectiva clase.
class Player(db.Model):
    # Atributos de player
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # Esta parte nola entiendo, creo que por la relacion user player.
    user = db.relationship("User", backref=db.backref("player", uselist=False))

    # M:1 player-location
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship("Location", backref="Player")

    # M:N relationship
    teams = db.relationship('Team', secondary=teams_players)
    is_active = db.Column(db.Boolean, default=True, server_default="true")

    def __repr__(self):
        return f"<User {self.name}"


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return f"<User {self.name}"


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)

    # M:1 location-region
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    region = db.relationship("Region", backref="Location")

    def __repr__(self):
        return f"<User {self.name}"


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)

    # M:1 region-country
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    country = db.relationship("Country", backref="Region")

    def __repr__(self):
        return f"<User {self.name}"


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return f"<User {self.name}"


# Marshmallow schemas definition
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        # model class for the schema
        model = User
        include_relationships = True
        load_instance = True
        sqla_session = db.session


class PlayerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Player
        include_relationships = True
        load_instance = True
        sqla_session = db.session


class TeamSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Team
        include_relationships = True
        load_instance = True
        sqla_session = db.session


class LocationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        include_relationships = True
        load_instance = True
        sqla_session = db.session


class RegionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Region
        include_relationships = True
        load_instance = True
        sqla_session = db.session


class CountrySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Country
        include_relationships = True
        load_instance = True
        sqla_session = db.session


class RoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        include_relationships = True
        load_instance = True
        sqla_session = db.session

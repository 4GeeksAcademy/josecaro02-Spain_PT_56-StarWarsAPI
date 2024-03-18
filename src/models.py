from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__  = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        #return '<User %r>' % self.email
        return f"Usuario con id {self.id} y email: {self.email}"

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "password": self.password
            # do not serialize the password, its a security breach
        }
    
class Planets(db.Model):
    __tablename__= 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return "Planeta {} de nombre {}".format(self.id, self.name)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    
class Favorite_Planets(db.Model):
    __tablename__ = 'favorite_planets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_relationship = db.relationship(User)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)
    planet_relationship = db.relationship(Planets)

    def __repr__(self):
        return "Al usuario {} le gusta el planeta {}".format(self.user_id, self.planet_id)
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }

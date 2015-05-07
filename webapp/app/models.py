from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db
from . import login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), unique=True)

    password_hash = db.Column(db.String(128))

    # org_id = db.Column(db.Integer, db.ForeignKey('orgs.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Customer:email %r>' % self.email


# class Organization(db.Model):
#     __tablename__ = 'orgs'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128))
#     province = db.Column(db.String(128))
# 
#     customers = db.relationship('Customer', backref='org', lazy='dynamic')
#     tests = db.relationship('Test', backref='org', lazy='dynamic')
# 
#     def __repr__(self):
#         return '<Organization %r>' % self.name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from shop import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

cart = db.Table('cart',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True),
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    cart = db.relationship("Item", secondary=cart)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}')"  

    @property
    def password(self):
        raise AttributeError('Password is not readable.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship("Category")
    description = db.Column(db.Text, nullable=False)
    picture = db.Column(db.String(100), nullable=False, default='default.jpg')
    price = db.Column(db.Integer, nullable=False)
    carbon = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Item('{self.id}', '{self.name}')"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, nullable=False)

    def __repr__(self):
        return f"Category('{self.id}', '{self.name}')"

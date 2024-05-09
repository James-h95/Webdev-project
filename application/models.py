from application import db, login
from application import bcrypt
from flask_login import UserMixin

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Association table
users_items = db.Table('users_items',
    db.Column('user_id',db.Integer(),db.ForeignKey('user.id')),
    db.Column('item_id',db.Integer(),db.ForeignKey('item.id')),                
    )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username =db.Column(db.String(length=30),nullable=False,unique=True)
    email_address = db.Column(db.String(length=50),nullable=True,unique=True)
    _password = db.Column(db.String(length=60), nullable=False) #avoid naming confusion
    balance = db.Column(db.Integer(),nullable=False,default=10)
    items = db.relationship('Item',secondary=users_items, back_populates='users',lazy='dynamic')

    @property
    #GETTER
    def password(self):
        return self.password
    
    #SETTER
    @password.setter
    def password(self,plain_password):
        self._password = bcrypt.generate_password_hash(plain_password)
    
    def check_password(self,given_password):
        return bcrypt.check_password_hash(self._password, given_password)

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30),nullable=False,unique=True)
    price = db.Column(db.Integer(),nullable=False)
    rarity = db.Column(db.String(length=30),nullable=False)
    users = db.relationship('User',secondary=users_items, back_populates="items",lazy='dynamic')
    
    #def __repr__(self):
        #return f'Item {self.name}'
    

class Message(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    sender_id = db.Column(db.Integer(), primary_key=True)
    receiver_id = db.Column(db.Integer(), primary_key=True)
    time = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(length=200),nullable=False,unique=True)
    
    def __reprr__(self):
        return f'Message: {self.text}'
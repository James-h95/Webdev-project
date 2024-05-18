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
    
    def can_purchase(self,item_obj):
        return self.balance >= item_obj.price

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30),nullable=False,unique=True)
    price = db.Column(db.Integer(),nullable=False)
    #rarity = db.Column(db.String(length=30))
    users = db.relationship('User',secondary=users_items, back_populates="items",lazy='dynamic')
    
    def buy(self,user_obj):
        self.users.append(user_obj) # Assign ownership to user who buys
        user_obj.balance -= self.price
        db.session.add(user_obj)
        db.session.add(self)
        db.session.commit()
        print(f"User {user_obj.username} bought item {self.name}")
    
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
    
# Game association table
# 1 user [plays] M games M [made by] 1 user
# 1 game [made by] 1 user

users_games = db.Table('users_games_played', 
    db.Column('user_id', db.Integer(),db.ForeignKey('user.id')),
    db.Column('game_id', db.Integer(),db.ForeignKey('game.id')),
    db.Column('time', db.Integer()),
    db.Column('comment', db.String(length=200))
    )    

class Game(db.Model):
     id = db.Column(db.Integer(), primary_key=True)
     creator = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
     phrase = db.Column(db.String(length=250),nullable=False)
     category = db.Column(db.String(length=10),nullable=False)
     timeLimit = db.Column(db.Integer(),nullable=False)
     caption = db.Column(db.String(length=200))
     created = db.Column(db.DateTime(timezone=True))
     times_played = db.Column(db.Integer())
     successes = db.Column(db.Integer())
     
    
     
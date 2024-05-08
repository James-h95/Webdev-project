from application import db

#Association table
users_items = db.Table('users_items',
    db.Column('user_id',db.Integer(),db.ForeignKey('user.id')),
    db.Column('item_id',db.Integer(),db.ForeignKey('item.id')),                
    )

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username =db.Column(db.String(length=30),nullable=False,unique=True)
    email_address = db.Column(db.String(length=50),nullable=False,unique=True)
    password = db.Column(db.String(length=60), nullable=False)
    balance = db.Column(db.Integer(),nullable=False,default=10)
    items = db.relationship('Item',secondary=users_items, back_populates='users',lazy='dynamic')

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
     
    
     
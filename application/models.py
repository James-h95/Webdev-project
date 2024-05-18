from application import db, login
from application import bcrypt
from flask_login import UserMixin

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Association table for many-to many relationship
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
    games_created = db.relationship('Game', back_populates='creator')
    games_played = db.relationship('UserGames', back_populates='user')

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
    sender_id = db.Column(db.Integer())
    receiver_id = db.Column(db.Integer())
    time = db.Column(db.Integer())
    text = db.Column(db.String(length=200))
    for_all = db.Column(db.NUMERIC)
    
    def __reprr__(self):
        return f"""sender_id={self.sender_id},
                   receiver_id={self.receiver_id},
                   time={self.time},
                   text={self.text},
                   for_all={self.for_all}
                """
    
# Game association table
# 1 user [plays] M games M [made by] 1 user
# 1 game [made by] 1 user

class Game(db.Model):
     id = db.Column(db.Integer(), primary_key=True)
     phrase = db.Column(db.String(length=250),nullable=False)
     category = db.Column(db.String(length=10),nullable=False)
     timeLimit = db.Column(db.Integer(),nullable=False)
     caption = db.Column(db.String(length=200))
     created = db.Column(db.DateTime(timezone=True))
     times_played = db.Column(db.Integer())
     successes = db.Column(db.Integer())
     creator_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
     creator = db.relationship('User', back_populates='games_created')
     users_played = db.relationship('UserGames', back_populates='game')
    
    
class UserGames(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(),db.ForeignKey('user.id'),nullable=False)
    game_id = db.Column(db.Integer(),db.ForeignKey('game.id'),nullable=False)
    success = db.Column(db.Integer(),nullable=False)
    
    user = db.relationship('User', back_populates='games_played')
    game = db.relationship('Game', back_populates='users_played')
     
    
     
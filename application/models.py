from application import db, login
from application import bcrypt
from flask_login import UserMixin

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Association table for many-to many relationship with users and items
users_items = db.Table('users_items',
    db.Column('user_id',db.Integer(),db.ForeignKey('user.id')),
    db.Column('item_id',db.Integer(),db.ForeignKey('item.id')),                
)

# User database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username =db.Column(db.String(length=30),nullable=False,unique=True)
    _password = db.Column(db.String(length=60), nullable=False) #avoid naming confusion
    balance = db.Column(db.Integer(),nullable=False,default=10)
    items = db.relationship('Item',secondary=users_items, back_populates='users',lazy='dynamic')
    games_created = db.relationship('Game', back_populates='creator')
    games_played = db.relationship('UserGames', back_populates='user')
    # Default avatar upon registration
    avatar_url = db.Column(db.String(200), default='https://i.pinimg.com/originals/e8/61/d4/e861d4843751b4daf463aa78a356bab1.jpg')

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
    
    def set_avatar(self, avatar_url):
        self.avatar_url = avatar_url
        db.session.commit()
        
# Stores items, price, and URL to assign avatars to users 
class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30),nullable=False,unique=True)
    price = db.Column(db.Integer(),nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    users = db.relationship('User',secondary=users_items, back_populates="items",lazy='dynamic')
    
    
    def buy(self,user_obj):
        self.users.append(user_obj) # Assign ownership to user who buys
        user_obj.balance -= self.price
        db.session.add(user_obj)
        db.session.add(self)
        db.session.commit()
        print(f"User {user_obj.username} bought item {self.name}")
        
# Utility function
# Items we have set to be sold in shop, will update over time
def create_items():
    items = [{'name':'Book worm','price':5,'image_url':'https://i.pinimg.com/originals/54/ba/4b/54ba4b946c7866fec64f7221324ce4b9.jpg'},
             {'name':'Demon','price':4,'image_url':'https://i.pinimg.com/originals/5b/0a/9b/5b0a9b71f215c5032fefb6ddcf15129f.jpg'},
             {'name':'Rainbow', 'price':20,'image_url':'https://i.pinimg.com/236x/80/bf/f3/80bff3773b35680ea28d918909dcc3c7.jpg'},
             {'name': 'Pink swag', 'price':100,'image_url':'https://i.pinimg.com/564x/2c/0e/36/2c0e3682a3e9535debd8a688f133b9ed.jpg'},
             {'name': 'Icecream', 'price':120,'image_url':'https://i.pinimg.com/564x/c9/1f/02/c91f0272ffef7f49e380bb9caf19b2b6.jpg'},
             {'name': 'Tunes', 'price':150, 'image_url':'https://i.pinimg.com/564x/91/7a/bf/917abf179cada8fae95f6e73e12c515a.jpg'},
             {'name': 'Chef gourmet','price':200,'image_url':'https://i.pinimg.com/564x/8c/62/62/8c6262e9ade593eb4150c950df508d73.jpg'},
             {'name': 'Zzzzzz', 'price':500,'image_url':'https://i.pinimg.com/564x/70/2c/bf/702cbf852e9e39da5609e5e2887daa83.jpg'}
             ]
    
    for x in items:
        item = Item.query.filter_by(name=x['name']).first() #check if exists
        if not item:
            new_item = Item(name=x['name'],price=x['price'],image_url=x['image_url'])
            db.session.add(new_item)
    
    db.session.commit()

# Stores instance of message in DB and whether the message was direct or global
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

# Stores game in DB with relevant stats which could be implemented
# Links to user via creator and users that have played the game
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
    
# Relational table for users who have played games, saves their result
# 1 = solved puzzle
# 0 = failed puzzle  
class UserGames(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(),db.ForeignKey('user.id'),nullable=False)
    game_id = db.Column(db.Integer(),db.ForeignKey('game.id'),nullable=False)
    success = db.Column(db.Integer(),nullable=False)
    
    user = db.relationship('User', back_populates='games_played')
    game = db.relationship('Game', back_populates='users_played')
     
    
     
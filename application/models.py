from application import db

class User(db.Model):
    id = db.column(db.String(length=30),nullable=False,unique=True)
    username =db.Column(db.String(length=30),nullable=False,unique=True)
    email_address = db.column(db.String(length=50),nullable=False,unique=True)
    password = db.Column(db.String(length=60), nullable=False)
    balance = db.Column(db.Integer(),nullable=False,default=10)
    items = db.relationship('Item',backref='owner',lazy=true)

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30),nullable=False,unique=True)
    price = db.Column(db.Integer(),nullable=False)
    rarity = db.Column(db.String(length=30),nullable=False)
    owner = db.Column(db.Integer(),db.ForeignKey('user.id'))
    
    def __reprr__(self):
        return f'Item {self.name}'
    

class Message(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    sender_id = db.Column(db.Integer(), primary_key=True)
    receiver_id = db.Column(db.Integer(), primary_key=True)
    time = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(length=200),nullable=False,unique=True)
    
    def __reprr__(self):
        return f'Message: {self.text}'
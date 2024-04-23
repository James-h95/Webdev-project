from application import db
class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30),nullable=False,unique=True)
    price = db.Column(db.Integer(),nullable=False)
    rarity = db.Column(db.String(length=30),nullable=False)
    
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
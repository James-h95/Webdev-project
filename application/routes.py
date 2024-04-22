from application import app
from flask import render_template
from application.models import Item  

@app.route('/')
@app.route('/home')
def landing_page():
    return render_template('home.html')

# Flask APP initialisation. Our Python package
@app.route('/shop')
def shop_page():
    # Example dictionaries to use
    '''items=[{'id':1,'name':'Simple badge','price':60, 'rarity':"Common"},
        {'id':2,'name':'Black Judo belt','price':150, 'rarity':"Rare"},
        {'id':3,'name':'Shiny star','price':300, 'rarity':"Legendary"}
        ]'''
    items = Item.query.all()
    return render_template('shop.html',items=items)



@app.route('/chat')
def play_page():
    return render_template('chat.html')
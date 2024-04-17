# Flask APP initialisation. Our Python package

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def landing_page():
    return render_template('home.html')

# Flask APP initialisation. Our Python package
@app.route('/shop')
def shop_page():
    # Example dictionaries to use
    items=[{'id':1,'name':'Simple badge','price':60, 'rarity':"Common"},
        {'id':2,'name':'Black Judo belt','price':150, 'rarity':"Rare"},
        {'id':3,'name':'Shiny star','price':300, 'rarity':"Legendary"}
        ]
        
    return render_template('shop.html',items=items)



@app.route('/chat')
def play_page():
    return render_template('chat.html')


# Checks if flask_app.py file has executed directly and not imported
if __name__ == '__main__':
    app.run(debug=True)
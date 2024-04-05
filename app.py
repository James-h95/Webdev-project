# Flask APP initialisation. Our Python package

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('landing.html')

# Flask APP initialisation. Our Python package
@app.route('/shop')
def shop_page():
    #items=[{'id':1,'name':'Cool badge','price':60},
          # {'id':2,'name':'Rare badge','price':150},
           #{'id':3,'name':'Premium badge','price':300}
           #]
    return render_template('shop.html',items=items)



# Work on Flask to make the chat
@app.route('/chat')
def play_page():
    return render_template('chat.html')


# Checks if flask_app.py file has executed directly and not imported
if __name__ == '__main__':
    app.run(debug=True)
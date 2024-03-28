# Flask APP initialisation. Our Python package

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('landing.html')

# Flask APP initialisation. Our Python package

# Checks if flask_app.py file has executed directly and not imported
if __name__ == '__main__':
    app.run(debug=True)
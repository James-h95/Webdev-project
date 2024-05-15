from application import app

#checks if run.py file execute directly
if __name__ == '__main__':
    app.run(debug=True, port=5000)
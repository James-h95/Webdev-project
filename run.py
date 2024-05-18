from application import create_app
from application.models import db,Item,User,Game

app = create_app()

# from application.models import db,Item,User,Game
#with app.app_context():
#     db.drop_all() 
#     db.create_all()
#     db.session.commit()



#checks if run.py file execute directly
if __name__ == '__main__':
    app.run(debug=True, port=5000)
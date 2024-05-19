from application import create_app, db
from application.models import Item, users_items,User,Game,UserGames,Message, create_items

app = create_app()



with app.app_context():
    db.create_all() # ensure all tables created
    create_items()





#checks if run.py file execute directly
if __name__ == '__main__':
    app.run(debug=True, port=4000)
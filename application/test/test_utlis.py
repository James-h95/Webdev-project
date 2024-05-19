# application/tests/test_utils.py

from application.models import db, User, Game
import datetime

def add_test_data_to_db():
    # Add test users
    user1 = User(username='testuser1', password='password1')
    user2 = User(username='testuser2', password='password2')

    # Add test games
    game1 = Game(phrase='testphrase1', category='history', creator=user1, timeLimit=60, caption='testcaption1', created=datetime.datetime.now())
    game2 = Game(phrase='testphrase2', category='sports', creator=user2, timeLimit=90, caption='testcaption2', created=datetime.datetime.now())

    db.session.add_all([user1, user2, game1, game2])
    db.session.commit()

"""
file to add tests
"""
import unittest
from unittest import TestCase
from application import create_app, db
from application.models import User, Game, UserGames
from application.config import Config
from application.test.test_utlis import add_test_data_to_db


class TestConfig(Config):
  TESTING = True
  DEBUG = True
  SQLALCHEMY_DATABASE_URI =  'sqlite:///:memory:'
  WTF_CSRF_ENABLED = False

class test_run(unittest.TestCase):
  # set up method to initialise test enviornment
  def setUp(self):
    testApp = create_app(config=TestConfig) #create app instance with TestConfig
    self.app_context = testApp.app_context()
    self.app_context.push()
    db.create_all()
    add_test_data_to_db()
  
  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()
  
  # test user creaion
  def test_user_creation(self):
    self.assertEqual(User.query.count(),2) # tests if there are 2 users (as in test db)
    self.assertEqual(User.query.first().username, 'testuser1') # test user's username is as expected
  
  # test game creation
  def test_game_creation(self):
    self.assertEqual(Game.query.count(), 2) # test there are two games created
    self.assertEqual(Game.query.first().phrase, 'testphrase1') # test first game phrase is as expencted
  
  # test password hashing
  def test_password_hashing(self):
    user = User.query.first()
    self.assertTrue(user.check_password('password1'))  # Check correct password
    self.assertFalse(user.check_password('wrongpassword'))  # Check incorrect password
  # Test playing a game and winning
  def test_play_game_win(self):
      user = User.query.filter_by(username='testuser1').first()
      game = Game.query.filter_by(phrase='testphrase1').first()
      
      playInstance = UserGames(user_id=user.id, game_id=game.id, success=1)
      db.session.add(playInstance)
      db.session.commit()

      user_game = UserGames.query.filter_by(user_id=user.id, game_id=game.id).first()
      self.assertEqual(user_game.success, 1)  # Verify success is 1
   # Test playing a game and losing
  def test_play_game_lose(self):
      user = User.query.filter_by(username='testuser2').first()
      game = Game.query.filter_by(phrase='testphrase2').first()
      
      playInstance = UserGames(user_id=user.id, game_id=game.id, success=0)
      db.session.add(playInstance)
      db.session.commit()

      user_game = UserGames.query.filter_by(user_id=user.id, game_id=game.id).first()
      self.assertEqual(user_game.success, 0)  # Verify success is 0

  
if __name__ == "__main__":
  unittest.main()






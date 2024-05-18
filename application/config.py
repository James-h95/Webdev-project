"""
this file contains configuration settings for Flask
"""
import os

# gets directory name of current file 
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
  SECRET_KEY  = os.environ.get('SECRET_KEY') or '290429d88cc03bbf9526fc4e'
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'hangman.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  DEBUG = False





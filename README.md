# CITS3403 Project - Let's Hang!
## Group members: 
- Aaminah Irfan - 23642166
- Carly Scott - 23359926
- Joshua Mance - 23420013
- James Hudibyo - 23452945
  
## Instructions to run: 
The following python code should be run in the terminal to set up the database:

from application.models import db, Item, User, Game, Message, UserGames
from application import app
with app.app_context():
    db.drop_all() 
    db.create_all()

Users and posts can then be created via the website using register/login 
  
## References: 
- ChatGPT
- Geeks4Geeks
- Stack Overflow
 



  

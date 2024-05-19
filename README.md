# CITS3403 Project - Let's Hang!
## Group members: 
| Name          | Student Number | Github User |
|---------------|----------------|-------------|
| Aaminah Irfan | 23642166       | aaminah06   |
| Carly Scott   | 23359926       | carlymayyy  |
| Joshua Mance  | 23420013       | Josh Mance  |
| James Hudibyo | 23452945       | James-h95   |

## Project Rundown
Let's Hang© is a dynamic site that brings to life the paper-and-pen game of hangman! Users have the opportunity to create their own games, play games created by other users, and compete for the top spot on the coveted leaderboard. Games award coins which can be used to purchase cool, upgraded avatars, incentivising continued gameplay. Users also have access to a chat feature to talk with fellow players between games. The main features of the site include:

. Login/register options to create an account, supported by a profile page detailing the user's personal stats such as the number of games they've created, their total number of games solved, and their favourite category to play.

. A feed page complete with chat pop-up that can be perused for games. Users can play as much as they want - as long as they are not the game creator and haven't played the game before. Users can also view the past plays for each game to see how other users did.

. A create page to make your own games by choosing a category, setting a word/phrase to be guessed, setting a time limit, and including a caption to be displayed on the feed (optional). Users post games which immediately go live on the feed.

. Games lead to a hangman page which presents gameplay in a fun, animated environment. Users must beat the clock to solve the word in order to win 10 coins.

. Coins can be spent freely in the site shop which offers customisations for users' avatars. Users' avatars will show in the feed above games they create.

. The leaderboard page keeps track of site-wide activity and ranks users by their numbers of successes as they vie for a top-20 spot.
  
## Instructions to run: 
Ensure all necessary packages are installed according to requirements.txt. The following python code should be run in the terminal to set up the database:

py // establishes python terminal
from application.models import db, Item, User, Game, Message, UserGames
from application import create_app
with app.app_context():
    db.drop_all()
    db.create_all()

Then the following can be run to launch the app in the Flask environment:

py run.py

Users and posts can then be created via the website using register/login. The chat is fully interactive and can be examined simultaneously from separate ports. 

## Testing instructions:

Tests are divided into **unit tests** and **web-based tests** using Selenium WebDriver.

**Running Unit Tests**
Our unit tests are written in Python using the unittest framework. These tests cover the basic functionalities of the models and routes within the application.

To run the unit tests, navigate to the project directory in your terminal and execute the following command:
```
python -m unittest discover -s application/test -p "unit.py"
```
**Running Web Tests with Selenium WebDriver**
The web tests use Selenium WebDriver to simulate user interactions with the web application. Before running these tests, ensure you have the necessary browser drivers installed and the selenium package added to your project.

To run the Selenium WebDriver tests, use the following command:
```
python -m unittest discover -s test -p "test_web.py"
```
**Prerequisites for Selenium Tests:**
Ensure you have selenium installed:

 pip install selenium

Notes
- It's recommended to run the tests in a development or staging environment as they can modify the database state.
- For Selenium tests, ensure your application server is running if it's not set up to start within the test scripts.
  
## Code references: 
- ChatGPT
- Geeks4Geeks
- Stack Overflow
- Flask Mega-Tutorial 
- CITS3403 Agile Web demos and lectures
- W3Schools

## Image references:
- Sticky note: https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGnsBpXkmSbxYJWYUvxJqnFrrYbst8AETf8NpJDz3W5w&s
- Profile images: https://i.pinimg.com/564x/f2/7a/80/f27a80460711f70cb2e7b94acec253ee.jpg





  

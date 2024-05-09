from application import app,db
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request, jsonify
from operator import attrgetter
import json
from application.models import Item, User, Message, Game
from application.forms import RegisterForm, CreateGameForm

NUM_VISIBLE_MESSAGES = 50

# -----------------------------------------------------
# This temporary and used for testing. A random id in 
# the range 0-99 is created to mimic a users id
from random import randint
USER_ID = randint(1, 1_000_000) % 100
# -----------------------------------------------------

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

# Flask APP initialisation. Our Python package
@app.route('/shop')
def shop_page():
    # Example dictionaries to use
    '''items=[{'id':1,'name':'Simple badge','price':60, 'rarity':"Common"},
        {'id':2,'name':'Black Judo belt','price':150, 'rarity':"Rare"},
        {'id':3,'name':'Shiny star','price':300, 'rarity':"Legendary"}
        ]'''
    items = Item.query.all()
    return render_template('shop.html',items=items)

@app.route('/feed', methods=['GET', 'POST'])
def feed_page():

    # Handling all GET requests. Tasks common to all GET
    # requests are handled first, and then the request 
    # arguments are checked to determine which specific actions
    # should be performed, as well as what the output will be.
    if request.method == "GET":

        # load the previous messages in order of their timestamp value
        all_messages = Message.query.all()
        all_messages.sort(reverse = True, key=attrgetter("time"))
        
        visible_messages = []
        # iterating through all messages, filling the visible messages list
        # with only messages to or for the the current user
        for row in all_messages:
                if  (len(visible_messages) >= NUM_VISIBLE_MESSAGES):
                    break
                elif row is not None:
                    message = {}
                    # If the message was sent by the user
                    if (row.sender_id == USER_ID):
                        message["type"] = "sent"
                        
                    # Else if the message was sent to @all chat
                    # by a different user
                    elif (row.for_all == True):
                         message["type"] = "received"

                    # If either of the two above conditions are met
                    if len(message) != 0:
                        message["text"] = row.text
                        message["time"] = row.time
                        visible_messages.append(message)

        # Showing oldest messages first
        visible_messages.reverse()

        # Used example from https://www.geeksforgeeks.org/flask-http-method/
        # to understand request arguments    
        
        # Returning most recent messages
        if request.args.get("request_type") == "update_query":
            update_required = (len(visible_messages) > 0)
            return {"USER_ID":USER_ID,
                    "update_required":update_required,
                    "visible_messages":visible_messages}
        
        else:
            # Loading the page
            return render_template('feed.html', USER_ID = USER_ID,
                                visible_messages = visible_messages)

    # If a post request is received, adding the new message to the database
    elif request.method == "POST":
        data = request.form
        message = Message()

        # Setting the variables of a new message object
        message.sender_id = int(data["sender_id"])
        message.receiver_id = str(data["receiver_id"])
        message.time = int(data["time"])
        message.text = str(data["text"])
        message.for_all = bool(data["for_all"])
        
        # Adding this new message object to the database
        db.session.add(message)
        db.session.commit()

        # Informing the client that adding the new message was successful 
        return jsonify("success")
    

@app.route('/create', methods=['GET', 'POST'])
def create_page():
    form = CreateGameForm()
    if form.validate_on_submit():
        new_game = Game(phrase=form.phrase.data,category=form.category.data,timeLimit=form.timeLimit.data,caption=form.caption.data)
        db.session.add(new_game)
        db.session.commit()
        flash("Game is now live!")
        return redirect(url_for('feed_page'))
    return render_template('create.html', form=form)


@app.route('/leaderboard')
def leaderboard_page():
    return render_template('leaderboard.html')

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,password=form.password1.data) # directly uses password data
        db.session.add(new_user)
        db.session.commit()
        flash("New user added!",new_user.username)
        return redirect(url_for('shop_page'))
    #Check if any validations fail
    if form.errors != {}:
        for err_msg in form.errors.values():
           flash(f'There was an error with creating a user: {err_msg}') 
    return render_template('register.html',form=form)
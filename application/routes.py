from flask import Blueprint
from application import models, routes, db
from flask import render_template, redirect, url_for, flash, request,jsonify
from sqlalchemy import desc, func
from application.models import Item, User, Message, Game, UserGames
from application.forms import RegisterForm, CreateGameForm,LoginForm, PurchaseItemForm
from operator import attrgetter
from flask_login import login_user, logout_user, login_required,current_user
import datetime
import json

main = Blueprint('main', __name__)

NUM_VISIBLE_MESSAGES = 50

@main.route('/')
@main.route('/home')
def home_page():
    return render_template('home.html')

# Flask APP initialisation. Our Python package
@main.route('/shop,',methods=['GET','POST'])
@login_required
def shop_page():
    # Example dictionaries to use
    '''items=[{'id':1,'name':'Simple badge','price':60, 'rarity':"Common"},
        {'id':2,'name':'Black Judo belt','price':150, 'rarity':"Rare"},
        {'id':3,'name':'Shiny star','price':300, 'rarity':"Legendary"}
        ]'''
    form = PurchaseItemForm()
    if request.method == "POST":
        # Purchase Item logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object: # if not null, apply ownership
            if current_user.can_purchase(p_item_object): # Verify curr user can afford it
                p_item_object.buy(current_user)
                #response['success'] = True
                #response['new_balance'] = current_user.balance  # Include new balance
                #response['message'] = f"Congratulations, you purchased {p_item_object.name} for ${p_item_object.price}!"
                #flash(response['message'], category='success')
                #print("Purchase successful")  # Debugging statement
                flash(f"Congratulations, you purchased {p_item_object.name} for ${p_item_object.price}!",category='success')
            else:
                #response['message'] = f"Unfortunately, you don't have enough money to purchase the {p_item_object.name}!"
                #flash(response['message'], category='danger')
                flash(f"Unfortunately, you don't have enough money to purchase the {p_item_object.name}!",category='danger')
                #print("Insufficient balance")  # Debugging statement
        else:
            print("Item not found")
            flash("Item not found!", category='danger')
        #return jsonify(response)
    items = Item.query.all()
    purchased_items = [item.name for item in current_user.items]
    return render_template('shop2.html',items=items, form=form,purchased_items=purchased_items)


@main.route('/equip_avatar', methods=['POST'])
@login_required
def equip_avatar():
    equip_item = request.form.get('equip_item')
    item = Item.query.filter_by(name=equip_item).first()
    if item and item in current_user.items:
        # Logic to equip the item as the user's avatar
        current_user.set_avatar(item.image_url)
        flash(f"{item.name} has been equipped as your avatar!", category='success')
    else:
        flash("Item not found or not owned by the user.", category='danger')
    return redirect(url_for('main.shop_page'))


@main.route('/feed', methods=['GET', 'POST'])
@login_required
def feed_page():
    already_played = [user_game for user_game in current_user.games_played]

    user_id = current_user.get_id()
    games = Game.query.order_by(desc(Game.created)).all()
    
    # Handling all GET requests. Tasks common to all GET
    # requests are handled first, and then the request 
    # arguments are checked to determine which specific actions
    # should be performed, as well as what the output will be.
    if request.method == "GET":

        # Info requests 

        # Returning all friend names.
        # Note: will need to restrict this to only friends
        if request.args.get("request_type") == "get_friends":
            friend_names = [user.username for user in User.query.all()]
            return {"friend_names":friend_names}
        
        if request.args.get("request_type") == "get_friend_id":
            username = request.args.get("username")
            for user in User.query.all():
                if user.username == username:
                    return {"id":user.id+1}


        else:

            # If the GET request is the page loading, then the default 
            # target user id is 0, i.e. the "all" chat
            returned_target_id_val = request.args.get("target_user_id")
            if returned_target_id_val  == None:
                target_user_id = 0
            else:
                target_user_id = int(returned_target_id_val)



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

                        # If the user is sending to the "all" chat
                        if target_user_id == 0:

                            # If the message was sent by the user
                            print(user_id, row.sender_id, row.text)
                            if (int(row.sender_id) == int(user_id)):
                                message["type"] = "sent"
                                
                                message["text"] = row.text
                                message["time"] = row.time
                                visible_messages.append(message)
                                
                            # Else if the message was sent to @all chat
                            # by a different user

            
                            elif (int(row.for_all) == 1):
                                message["type"] = "received"
                                
                                message["text"] = row.text
                                message["time"] = row.time
                                visible_messages.append(message)

                        # Otherwise, if the user is sending to a single user
                        else:
                            # If the message was sent by the user
                            if (int(row.sender_id) == int(user_id)):
                                if (int(row.receiver_id) == int(target_user_id)):
                                    message["type"] = "sent"
                                    
                                    message["text"] = row.text
                                    message["time"] = row.time
                                    visible_messages.append(message)
                                
                            # Else if the target user sent the message to the user
                            elif (int(row.receiver_id) == int(user_id)):
                                if (int(row.sender_id) == int(target_user_id)):
                                    message["type"] = "received"
                                    
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
            return {"user_id":user_id,
                    "update_required":update_required,
                    "visible_messages":visible_messages}
        
        # Returning all friend names.
        # Note: will need to restrict this to only friends
        elif request.args.get("request_type") == "get_friends":
            friend_names = [user.username for user in User.query.all()]
            return {"friend_names":friend_names}
        
        else:
            # Loading the page
            return render_template('feed.html', user_id = user_id,
                                visible_messages = visible_messages,
                                games=games, already_played=already_played)

    # If a post request is received, adding the new message to the database
    elif request.method == "POST":

        data = request.form

        print(data)
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

@main.route('/gameHistory/<int:game_id>')
def get_history(game_id):
    game_history = UserGames.query.filter_by(game_id=game_id).all()
    return jsonify(game_history=[{
        'username':gameHist.user.username,
        'success': gameHist.success} for gameHist in game_history])

@main.route('/chat')
def play_page():
    messages = Message.query.all()
    return render_template('chat.html')

@main.route('/create', methods=['GET', 'POST'])
def create_page():
    form = CreateGameForm()
    if form.validate_on_submit():
        date = datetime.datetime.now()
        new_game = Game(creator_id=current_user.id, phrase=form.phrase.data,category=form.category.data,timeLimit=form.timeLimit.data,caption=form.caption.data,created=date,times_played=0,successes=0)
        db.session.add(new_game)
        db.session.commit()
        flash("Game is now live!",category="success")
        return redirect(url_for('main.feed_page'))
    return render_template('create.html', form=form)

@main.route('/hangman/<int:game_id>', methods=['GET'])
def hangman_page(game_id):
    current_game = Game.query.get(game_id)
    user = User.query.get(current_user.id)
    return render_template('hangman.html', current_game=current_game, user=user)

@main.route('/save', methods=['POST'])
def save_play():
    data = request.json
    uid = data.get('user_id')
    gid = data.get('game_id')
    ss = data.get('success')
    game = Game.query.get(gid)
    playInstance = UserGames(user_id=uid, game_id=gid, success=ss)
    if ss == True:
        user = User.query.get(current_user.id)
        user.balance += 10
        game.successes += 1
    game.times_played += 1

    db.session.add(playInstance)
    db.session.commit()
    
    return jsonify({"message": "Success"})

@main.route('/leaderboard', methods=['GET'])
def leaderboard_page():
    successes = func.sum(UserGames.success)
    ordered_table = db.session.query(User.username.label('Username'), successes.label('Successes')).join(UserGames, User.id == UserGames.user_id).group_by(User.username).order_by(successes.desc()).all()
    return render_template('leaderboard.html', ordered_table=ordered_table)

@main.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,password=form.password1.data) # directly uses password data
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f"Account created! Welcome, {new_user.username}",category='success')
        
        return redirect(url_for('main.shop_page'))
    
    #Check if any validations fail
    if form.errors != {}:
        for err_msg in form.errors.values():
           flash(f'There was an error with creating a user: {err_msg}',category='danger') 
    return render_template('register.html',form=form)

@main.route('/login',methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # If user not None
        if user and user.check_password(given_password=form.password.data):
            login_user(user)
            flash(f"You have logged in! Welcome back, {user.username}",category='success')
            return redirect(url_for('main.shop_page'))
        # If user or password none
        else:
            flash('Invalid username or password. Try again',category='danger')
    return render_template('login.html',form=form)

@main.route('/logout')
def logout_page():
    logout_user()
    flash("You have logged out!",category='info')
    return redirect(url_for("main.home_page"))

# profile page
@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    user = current_user
    games_created = Game.query.filter_by(creator_id = user.id).count()
    successes = func.sum(UserGames.success)
    game_success = db.session.query(successes).filter(UserGames.user_id == user.id).scalar() or 0
    category_made_counts = db.session.query(Game.category, func.count(UserGames.game_id)).join(UserGames, Game.id == UserGames.game_id).filter(UserGames.user_id == user.id).group_by(Game.category).all()
    favourite_category = max(category_made_counts, key=lambda x: x[1])[0] if category_made_counts else "TBD!"
    return render_template('profile.html', user = user, games_created = games_created, game_success=game_success, favourite_category=favourite_category)
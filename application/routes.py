from application import app,db
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from application.models import Item, User, Message, Game
from application.forms import RegisterForm, CreateGameForm,LoginForm
from flask_login import login_user, logout_user, login_required, current_user
import datetime

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

# Flask APP initialisation. Our Python package
@app.route('/shop')
@login_required
def shop_page():
    # Example dictionaries to use
    '''items=[{'id':1,'name':'Simple badge','price':60, 'rarity':"Common"},
        {'id':2,'name':'Black Judo belt','price':150, 'rarity':"Rare"},
        {'id':3,'name':'Shiny star','price':300, 'rarity':"Legendary"}
        ]'''
    items = Item.query.all()
    return render_template('shop.html',items=items)

@app.route('/chat')
def play_page():
    messages = Message.query.all()
    return render_template('chat.html')

@app.route('/feed', methods=['GET'])
@login_required
def feed_page():
    games = Game.query.all()
    return render_template('feed.html', games=games)

@app.route('/hangman')
def hangman_page():
    return render_template('hangman.html')

@app.route('/create', methods=['GET', 'POST'])
def create_page():
    form = CreateGameForm()
    if form.validate_on_submit():
        date = datetime.datetime.now()
        new_game = Game(creator_id=current_user.id, phrase=form.phrase.data,category=form.category.data,timeLimit=form.timeLimit.data,caption=form.caption.data,created=date,times_played=0,successes=0)
        db.session.add(new_game)
        db.session.commit()
        flash("Game is now live!",category="success")
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
        login_user(new_user)
        flash(f"Account created! Welcome, {new_user.username}",category='success')
        
        return redirect(url_for('shop_page'))
    
    #Check if any validations fail
    if form.errors != {}:
        for err_msg in form.errors.values():
           flash(f'There was an error with creating a user: {err_msg}',category='danger') 
    return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # If user not None
        if user and user.check_password(given_password=form.password.data):
            login_user(user)
            flash(f"You have logged in! Welcome back, {user.username}",category='success')
            return redirect(url_for('shop_page'))
        # If user or password none
        else:
            flash('Invalid username or password. Try again',category='danger')
    return render_template('login.html',form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have logged out!",category='info')
    return redirect(url_for("home_page"))

# profile page
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    user = current_user
    games_created = Game.query.filter_by(creator_id = user.id).count()
    return render_template('profile.html', user = user, games_created = games_created)
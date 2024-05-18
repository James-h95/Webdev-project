from application import app,db
from flask import render_template, redirect, url_for, flash, request,jsonify
from application.models import Item, User, Message, Game
from application.forms import RegisterForm, CreateGameForm,LoginForm, PurchaseItemForm
from flask_login import login_user, logout_user, login_required,current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

# Flask APP initialisation. Our Python package
@app.route('/shop',methods=['GET','POST'])
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
    purchased_items = [item.name for item in current_user.items]# List of curr user
    return render_template('shop2.html',items=items, form=form, purchased_items=purchased_items)


@app.route('/equip_avatar', methods=['POST'])
@login_required
def equip_avatar():
    equip_item = request.form.get('equip_item')
    item = Item.query.filter_by(name=equip_item).first()
    if item and item in current_user.items:
        # Logic to equip the item as the user's avatar
        current_user.avatar = item.image_url  # Assuming the item has an image_url attribute
        db.session.commit()
        flash(f"{item.name} has been equipped as your avatar!", category='success')
    else:
        flash("Item not found or not owned by the user.", category='danger')
    return redirect(url_for('shop_page'))


@app.route('/chat')
def play_page():
    messages = Message.query.all()
    return render_template('chat.html')

@app.route('/feed')
def feed_page():
    return render_template('feed.html')

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

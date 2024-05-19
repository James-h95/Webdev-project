from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, TextAreaField
from wtforms.validators import Length, EqualTo, DataRequired, NumberRange, Regexp, ValidationError
from application.models import User

# Register a user with the site
class RegisterForm(FlaskForm):
    
    #Check if username already exists
    def validate_username(self,username_given):
        user = User.query.filter_by(username=username_given.data).first()
        if user:
            raise ValidationError('Username already exists. Use different username')
    
    
    username = StringField('User Name:',validators=[Length(min=3,max=20), DataRequired()])
    password1 = PasswordField('Password:',validators=[Length(min=7), DataRequired()])
    password2 = PasswordField('Confirm Password:',validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField('Sign Up')
    
# Allow users to log in to the site
class LoginForm(FlaskForm):
    username = StringField('User Name:',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')
    
# Purchase an item in the shope
class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label="Purchase")
    
# Users can create games specifying category, time limit, phrase, and caption
# All validated according to length or min/max, phrase validated for bad characters
class CreateGameForm(FlaskForm):
    category = SelectField('Category:',choices=[("media", "Media"), ("books", "Books"), ("history", "History"), ("sports", "Sports"), ("music", "Music"), ("games", "Games"), ("places", "Places"), ("food", "Food"), ("misc", "Misc.")], validators=[DataRequired()])
    timeLimit = IntegerField('Time Limit (s):',validators=[NumberRange(min=20,max=120),DataRequired()])
    phraseValidator = Regexp(regex=r'^[a-zA-Z\s,"\'\?!:;.]+$', message='Must contain only letters and the following punctuation: ''"".,?!:;')
    phrase = TextAreaField('Word/phrase:',validators=[Length(min=3,max=250), phraseValidator,DataRequired()])
    caption = TextAreaField('Caption (optional):',validators=[Length(max=50)])
    submit = SubmitField('Create')
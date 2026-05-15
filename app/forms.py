from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Optional, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed

class CoffeeLogForm(FlaskForm):
    cafe_name=StringField('Cafe Name', validators=[DataRequired()])
    coffee_type=SelectField('Coffee Type', choices=[
        ('', 'Select a coffee type...'),
        ('cappuccino', 'Cappuccino'),
        ('flat_white', 'Flat White'),
        ('latte', 'Latte'), 
        ('long_black', 'Long Black'),
        ('espresso', 'Espresso'), 
        ('iced_latte', 'Iced Latte'), 
        ('cold_brew', 'Cold Brew'),
        ('cortado', 'Cortado'),
        ('piccolo', 'Piccolo'), 
        ('mocha', 'Mocha'), 
    ], validators=[DataRequired()])
    rating=IntegerField('Rating', validators=[DataRequired()])
    photo=FileField('Add a Photo', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png'])])
    notes=TextAreaField('Notes', validators=[Optional()])
    submit=SubmitField('Save to journal')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create account')
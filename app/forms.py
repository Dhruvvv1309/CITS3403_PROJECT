from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileField, FileAllowed

class CoffeeLogForm(FlaskForm):
    cafe_name=StringField('Cafe Name', validators=[DataRequired()])
    coffee_type=SelectField('Coffee Type', choices=[
        ('', 'Select a coffee type...'), #empty string so DataRequired() catches if user doesn't pick option
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
    photo=FileField('Add a Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    notes=TextAreaField('Notes', validators=[Optional()])
    submit=SubmitField('Save to journal')
    

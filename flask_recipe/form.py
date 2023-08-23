from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class RecipeForm(FlaskForm):
    query = StringField('query', validators=[DataRequired()])
    submit = SubmitField('submit')

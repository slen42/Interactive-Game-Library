from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
from games.services.authentication.valid_password import ValidPassword


class AddReviewForm(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired()])

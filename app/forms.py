from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from wtforms import validators
from flask_wtf.file import FileField, FileRequired, FileAllowed
import re
from app.models import Category

class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField('Category', 
        choices=[("", "Please select")] + [(str(c.id), c.name) for c in Category.query.order_by(Category.name.asc()).all()],
        validators=[DataRequired()])
    image = FileField('Feature image', validators=[
        # FileRequired(),
        FileAllowed(['jpg','jpeg','png'], 'Images (jpg, jpeg, png) only!')
    ])
    submit = SubmitField('Submit article')

class ArticleDeleteForm(FlaskForm):
    submit = SubmitField('Delete article')
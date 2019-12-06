from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Regexp
import re

class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Title', validators=[DataRequired()])
    category = SelectField('Category', 
        choices=[('politics', 'Politics'), 
                ('economics', 'Economics'),
                ('sports', 'Sports')],
        validators=[DataRequired()])
    image = FileField('Image File', validators=[DataRequired()])
    submit = SubmitField('Submit article')

    def validate_image(form, field):
        if field.data:
            field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data) 
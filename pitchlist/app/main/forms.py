from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField,
                    SubmitField, SelectField)
from wtforms.validators import Required

class PostForm(FlaskForm):
    title = StringField('Pitch title',validators=[Required()])
    post = TextAreaField('Your Pitch')
    category = SelectField(u'Category', choices=[('Sports', 'Sports'), 
                                                ('Tech', 'Tech'),
                                                ('Music', 'Music'),
                                                ('Other', 'Other') ])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment = TextAreaField('Post Comment', validators=[Required()])
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField("Tell us about yourself")
    submit = SubmitField("Update")
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from flask_login import current_user


class TranslationForm(FlaskForm):
    input_text = TextAreaField('Input your text', validators=[DataRequired()])
    output_text = TextAreaField('Translation', validators=[DataRequired()])
    submit = SubmitField('Save to my Dictionary')

    def validate_input_text(self, input_text):
        word = current_user.word.filter_by(word=input_text.data).first()
        if word is not None:
            raise ValidationError('This word in your dictionary')


class SearchWordForm(FlaskForm):
    search_word = StringField('Search word', validators=[DataRequired()])
    search = SubmitField('Go')

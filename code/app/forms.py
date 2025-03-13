from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,  TextAreaField, DecimalField, SelectField, FileField, IntegerField 
from wtforms.validators import DataRequired, Length, NumberRange, Optional, URL

class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Save')


class CourseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    language = StringField('Language', validators=[DataRequired()])
    level = SelectField('Level', choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    thumbnail = FileField('Thumbnail')



class LessonForm(FlaskForm):
    title = StringField(
        'Title', 
        validators=[DataRequired(), Length(max=255)]
    )
    content_type = SelectField(
        'Content Type',
        choices=[('video', 'Video'), ('pdf', 'PDF'), ('text', 'Text')],
        validators=[DataRequired()]
    )
    content_url = StringField(
        'Content URL',
        validators=[Optional(), URL(message="Invalid URL format")]
    )
    video_url = StringField(
        'Video URL',
        validators=[Optional(), URL(message="Invalid URL format")]
    )
    duration = StringField(
        'Duration (e.g., HH:MM:SS)',
        validators=[Optional()]
    )
    order = IntegerField(
        'Order',
        validators=[DataRequired(), NumberRange(min=1, message="Order must be at least 1")]
    )
    submit = SubmitField('Save')

    def validate_duration(form, field):
        if field.data:
            import re
            pattern = r'^(\d{1,2}):([0-5]?\d):([0-5]?\d)$'
            if not re.match(pattern, field.data):
                raise ValidationError("Invalid duration format. Use HH:MM:SS.")
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField,  TextAreaField, DecimalField, SelectField, FileField, IntegerField, ValidationError 
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
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    content_type = SelectField(
        'Content Type',
        choices=[('video', 'Video'), ('pdf', 'PDF'), ('text', 'Text')],
        validators=[DataRequired()]
    )
    content_url = HiddenField('Content Url', validators=[Optional()])
    text_content = TextAreaField('Text Content', validators=[Optional()])
    duration = StringField('Duration (e.g., HH:MM:SS)', validators=[Optional()])
    order = IntegerField('Order', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Save')

    def validate(self, extra_validators=None):
        rv = super().validate(extra_validators=extra_validators)
        if not rv:
            return False

        if self.content_type.data == 'text' and not self.text_content.data:
            self.text_content.errors.append('Text content is required.')
            return False

        return True

    def validate_duration(form, field):
        if field.data:
            import re
            pattern = r'^(\d{1,2}):([0-5]?\d):([0-5]?\d)$'
            if not re.match(pattern, field.data):
                raise ValidationError("Invalid duration format. Use HH:MM:SS.")

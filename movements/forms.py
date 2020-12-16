from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, HiddenField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, ValidationError, AnyOf, Email
from wtforms.widgets import TextArea, Select

from datetime import date

def must_contain_one_digit(form, field):
    for c in '0123456789':
        if c in field.data:
            return None
    raise ValidationError("Té que tindre com a mínim un número")



class MovementForm(FlaskForm):
    id = IntegerField ("id")
    data = DateField("Data", validators=[DataRequired()])
    concepte = StringField("Concepte", validators=[DataRequired(), Length(min=10, message= "El concepte té que tindre un mínim de 10 caracters"), must_contain_one_digit])
    quantitat = FloatField("Quantitat",validators=[DataRequired()])

    submit = SubmitField("Registrar")
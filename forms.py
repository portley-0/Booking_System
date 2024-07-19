from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField
from wtforms.validators import InputRequired, EqualTo

class RegistrationForm(FlaskForm):
    user_id = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    password2 = PasswordField("Repeat password:", validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    user_id = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    submit = SubmitField("Submit")

class BookingForm(FlaskForm):
    booking = SelectField("Please select a session: ", choices = ["9am - 10am", "10am - 11am", "11am - 12pm", "12pm - 1pm", "2pm - 3pm", "3pm - 4pm", "4pm - 5pm", "5pm - 6pm"], validators=[InputRequired()], coerce=str)
    date = DateField("Please select a date", validators=[InputRequired()])
    submit = SubmitField("Submit")


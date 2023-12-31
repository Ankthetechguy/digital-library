from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from werkzeug.security import check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import openai


api_key = "add_your_own_key"

# Initialize the OpenAI API client
openai.api_key = api_key

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///C:/Users/ankka/webdev/webappsflask/project1/user.db"
app.config['SECRET_KEY'] = "your_secret_key_here"
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class UserNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_auth.id'))
    content = db.Column(db.Text)


class UserAuth(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    notes = db.relationship('UserNote', backref='user', lazy=True)


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class NoteForm(FlaskForm):
    notes = TextAreaField('Notes')
    submit = SubmitField('Save')    

@login_manager.user_loader
def load_user(user_id):
    return UserAuth.query.get(int(user_id))

@login_manager.user_loader
def load_user(user_id):
    return UserAuth.query.get(int(user_id))

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = UserAuth.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email already registered. Please log in.", "error")
        else:
            new_user = UserAuth(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Signup successful", "success")
            return redirect(url_for('notelib'))
    return render_template('signup.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = UserAuth.query.filter_by(email=email).first()
        if user and UserAuth.query.filter_by(password=password).first():
            login_user(user)
            return redirect(url_for('notelib'))
        else:
            flash("Invalid email or password", "error")
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/notes", methods=["GET", "POST"])
@login_required
def notes():
    form = NoteForm()

    if form.validate_on_submit():
        doubts = request.form.get("question")

        # Use OpenAI to summarize the user's doubts
        summary = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"answer following text with detailed and well eplained pionts, also write solution or code if needed:\n\n{doubts}\n\nAnswer:",
            max_tokens=1000,
            stop=None,
        )
        summarized_doubts = summary.choices[0].text
        print(summarized_doubts)

        return render_template("notes.html", form=form,answer=summarized_doubts, question=doubts)

    return render_template("notes.html", form=form)

@app.route("/notelib")
@login_required
def notelib():
    return render_template('notelib.html')

@app.route("/notelibinneruc")
@login_required
def notelibinneruc():
    return render_template('notelibinneruc.html')    

@app.route("/notelibinnerpc")
@login_required
def notelibinnerpc():
    return render_template('notelibinnerpc.html')

@app.route("/notelibinneroe")
@login_required
def notelibinneroe():
    return render_template('notelibinneroe.html')        


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)









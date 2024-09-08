from flask import Flask, jsonify, request, render_template_string, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a real secret key
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    tasks = db.relationship('Task', backref='author', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Forms
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Task')

# Routes
@app.route('/')
@jwt_required()
def index():
    current_user = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=current_user['id']).all()
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><title>Task Manager</title></head>
        <body>
            <nav>
                <a href="{{ url_for('index') }}">Home</a>
                <a href="{{ url_for('login') }}">Login</a>
                <a href="{{ url_for('register') }}">Register</a>
            </nav>
            <h1>Welcome to Task Manager!</h1>
            <h2>Your Tasks:</h2>
            <ul>
                {% for task in tasks %}
                    <li>
                        <h3>{{ task.title }}</h3>
                        <p>{{ task.description }}</p>
                        <form action="{{ url_for('delete_task', task_id=task.id) }}" method="post">
                            <button type="submit">Delete</button>
                        </form>
                    </li>
                {% endfor %}
            </ul>
        </body>
        </html>
    ''', tasks=tasks)

@app.route('/register', methods=['POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return jsonify(message='User registered successfully'), 201
    return jsonify(message='Invalid input'), 400

@app.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            access_token = create_access_token(identity={'id': user.id, 'username': user.username})
            return jsonify(access_token=access_token), 200
        return jsonify(message='Invalid credentials'), 401
    return jsonify(message='Invalid input'), 400

@app.route('/task/new', methods=['POST'])
@jwt_required()
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        current_user = get_jwt_identity()
        task = Task(title=form.title.data, description=form.description.data, user_id=current_user['id'])
        db.session.add(task)
        db.session.commit()
        return jsonify(message='Task created successfully'), 201
    return jsonify(message='Invalid input'), 400

@app.route('/task/<int:task_id>/delete', methods=['POST'])
@jwt_required()
def delete_task(task_id):
    current_user = get_jwt_identity()
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user['id']:
        return jsonify(message='Not authorized'), 403
    db.session.delete(task)
    db.session.commit()
    return jsonify(message='Task deleted successfully'), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

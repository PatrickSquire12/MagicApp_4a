from flask import Flask, request, render_template, redirect, url_for, flash
from markupsafe import Markup
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# Change below file for offline debugging
user_credentials_file = '/home/PDogg95/MagicApp_4a/user_data/user_credentials.txt'

# Define the base directory for uploads
uploads_dir = '/home/PDogg95/MagicApp_4a/uploads'

# Function to check credentials
def check_credentials(username, password):
    with open(user_credentials_file, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 2:
                stored_username, stored_password = parts
                if stored_username == username and stored_password == password:
                    return True
    return False

# Function to check if a username exists
def username_exists(username):
    with open(user_credentials_file, 'r') as file:
        for line in file:
            stored_username, _ = line.strip().split(',')
            if stored_username == username:
                return True
    return False

# Function to register a new user
def register_user(username, password):
    with open(user_credentials_file, 'a') as file:
        file.write(f"{username},{password}\n")

# Function to reset password
def reset_password(username, new_password):
    lines = []
    with open(user_credentials_file, 'r') as file:
        lines = file.readlines()
    
    with open(user_credentials_file, 'w') as file:
        for line in lines:
            stored_username, stored_password = line.strip().split(',')
            if stored_username == username:
                file.write(f"{username},{new_password}\n")
            else:
                file.write(line)
                
                
                
# Function to create user directories and files
def create_user_files(username):
    user_dir = os.path.join(uploads_dir, username)
    os.makedirs(user_dir, exist_ok=True)
    
    # Create collection.txt
    with open(os.path.join(user_dir, 'collection.txt'), 'w') as f:
        f.write('')
    
    # Create deck1.txt to deck20.txt
    for i in range(1, 21):
        with open(os.path.join(user_dir, f'deck{i}.txt'), 'w') as f:
            f.write('')

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if check_credentials(username, password):
        global current_user
        current_user = username
        return f"Welcome, {username}!"
    else:
        flash(Markup("<span style='color: red;'>Incorrect Username or Password</span>"))
        return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username_exists(username):
            flash(Markup("<span style='color: red;'>Username already in use</span>"))
            return redirect(url_for('register'))
        else:
            register_user(username, password)
            create_user_files(username)  # Create user files upon registration
            flash(Markup("<span style='color: green;'>Registration successful</span>"))
            return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']
        if username_exists(username):
            reset_password(username, new_password)
            flash(Markup("<span style='color: green;'>Password reset successfully</span>"))
            return redirect(url_for('home'))
        else:
            flash(Markup("<span style='color: red;'>Username not found</span>"))
            return redirect(url_for('forgot_password'))
    return render_template('forgot_password.html')

if __name__ == '__main__':
    app.run(debug=True)

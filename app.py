from flask import Flask, request, render_template, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# Change below file for offline debugging
user_credentials_file = '/home/PDogg95/MagicApp_4a/user_data/user_credentials.txt'

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

# Function to register a new user
def register_user(username, password):
    with open(user_credentials_file, 'a') as file:
        file.write(f"{username},{password}\n")
        
# Function to check if a username exists
def username_exists(username):
    with open(user_credentials_file, 'r') as file:
        for line in file:
            stored_username, _ = line.strip().split(',')
            if stored_username == username:
                return True
    return False


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
        flash("Incorrect Username or Password")
        return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username_exists(username):
            flash("Username already in use")
            return redirect(url_for('register'))
        else:
            register_user(username, password)
            return redirect(url_for('home'))
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
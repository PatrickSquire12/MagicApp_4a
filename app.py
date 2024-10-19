from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Change below file for offline debugging
user_credentials_file = '/home/PDogg95/MagicApp_4a/user_data/user_credentials.txt'

# Function to check credentials
def check_credentials(username, password):
    with open(user_credentials_file, 'r') as file:
        for line in file:
            stored_username, stored_password = line.strip().split(',')
            if stored_username == username and stored_password == password:
                return True
    return False

# Function to register a new user
def register_user(username, password):
    with open(user_credentials_file, 'a') as file:
        file.write(f"{username},{password}\n")

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
        return "Invalid credentials. Please try again."

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        register_user(username, password)
        return redirect(url_for('home'))
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)

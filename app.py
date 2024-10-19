from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

#change below file for offline debugging
user_credentials_file = '/home/PDogg95/MagicApp_4a/user_data/user_credentials.txt'

# Function to check credentials
def check_credentials(username, password):
    with open(user_credentials_file, 'r') as file:
        for line in file:
            stored_username, stored_password = line.strip().split(',')
            if stored_username == username and stored_password == password:
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
        # Save the current user as a variable
        global current_user
        current_user = username
        return f"Welcome, {username}!"
    else:
        return "Invalid credentials. Please try again."

if __name__ == '__main__':
    app.run(debug=True)

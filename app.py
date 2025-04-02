from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from markupsafe import Markup
import os


##############################################################################################################
#change below variables for offline vs server
# STATIC_DIR = r'C:\Users\squ111732\Documents\python_workspace\home projects\MagicApp_4a\static' #work pc
STATIC_DIR = r'C:\Users\patri\Documents\Computer\Python\MagicApp_4a\static' #home pc
# STATIC_DIR = '/home/PDogg95/MagicApp_4a/static' #python server

# Change below file for offline vs server
# user_credentials_file = '/home/PDogg95/MagicApp_4a/user_data/user_credentials.txt' #python server
user_credentials_file = 'user_data/user_credentials.txt' #home or work

# Define the base directory for uploads
# uploads_dir = '/home/PDogg95/MagicApp_4a/uploads' #python server
uploads_dir = 'uploads'    #home or work

################################################################################################################
app = Flask(__name__, static_folder=STATIC_DIR)
app.secret_key = 'your_secret_key'  # Replace with a secure key

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
    
    # Create deck1.txt to deck21.txt
    for i in range(1, 22):
        with open(os.path.join(user_dir, f'deck{i}.txt'), 'w') as f:
            f.write('')
    
    # Create reference.txt
    with open(os.path.join(user_dir, 'reference.txt'), 'w') as f:
        for i in range(1, 22):
            f.write(f'Deck {i},Deck {i}\n')
    
    # Create scores.txt with 21 lines each containing 0
    with open(os.path.join(user_dir, 'scores.txt'), 'w') as f:
        for _ in range(21):
            f.write('0\n')


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
        return redirect(url_for('index'))  # Redirect to the index page on successful login
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
    
 
@app.route('/index')
def index():
    global current_user  # Use the global variable for the current user
    if 'current_user' not in globals() or current_user is None:
        return redirect(url_for('home'))
    
    percentages = calculate_percentages(current_user)
    return render_template('index.html', username=current_user,percentages=percentages)

    
    
@app.route('/update_file', methods=['POST'])
def update_file():
    data = request.get_json()
    print(f"Current user: {current_user}")  # Debugging line
    print(f"Received request data: {data}")  # Debugging line
    file_type = data['type']
    index = data['index']
    text = data['text']
    deck_name = data.get('deckName', None)

    user_dir = os.path.join(uploads_dir, current_user)
    if file_type == 'Collection':
        file_path = os.path.join(user_dir, 'collection.txt')
    else:
        file_path = os.path.join(user_dir, f'deck{index}.txt')

    with open(file_path, 'w') as file:
        file.write(text)
    print(f"Updated {file_path} with provided text.")  # Debugging line

    # Update reference.txt if deck_name is provided
    if deck_name:
        reference_file_path = os.path.join(user_dir, 'reference.txt')
        lines = []
        with open(reference_file_path, 'r') as file:
            lines = file.readlines()
        
        with open(reference_file_path, 'w') as file:
            for line in lines:
                if line.startswith(f'Deck {index},'):
                    file.write(f'Deck {index},{deck_name}\n')
                else:
                    file.write(line)
        print(f"Updated reference.txt with Deck {index} name: {deck_name}")  # Debugging line

    return jsonify({'message': f'{file_type} {index} updated successfully!'})


@app.route('/get_deck_name', methods=['GET'])
def get_deck_name():
    index = request.args.get('index')
    user_dir = os.path.join(uploads_dir, current_user)
    reference_file_path = os.path.join(user_dir, 'reference.txt')
    
    deck_name = ''
    with open(reference_file_path, 'r') as file:
        for line in file:
            if line.startswith(f'Deck {index},'):
                deck_name = line.strip().split(',')[1]
                break
    
    return jsonify({'deckName': deck_name})


@app.route('/get_deck_data', methods=['GET'])
def get_deck_data():
    index = request.args.get('index')
    print(f'Received index: {index}')  # Debugging line
    user_dir = os.path.join(uploads_dir, current_user)
    reference_file_path = os.path.join(user_dir, 'reference.txt')
    deck_file_path = os.path.join(user_dir, f'deck{index}.txt')
    
    deck_name = ''
    with open(reference_file_path, 'r') as file:
        for line in file:
            if line.startswith(f'Deck {index},'):
                deck_name = line.strip().split(',')[1]
                break
    
    deck_content = ''
    if os.path.exists(deck_file_path):
        with open(deck_file_path, 'r') as file:
            raw_content = file.read()
            # Normalize newlines without stripping any whitespace
            deck_content = raw_content.replace('\n\n', '\n')
            
    return jsonify({'deckName': deck_name, 'deckContent': deck_content})
    
    
    
@app.route('/get_collection_data')
def get_collection_data():
    user_folder = os.path.join(uploads_dir, current_user)
    collection_file = os.path.join(user_folder, 'collection.txt')
    
    collection_content = ''
    if os.path.exists(collection_file):
        with open(collection_file, 'r') as file:
            raw_content = file.read()
            print("Raw content from file:")
            print(repr(raw_content))  # Use repr to show hidden characters like \n and \r
            
            # Normalize newlines without stripping any whitespace
            collection_content = raw_content.replace('\n\n', '\n')
            print("Normalized content:")
            print(repr(collection_content))
    
    return jsonify({'collectionContent': collection_content})


def calculate_percentages(user):
    user_folder = os.path.join(uploads_dir, user)
    collection_file = os.path.join(user_folder, 'collection.txt')
    reference_file = os.path.join(user_folder, 'reference.txt')
    
    # Read the lines in collection.txt
    try:
        with open(collection_file, 'r') as f:
            collection_lines = set(line.strip() for line in f.readlines())
    except FileNotFoundError:
        collection_lines = set()
    
    # Read the reference.txt file and create a dictionary for deck names
    deck_names = {}
    try:
        with open(reference_file, 'r') as f:
            for line in f:
                deck_number, deck_name = line.strip().split(',')
                deck_names[deck_number] = deck_name
    except FileNotFoundError:
        pass
    
    percentages = []
    for i in range(1, 22):
        deck_file = os.path.join(user_folder, f'deck{i}.txt')
        try:
            with open(deck_file, 'r') as f:
                deck_lines = [line.strip() for line in f.readlines()]
            matching_lines = sum(1 for line in deck_lines if line in collection_lines)
            deck_count = len(deck_lines)
        except FileNotFoundError:
            matching_lines = 0
            deck_count = 0
        
        if deck_count > 0:
            percentage = (matching_lines / deck_count) * 100
        else:
            percentage = 0
        
        deck_name = deck_names.get(f'Deck {i}', 'Unknown')
        percentages.append((f'Deck {i}', deck_name, f'{percentage:.2f}%'))
    
    return percentages

@app.route('/get_percentages')
def get_percentages():
    percentages = calculate_percentages(current_user)
    return {'percentages': percentages}



@app.route('/logout')
def logout():
    global current_user
    current_user = None
    return redirect(url_for('home'))
    
    
@app.route('/deck.html')
def deck_page():
    return render_template('deck.html')


@app.route('/collection.html')
def collection_page():
    print(f"Current user before rendering collection.html: {current_user}")  # Debugging line
    return render_template('collection.html')


@app.route('/update_collection', methods=['POST'])
def update_collection():
    text_content = request.form['textContent']
    user_dir = os.path.join(uploads_dir, current_user)
    file_path = os.path.join(user_dir, 'collection.txt')

    with open(file_path, 'w') as file:
        file.write(text_content)

    return redirect(url_for('index'))
    
    
@app.route('/update_deck', methods=['POST'])
def update_deck():
    # Get updated deck name and content from the form
    deck_name = request.form['deckName']
    deck_content = request.form['textContent']
    index = request.args.get('index')  # Retrieve index from query string

    user_dir = os.path.join(uploads_dir, current_user)
    reference_file_path = os.path.join(user_dir, 'reference.txt')
    deck_file_path = os.path.join(user_dir, f'deck{index}.txt')

    # Update deck content in deck{index}.txt
    with open(deck_file_path, 'w') as file:
        file.write(deck_content)

    # Update deck name in reference.txt
    with open(reference_file_path, 'r') as file:
        lines = file.readlines()

    # Ensure the index is valid and update the correct line
    if index and 0 < int(index) <= len(lines):
        lines[int(index) - 1] = f'Deck {index},{deck_name}\n'  # Update the line format

    with open(reference_file_path, 'w') as file:
        file.writelines(lines)

    return redirect(url_for('index'))





        
        
# @app.route('/get_deck_data')
# def get_deck_data():
    # index = request.args.get('index', type=int)
    # user_folder = os.path.join(uploads_dir, current_user)
    # deck_file = os.path.join(user_folder, f'deck_{index}.txt')
    
    # deck_content = ''
    # if os.path.exists(deck_file):
        # with open(deck_file, 'r') as file:
            # raw_content = file.read()
            # print("Raw content from file:")
            # print(repr(raw_content))  # Use repr to show hidden characters like \n and \r
            
            # Normalize newlines without stripping any whitespace
            # deck_content = raw_content.replace('\n\n', '\n')
            # print("Normalized content:")
            # print(repr(collection_content))
    
    # return jsonify({'deckContent': deck_content})




if __name__ == '__main__':
    app.run(debug=True)

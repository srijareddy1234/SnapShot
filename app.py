from flask import Flask, request, jsonify, render_template, send_from_directory, session
import json
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'your_super_secret_key_here'

UPLOAD_FOLDER = 'data/gallery'
POSTS_FILE = 'data/posts.json'
USERS_FILE = 'users.json'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helpers
def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/gallery/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()

    if not email or not password:
        return jsonify({'success': False, 'error': 'Email and password are required'}), 400

    users = load_users()
    for user in users:
        if user['email'] == email and check_password_hash(user['password'], password):
            session['username'] = user['username']
            return jsonify({'success': True})

    return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email', '').strip().lower()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not email or not username or not password:
        return jsonify({'success': False, 'error': 'All fields are required'}), 400

    users = load_users()
    if any(u['email'] == email or u['username'] == username for u in users):
        return jsonify({'success': False, 'error': 'User already exists'}), 409

    hashed_password = generate_password_hash(password)
    users.append({'email': email, 'username': username, 'password': hashed_password})
    save_users(users)
    return jsonify({'success': True})

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No image part', 400

    image = request.files['image']
    if image.filename == '':
        return 'No selected file', 400

    if not allowed_file(image.filename):
        return 'Invalid file type', 400

    filename = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    post = {
        "type": "image",
        "filename": filename
    }

    try:
        with open(POSTS_FILE, 'r') as f:
            posts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        posts = []

    posts.append(post)

    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f, indent=2)

    return 'Image uploaded', 200

@app.route('/submit-post', methods=['POST'])
def submit_post():
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({'message': 'No content provided'}), 400

    post = {'type': 'text', 'content': data['content']}
    try:
        with open(POSTS_FILE, 'r+') as f:
            posts = json.load(f)
            posts.append(post)
            f.seek(0)
            f.truncate()
            json.dump(posts, f, indent=2)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(POSTS_FILE, 'w') as f:
            json.dump([post], f, indent=2)

    return jsonify({'message': 'Post submitted successfully!'})

@app.route('/get-posts')
def get_posts():
    try:
        with open(POSTS_FILE) as f:
            posts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        posts = []
    return jsonify(posts)

@app.route('/clean-posts', methods=['POST'])
def clean_posts():
    try:
        with open(POSTS_FILE, 'r') as f:
            posts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({'message': 'No posts found.'}), 404

    cleaned_posts = [
        post for post in posts
        if post['type'] != 'image' or os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], post['filename']))
    ]

    with open(POSTS_FILE, 'w') as f:
        json.dump(cleaned_posts, f, indent=2)

    return jsonify({'message': 'Cleaned broken image posts.'})

@app.route('/change-password', methods=['POST'])
def change_password():
    data = request.get_json()
    old_password = data.get('oldPassword')
    new_password = data.get('newPassword')

    username = session.get('username')
    if not username:
        return jsonify({'message': 'Not logged in'}), 401

    users = load_users()
    for user in users:
        if user['username'] == username:
            if not check_password_hash(user['password'], old_password):
                return jsonify({'message': 'Old password is incorrect'}), 400
            user['password'] = generate_password_hash(new_password)
            save_users(users)
            return jsonify({'message': 'Password changed successfully'})

    return jsonify({'message': 'User not found'}), 404

@app.route('/logout')
def logout():
    session.pop('username', None)
    return jsonify({'message': 'Logged out'})

if __name__ == '__main__':
    app.run(debug=True)

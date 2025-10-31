#this is the main flask app
#it consists of 5 main functions
#@app.route is used to maintain the route in which the app'll work
#1. home - it is the page where all the other 4 are connected, it is like an entrance to a movie theater
#2.
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from utils import create_token
from decor import token_req, admin_req

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY']=os.getenv("SECRET_KEY")

#mock user db for testing
users_db = {
    "alice":{"password": "password123", "user_id": 1, "role":"user"},
    "bob": {"password": "bobpass", "user_id": 2, "role": "user"},
    "sarvadnya":{"password": "vedimulgi", "user_id": 3, "role": "user"},
    "shravani": {"password":"vedimulgi2","user_id": 4, "role": "admin"},
    "duryodhan":{"password":"suikinok", "user_id": 5, "role": "admin"}
}
@app.route('/')
def home():
    """
    Home page - Theater Entrance
    """
    return jsonify({
        'message': 'Welcome to JWT Auth Theater!',
        'endpoints':{
            'POST /login': 'Get your access token',
            'GET /public': 'Public area (no token needed)',
            'GET /protected': 'Protected area (token req)',
            'GET /admin': 'Admin area (admin token required)'
        }
    })

@app.route('/login',methods=['POST'])
def login():
    """
    Login endpoint - Ticket counter
    """
    data = request.json

    #validate input
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({
            'message': 'Username or password is incorrect!',
            'status': 'error'
        }), 400
    
    username = data['username']
    password = data['password']

    #checking credentials (ofc in real app this would be checked against db)
    user = users_db.get(username)
    if user and user['password'] == password:
        #credentials valid therefore create token
        token = create_token(
            user_id = user['user_id'],
            username=username,
            secret_key=app.config['SECRET_KEY']
        )

        return jsonify({
            'message': 'Login',
            'token': token,
            'user':{
                'username': username,
                'user_id': user['user_id'],
                'role': user['role']
            },
            'status': 'success'
        }) 
    else:
        return jsonify({
            'message': 'Invalid username or password',
            'status': 'error'
        }), 401
@app.route('/public', methods=['GET'])
def public_route():
    """
    Public route - Theater Lobby (No ticket needed)
    """
    return jsonify({
        'message': 'This is a public area, no token needed.',
        'status': 'success'
    })

@app.route('/protected',methods=['GET'])
@token_req
def protected_route(user_data): #like movie theatre where ticket itc token is req
    """
    Protected route 
    """
    return jsonify({
        'message':f'Welcome to the VIP area, {user_data["username"]}',
        'your_data': user_data,
        'access': 'You have access to protected content',
        'status': 'success'
    })
@app.route('/admin', methods=['GET'])
@token_req
def admin_route(user_data):
    """
    Admin route (for admin only)
    """
    if user_data.get('role') != 'admin':
        return jsonify({
            'message': 'Admin access required!',
            'status': 'error'
        }), 403
    return jsonify({
        'message': f'Welcome to amdin panel, {user_data["username"]}',
        'admin_features':['User management','System settings','Analytics'],
        'status':'success'
    })

@app.route('/profile',methods=['GET'])
@token_req
def user_profile(user_data): #like a personel locker area
    """
    User profile
    """
    return jsonify({
        'message': 'Your profile information',
        'user_data': user_data,
        'profile_features': ['View history','Settings','Pereferences'],
        'status': 'success'
    })

if __name__=='__main__':
    print("Starting JWT Auth Theater...")
    print("Endpoints:")
    print(" http://localhost:5000/ - Home")
    print(" http://localhost:5000/login - Login")
    print(" http://localhost/protected - Protected area")
    print(" http://localhost:5000/admin - Admin area")

    app.run(debug=True)


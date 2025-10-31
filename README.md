# Basic JWT Authentication with Flask
A simple JWT token implementation using Flask to understand how authentication works in web applications.

# What This Does
This project shows how to:
1. Create JWT tokens when users login
2. Protect certain routes so only logged-in users can access them
3. Verify tokens to check if users are authenticated
4. Handle token expiration and errors

# Quick Start
Install requirements:
pip install flask pyjwt python-dotenv

Run the server:
python app.py

Test the API:
1. Get a token:
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"password123"}'
2. Use the token:
curl -X GET http://127.0.0.1:5000/protected \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
   
# Project Structure
1. app.py - Main Flask application with routes
2. jwt_utils.py - Functions to create and verify JWT tokens
3. auth_decorators.py - Protection for routes that need authentication

# Learning Purpose
This is a beginner-friendly project to understand:
1. How JWT tokens work
2. Basic web authentication
3. Flask route protection
4. API development fundamentals
5. Perfect for learning web development and authentication concepts!

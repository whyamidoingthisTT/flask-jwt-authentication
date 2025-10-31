#this file is for APItesing script
from flask import requests
import json

BASE_URL = "http://localhost:5000"

def test_public_route():
    """Test public route (x token) """
    print("Testing Public Route...")
    response = requests.get(f"{BASE_URL}/public")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_login(username, password):
    """Test login and get token"""
    print(f"Testing Login for {username}...")
    response = requests.post(
        f"{BASE_URL}/login",
        json={"username": username,"password": password}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Token: {data['token'][:50]}...") #will show furst 50 chars
        return data['token']
    else:
        print(f"Error: {response.json()}")
        return None
    

def test_protected_route(token):
    """Test protected route with token"""
    print("Testing Protected Route...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/protected", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_admin_route(token):
    """Test admin route (w token)"""
    print("Testing Admin Route...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/admin", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_without_token():
    """Test protected wwithout token"""
    print("Testing Protected Route (x token)...")
    response = requests.get(f"{BASE_URL}/protected")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

if __name__ == "__main__":
    print("🧪 Starting API Tests...\n")
    
    # Test 1: Public route
    test_public_route()
    
    # Test 2: Try protected route without token
    test_without_token()
    
    # Test 3: Login as regular user
    user_token = test_login("alice", "password123")
    if user_token:
        test_protected_route(user_token)
        test_admin_route(user_token)

    # Test 4: Login as admin
    admin_token = test_login("admin", "adminpass")
    if admin_token:
        test_protected_route(admin_token)
        test_admin_route(admin_token)  # This should work
    
    print("🎉 All tests completed!")

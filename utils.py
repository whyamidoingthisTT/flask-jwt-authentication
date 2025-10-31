#this is the jwt utils file that consist of 3 functioins, jwt token functions
# 1. create_token -> this function creates the tokens for each user may it be admin or normal user
# 2. verify_token -> this function assigns the secret key with the token to verify if it exists or is valid
# 3. refresh_token -> (optional function) this function refreshes an existing function by temporarily deleting the expiry and iat for that specific function

import jwt
import datetime

def create_token(user_id, username, secret_key):
    """
    Create a JWT token - The Ticket Printing Machine
    
    Args:
        user_id: Unique user identifier
        username: User's username
        secret_key: Secret key to sign the token
        
    Returns:
        str: Encoded JWT token
    """

    #payload=data stored inside token
    payload ={
        'user_id': user_id,
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1), #expiry 1 hr
        'iat': datetime.datetime.utcnow() #issued at time
    }
    #create token=sign payload w secret key
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def verify_token(token, secret_key):
    """
    Verify JWT token - The Ticket Scanner
    
    Args:
        token: JWT token to verify
        secret_key: Secret key used to verify signature
        
    Returns:
        dict: Token payload if valid, None if invalid
    """
    try:
        #decode+verify token sign+expiry
        payload = jwt.decode(token,secret_key,algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        #expired
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        #invalid/fake
        print("Invalid token")
        return None
    
#refreshing fun (timepass)
def refresh_token(token, secret_key):
    """
    Refresh an existing token
    """
    payload = verify_token(token, secret_key)
    if payload:
        #removing expiration+issued at from og payload
        payload.pop('exp',None)
        payload.pop('iat',None)
        #new token
        return create_token(payload['user_id'], payload['username'], secret_key)
    return None


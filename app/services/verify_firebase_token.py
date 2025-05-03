from firebase_admin import auth
from firebase_admin.auth import InvalidIdTokenError, ExpiredIdTokenError, RevokedIdTokenError

def verify_firebase_token(id_token):
    return "123"
    # try:
    #     decoded_token = auth.verify_id_token(id_token, check_revoked=True)
    #     uid = decoded_token['uid']
    #     return uid
    # except InvalidIdTokenError:
    #     print("Invalid ID token.")
    # except ExpiredIdTokenError:
    #     print("ID token has expired.")
    # except RevokedIdTokenError:
    #     print("ID token has been revoked.")
    # except Exception as e:
    #     print(f"Token verification failed: {e}")
    # return None

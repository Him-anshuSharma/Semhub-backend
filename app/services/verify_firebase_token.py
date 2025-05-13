import logging
import os
import firebase_admin
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth, credentials

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    try:
        cred_path = os.getenv('FIREBASE_CREDENTIALS')
        if not cred_path:
            raise ValueError("FIREBASE_CREDENTIALS environment variable not set")
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        logger.info("Firebase Admin SDK initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Firebase Admin SDK: {str(e)}")
        raise

security = HTTPBearer()

async def verify_firebase_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify Firebase ID token from Authorization header.
    Returns the decoded token if valid.
    """
    try:
        logger.info("Verifying Firebase token...")
        token = credentials.credentials
        
        if not token:
            logger.error("No token found in credentials")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No authentication token provided"
            )
            
        logger.info(f"Token received (first 10 chars): {token[:10]}...")
        
        # Verify the token
        decoded_token = auth.verify_id_token(token)
        
        logger.info(f"Token verified successfully for user: {decoded_token.get('uid')}")
        return decoded_token
        
    except auth.ExpiredIdTokenError:
        logger.error("Token has expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired"
        )
    except auth.RevokedIdTokenError:
        logger.error("Token has been revoked")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has been revoked"
        )
    except auth.InvalidIdTokenError as e:
        logger.error(f"Invalid token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    except Exception as e:
        logger.exception(f"Unexpected error during token verification: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )

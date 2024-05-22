import os
import secrets
import string


def generate_random_secret_key(lenth:int=16):
    """
    Generates a random secret key of the specified length.

    Parameters:
        lenth (int, optional): The length of the secret key. Defaults to 16.

    Returns:
        str: The randomly generated secret key.
    """
    return ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(lenth))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', generate_random_secret_key(16))
    ADMINS = []

    # Mongoengine
    MONGO_TIMEOUT = os.environ.get('MONGO_TIMEOUT', 1000)
    # DBs URI
    USERS_DB_URI = os.environ.get('USERS_DB_URI', 'mongodb://localhost:27017')
    COSMETICS_DB_URI = os.environ.get('COSMETICS_DB_URI', 'mongodb://localhost:27018')

    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ALGORITHM = "HS256"
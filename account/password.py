# password.py
# @author Allen Wittika
#
# Handles the password parameter handling and hashing as well as assigning the password.


#Imports
import string
import bcrypt


class Password:


    #
    # @param password
    #
    # @require password between 10 and 16 characters
    # @require password contains at least one number
    # @require password contains special character
    #
    # @ensure only hashed password is associated
    def __init__(self, password):

        if password is None:
            raise ValueError("Error: Password cannot be empty..")

        if not (10 <= len(password) <= 16):
            raise ValueError("Error: Password must be between 10 and 16 characters..")

        if not any(char.isdigit() for char in password):
            raise ValueError("Error: Password must contain at least one number..")

        if not any(char in string.punctuation for char in password):
            raise ValueError("Error: Password must contain at least one symbol..")

        salt = bcrypt.gensalt()
        self._passhash = bcrypt.hashpw(password.encode(), salt)

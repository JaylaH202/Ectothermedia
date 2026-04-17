# password.py
# @author Allen Russell
# @date created: 2/16/26
# @date modified: 2/18/26
#
# This class implements the password child domain, applying the constraints and keeping parameters within valid bounds.


# Imports the needed libraries and dependencies
import bcrypt, string
# Bcrypt is used over hashlib for it's slower and more secure hashing, as well as it's built-in method for salting and versatility
# involving the salt value.


# The password class
class Password:
    
    
    
    # The password constructor
    #
    # @param password: a string password
    #
    # @require password: Password must be validated
    #
    # @ensure salt: salt for password hashing is generated for each password
    def __init__(self, password):
        
        # Validates password through a helper function and returns a tuple with the boolean
        # and possible error if any, otherwise it is Null. This is done so that changePassword()
        # does not crash the system when validating the new password to change to.
        check = Password.validatePassword(password)
        
        if check[0]:
            # Create the salt value | bcrypt stores the unique salt in the hashed string
            salt = bcrypt.gensalt()
        
            # Cast the string password as bytes for hashing
            password = password.encode('utf-8')
        
            # Hash the password with the salt then store the hashed password, making sure to decode the
            # bytes back into a string format for database storing.
            self.p_hash = bcrypt.hashpw(password, salt).decode('utf-8')
            # will need to .encode('utf-8') it back to bytes before passing it to bcrypt.checkpw() when verifying logins
        
            password = None #Nullify the temporary variable now that the password is set to minimize security risk
        else:
            raise TypeError(check[1]) # | account_controller needs to print this message to user in webpage |
        
        
        
    # The special methods: __str__ and __repr__ for use in keeping the password hidden to minimize security risk
    
    # __repr__ method
    #
    # @param self
    def __repr__(self):
        return "Protected Password"
        
        
        
    # __str__ method
    #
    # @param self
    def __str__(self):
        return "********"
    
    

    # Mutator and Accesor methods as needed
    
    # changePassword()
    #
    # @param self
    # @param currPass: The attempted current password
    # @param newPass: The new password to change to
    #
    # @require newPass should not be self | Don't change username to be the same
    #
    # @ensure newPass is run through the constraints and boundaries for a username
    # @ensure Password is changed before returning true
    def changePassword(self, currPass, newPass):
            
        # Password should be verified before changing to a new password.
        if self.verifyPassword(currPass):
            
            #New password must be different
            if self.verifyPassword(newPass):
                return False, "New password must be different from the current password."
            
            # Checks to ensure that the new username is a valid username before setting it
            check = Password.validatePassword(newPass)
        
            # The new password is valid, so hash then set the new username
            if check[0]:
                # Create the salt value | bcrypt stores the unique salt in the hashed string
                salt = bcrypt.gensalt()
        
                # Cast the string password as bytes for hashing
                newPass = newPass.encode('utf-8')
        
                # Hash the password with the new salt then store the hashed password, making sure to
                # decode the bytes back into a string format for database storing.
                self.p_hash = bcrypt.hashpw(newPass, salt).decode('utf-8')
        
                currPass = None#Nullify the temporary variable now that the new password is set to minimize security risk
                newPass = None #Nullify the temporary variable now that the new password is set to minimize security risk
                return True, "Successfully changed." # | account_controller needs to print this message to user in webpage |
                
            #The new password is invalid, so return false and the error
            else:
                return False, check[1]
        # The current password was not verified.    
        else:
            return False, "Must verify old password to change password." # | account_controller needs to print this message to user in webpage |
        
        
        
    #verifyPassword()
    #
    # @param self
    # @param otherPass: The attempted password
    #
    # @require otherPass: String object
    # @require otherPass: Must not be empty -> Saves time on bcrypt processing
    #
    # @ensure Passwords match before returning true
    def verifyPassword(self, otherPass):
        
        # Should otherPass not meet the string requirement:
        if not isinstance(otherPass, str):
            return False # Returns false under assumption of making multiple password attempts
        
        # Should otherPass be an empty string:
        if not otherPass:
            return False # Returns false under assumption of making multiple password attempts
        
        # Encode otherPass to bytes for comparison
        otherPass = otherPass.encode('utf-8')
        
        # Compare the attempted password with the password stored and return the result
        return bcrypt.checkpw(otherPass, self.p_hash.encode('utf-8'))
    
    
    
    # validatePassword()
    #
    # Helper function for validating constraints and boundaries and it returns a tuple so that
    # errors can still be specified without breaking the system during a password check.
    #
    # @param password: Password to be validated
    #
    # @require password: String object
    # @require password: 8 <= length <= 16
    # @require password: must not contain whitespace
    # @require password: must contain a special character (ex. _, !, ?)
    # @require password: must contain a numerical character (ex. 1, 2, 3)
    #
    # @ensure True or False is returned as well as the error, if any.
    def validatePassword(password):
                
        # Should username not meet the string requirement:
        if not isinstance(password, str):
            return False, "New Password must be a string."
        
        # Should username not meet the length requirement:
        if len(password) < 8 or len(password) > 16:
            return False, "New Password must be 8 to 16 characters long."
        
        # Should username contain spaces or be empty:
        if any(char.isspace() for char in password) or not password:
            return False, "New Password must not be empty or contain spaces."
        
        # Should password not meet the special character requirement:
        if not any(char in string.punctuation for char in password):
            return False, f"New Password must include one special character: {string.punctuation}"
            
        # Should password not meet the numerical character requirement:
        if not any(char.isdigit() for char in password):
            return False, f"Password must include one numerical character: {string.digits}"
            
        return True, None # If it passes, return true, and nullify the error element
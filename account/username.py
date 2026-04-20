# username.py
# @author Allen Russell
# @date created: 2/18/26
#
# This class implements the username child domain, applying the constraints and keeping parameters within valid bounds.


# Imports the needed libraries and dependencies
import string


# The username class
class Username:
    
    
    
    # The username constructor
    #
    # The username can consist of letters, numbers, and two symbols (_ and .)
    #
    # @param username: a string username
    #
    # @require username: Username is validated
    #
    # @ensure username is set after validation
    def __init__(self, username):
            
        # Validates username through a helper function and returns a tuple with the boolean
        # and possible error if any, otherwise it is Null. This is done so that changeUsername()
        # does not crash the system when validating the new username to change to.
        check = Username.validateUsername(username)
            
        # The username is valid, so set the new username
        if check[0]:
            #Store the valid username
            self.username = username
        
        # The username is invalid, so return an error
        else:
            raise TypeError(check[1]) # | account_controller needs to print this message to user in webpage |
        


# The special methods: __str__ and __repr__ for use in displaying the user's username
    
    # __repr__ method
    #
    # @param self
    def __repr__(self):
        return f"Username:{self.username}"
        
        
        
    # __str__ method
    #
    # @param self
    def __str__(self):
        return self.username
    
    

    # Mutator and Accesor methods as needed
    
    # changeUsername()
    #
    # @param self
    # @param newUser: The new username to change to
    #
    # @require newUser should not be self | Don't change username to be the same
    #
    # @ensure newUser is run through the constraints and boundaries for a username
    # @ensure Username is changed before returning true
    def changeUsername(self, newUser):
            
        # Username should be changed to a new username, not the same one.
        if self.username == newUser:
            return False, "New username must be different" # Returns false under assumption of making multiple username change attempts.    
        
        # Checks to ensure that the new username is a valid username before setting it
        check = Username.validateUsername(newUser)
        
        # The new username is valid, so set the new username
        if check[0]:
            # Sets the new username, then returns true to indicate a successful change.
            self.username = newUser
            return True, "Successfully changed." # | account_controller needs to print this message to user in webpage |
        
        #The new username is invalid, so return false and the error
        else:
            return False, check[1] # | account_controller needs to print this message to user in webpage |
        
    

    # verifyUsername()
    #
    # @param self
    # @param otherUser: The attempted username
    #
    # @require otherUser: String object
    # @require otherUser: Must not be empty
    #
    # @ensure Usernames match before returning true
    def verifyUsername(self, otherUser):
        
        # Should otherPass not meet the string requirement:
        if not isinstance(otherUser, str):
            return False # Returns false under assumption of making multiple username attempts
        
        # Should otherPass be an empty string:
        if not otherUser:
            return False # Returns false under assumption of making multiple username attempts
        
        # Compare the attempted username with the username stored and return the result
        return self.username == otherUser



    # validateUsername()
    #
    # Helper function for validating constraints and boundaries and it returns a tuple so that
    # errors can still be specified without breaking the system during a username check.
    #
    # @param username: Username to be validated
    #
    # @require username: String object
    # @require username: 8 <= length <= 12
    # @require username: must not contain whitespace
    # @require username: should username contain special characters, it must be a '_' or a '.'
    #
    # @ensure True or False is returned as well as the error, if any.
    def validateUsername(username):
                
        # Should username not meet the string requirement:
        if not isinstance(username, str):
            return False, "New Username must be a string." 
        
        # Should username not meet the length requirement:
        if len(username) < 8 or len(username) > 12:
            return False, "New Username must be 8 to 12 characters long." 
        
        # Should username contain spaces or be empty:
        if any(char.isspace() for char in username) or not username:
            return False, "New Username must not be empty or contain spaces." 
        
        # Should username contain special characters, ensure it's a '_' or a '.':
        for char in username:
            if not (char.isalnum() or char in {'_', '.'}):
                return False, "New Username should only contain a '_' or a '.', no other special characters."
            
        return True, None # If it passes, return true, and nullify the error element

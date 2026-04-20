# Account.py
# @author Allen Russell
# @date created: 2/18/26
#
# This class implements the account parent domain, connecting the username and password child domain.
# It is also in charge of creating accounts then storing them.


# Imports the needed libraries and dependencies
import uuid
from account.pet import Pet
from account.username import Username
from account.password import Password


# The Account class
class Account:
    
    
    
    # The Account constructor
    #
    # The account creates a username and password, and associates it with a User ID for storing to the
    # database
    #
    # @param username: a string username
    # @param password: a string password
    # @param userID: Specific to authentication | A given user's ID
    # @param hpass: Specific to authentication | A given hash for a password
    #
    # @require username must be a valid username
    # @require password must be a valid password
    # @require username: must be a Username object before storing
    # @require password: must be a Password object before storing
    #
    # @ensure username is properly set
    # @ensure password is properly set
    # @ensure password's hash = hpass if any
    # @ensure user ID = uid if any, else assign one
    def __init__(self, username, password, hpass = None):
        
        # Grab the boolean and possible error
        userCheck = Username.validateUsername(username)
        passCheck = Password.validatePassword(password)
        
        #Validate that both are a valid username and password
        if userCheck[0] and passCheck[0]:
            self.username = Username(username)
            self.password = Password(password)
            self.pets = [] # empty list for adding pets to the account later
            
            if hpass is not None:
                self.password.p_hash = hpass
                
        else:
            print(f"Error: {userCheck[1] if not userCheck[0] else passCheck[1]}.")
            raise TypeError(f"{userCheck[1] if not userCheck[0] else passCheck[1]}.") # | account_controller needs to print this message to user in webpage |



    # The special methods: __str__ and __repr__ for use in displaying the user's account
    
    # __repr__ method
    #
    # @param self
    def __repr__(self):
        return f"ID: {self.uid} | Username:{self.username} | {repr(self.password)} | Pets: {self.pets}"
        # Unformatted Pets for simple dev purposes and accessing in DB, structuring of inner info not vital
        
        
        
    # __str__ method
    #
    # @param self
    def __str__(self):
        # Starts constructing string for formatted displaying
        str_acc = f"Account: {self.username}\nAccount ID: {self.uid}\n\n"
        
        # Iterates the list of Pets to format the string
        str_acc += "Registered Pet Profiles:\n"
        i = 1 # for adding ( Pet #1, #2, #3... ) structuring
        for pet in self.pets:
            str_acc += f"\t Pet #{i}: {pet.getName()}"
            # Provides structured string formatting for pet and adds it to the str_acc
            str_acc += f"\t\tSpecies: {pet.getSpecies()}"
            str_acc += f"\t\tAge (years): {pet.getAge()}"
            
        # Return the constructed string
        return str_acc



    # Mutator and Accesor methods as needed
    
    # Authenticator for Account logins
    #
    # @param self
    # @param username: Attempted username for authenticating
    # @param password: Attempt password for authenticating
    #
    # @ensure username and password matches before confirming authentication
    def authenticate(self, username, password):
        #Verify username and password:
        if not self.username.verifyUsername(username) or not self.password.verifyPassword(password):
            print(f"User {username} made a failed attempt to authenticate.")
            return False, "Invalid credentials given." # | account_controller needs to print this message to user in webpage |
        else:
            print(f"User {self.username} has been successfully authenticated.")
            return True, "Login successful." # | account_controller needs to print this message to user in webpage |
        
        
        
    # Mutator for adding Pet class objects to the Pet list of the account
    #
    # @param self
    # @param name: Name of the pet being added
    # @param species: Species of reptile that pet is
    # @param age: (in years) The age of the pet
    #
    # parameters are checked by Pet class, so just pass the parameters
    #
    # @ensure pet is added to list
    #
    # @return true or false, and resulting message for which case | success or fail
    def addPet(self, name, species, age):
        # Try to add the pet, if it works, return True and show the success msg.
        try:
            # Creates the pet object (pet profile : user)
            pet = Pet(name, species, age)
        
            # Adds the new pet to the Account's list and return True and success message
            self.pets.append(pet)
            return True, "Pet added successfully."
        # Else, return the error message and False if it failed
        except TypeError as err:
            return False, str(err)

    
    # Mutator for removing Pet class objects to the Pet list of the account
    #
    # @param self
    # @param pet_name: The name of the pet being removed
    #
    # @ensure pet is removed from the list
    #
    # @return true or false, and resulting message for which case | success or fail
    def removePet(self, pet_name):
        # Iterates list of pets for the pet with matching name:
        for pet in self.pets:
            if pet.getName() == pet_name:
                self.pets.remove(pet)
                return True, f"Successfully removed {pet_name}."
        # If pet wasn't able to be removed, return the Error and False
        return False, f"Error removing {pet_name}"
    
    
    
    # Internal accessor for the username
    #
    # @param self
    #
    # @return username
    def _getUsername(self):
        return str(self.username)
    
    
    
    # Internal accessor for the pet list
    #
    # @param self
    #
    # @return list of pets
    def _getPetList(self):
        return self.pets
    
    
    
    # Internal accessor for the password
    #
    # For storing to the account database
    #
    # @param self
    #
    # @return password
    def _getPassword(self):
        return self.password.p_hash
    
    
    
    # Internal accessor for the user ID
    #
    # @param self
    #
    # @return user ID
    def _getUserID(self): # Only the application/database needs to access it, user does not need to manually get it
        return str(self.uid)
    


    # Mutator for the username
    #
    # @param self
    # @param username
    #
    # @ensure username is successfully changed before returning true
    def changeUsername(self, username):
        #Pass the username to the Username class for validation, afterwards storing the results for handling
        check = self.username.changeUsername(username)
        
        #See if it was successful in changing, otherwise return the error
        if check[0]:
            print(f"Username changed to: {self.username}")
            return True, check[1] # | account_controller needs to print this message to user in webpage |
        else:
            print(f"{self.username} attempted a username change")
            return False, check[1] # | account_controller needs to print this message to user in webpage |
        
        
        
    # Mutator for the password
    #
    # @param self
    # @param curr_pw
    # @param new_pw
    #
    # @ensure password is successfully changed before returning true
    def changePassword(self, curr_pw, new_pw):
        #Pass the password to the Password class for validation, afterwards storing the results for handling
        check = self.password.changePassword(curr_pw, new_pw)
        
        #See if it was successful in changing, otherwise return the error
        if check[0]:
            print(f"Password for User {self.uid} changed to: {repr(self.password)}")
            return True, check[1]
        else:
            return False, check[1]

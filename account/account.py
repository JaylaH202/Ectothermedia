# account.py
# @author Allen Wittika
#
# Connects the entire modular package for functionality within the application
# for establishing accounts.


# Imports
from .username import Username
from .password import Password
from .pet import Pet
import bcrypt


# Account.py
#
# @param username
# @param password
#
# @ensure if success, initialize the account's pet container
# @ensure error, if any, is returned to the user during application runtime
class Account:


    def __init__(self, username, password):

        try: # try-except for error displaying to the user
            # parameters are validated within object constructors
            self.username = Username(str(username.strip()))
            self.password = Password(str(password.strip())) # only stores the hashed password
            self.pets = [] #initialize empty list for the accounts' container of pets

        except (ValueError, TypeError) as e:
            #passes the raised error to the framework for displaying
            raise e # e - specific error related to either username or password




    # For logging in the user to verify proper authentication
    def authenticate(self, username, pass_attempt):
        if self.username._username == username:
            return bcrypt.checkpw(pass_attempt.encode(), self.password._passhash)
        else:
            return False
    
    
    
    
    # Used to display user info
    def getUsername(self):
        return str(self.username)


    

    # Used in Pet profile entry
    def getPets(self):
        return self.pets




    # Used in DB entry
    def getHash(self):
        return self.password._passhash.decode('utf-8')
    
    
    
    
    # For changing username 
    #
    # -- reauthenticates to prevent hijacked session keys from changing account info
    def changeUsername(self, new_user, pass_attempt):
        if self.authenticate(self.username._username, pass_attempt):
            self.username.update(new_user)
            return True
        else:
            return False




    # For adding a pet
    #
    # @param name
    # @param age
    # @param gender
    # @param species
    #
    # @ensure if pet succeeds, add the pet
    # @ensure error, if any, is returned to the user during application runtime
    def addPet(self, name, age, gender, species):

        try: # try-except for error displaying to the user
        # parameters are validated within object constructors
            pet = Pet(name, int(age), gender, species) # create pet - pet tests constraints
            self.pets.append(pet) # append the created pet to acc's list.
            return True

        except (ValueError, TypeError) as e:
            # passes the raised error to the framework for displaying
            raise e  # e - specific error related to pet variables




    # For removing a pet
    #
    # @param pet
    #
    # @ensure if pet found, remove pet
    def removePet(self, name, species):
        for pet in self.pets:
            if pet.name == name and pet.species == species: # pet found
                self.pets.remove(pet) # pet removed
                return True # exit true
        return False  # Not able to remove

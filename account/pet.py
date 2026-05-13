# pet.py
# @author Allen Wittika
#
# Handles the pet parameter handling as well as assigning the pet and modifying pet.


class Pet():


    #
    # @param name
    # @param age
    # @param gender
    # @param species
    #
    # @require name is an alphabetical string and is between 8 and 12 characters
    # @require age is number and < 100 (none of our species in DB age past this)
    # @require gender is either an F or M
    # @require species is an alphabetical string and =< 36 characters
    #
    # @ensure variables are properly set
    def __init__(self, name, age, gender, species):

        if not name.isalpha() or 3 > len(name) > 12:
            raise TypeError("Error: Pet's name must be alphabetical and between 3 and 12 characters")

        if age < 0 or age > 100:
            raise TypeError("Error: Pet's age must be between 0 and under 100")

        # should not occur error-wise since check-box determines this input and input can be empty
        if gender is not None and gender not in ["M", "F"]:
            raise TypeError("Error: Pet's gender must be 'M' or 'F' if filled out")

        if not species.isalpha() and 0 > len(species) > 36:
            raise TypeError("Error: Pet's species must be a 36-character max alphabetical string, and cannot be empty.")

        self.name = name
        self.age = age
        self.gender = gender
        self.species = species




    # Mutator for updating the name when request to change it is made.
    # @param new name
    #
    # @require parameter is rechecked
    #
    # @ensure name is not curr name
    def update_name(self, name):
        # Don't make new username the current username
        if name is self.name:
            raise ValueError(f"{name} already has this name..")
        # Retest the constraint
        if not name.isalpha() and 8 > len(name) > 12:
            raise TypeError("Pet's name must be alphabetical and between 8 and 12 characters")
        # Calls constructor to call the constraints to prevent incorrect injection
        self.name = name




    # Mutator for updating the age when request to change it is made.
    # @param new age
    #
    # @require parameter is rechecked
    #
    # @ensure age is not curr age
    def update_age(self, age):
        # Don't make new username the current username
        if age is self.age:
            raise ValueError(f"{self.name} is already {age} years old..")
        # Retest the constraint
        if age < 0 or age > 100:
            raise TypeError("Pet's age must be between 0 and under 100")
        # Calls constructor to call the constraints to prevent incorrect injection
        self.age = age

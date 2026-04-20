# Pet.py
# @author Allen Russell
# @date created: 3/31/26
#
# This class implements the pet child domain, which implements functions for
# storing data on an individual reptilian pet


# The Pet class
class Pet:
    
    
    # Pet Constructor
    #
    # Creates the individual Pet data object
    #
    # @param name: Pet's name: String
    # @param species: Pet's species: String: Immutable
    # @param age: Pet's age: Int
    #
    # @require name is a string
    # @require species is a string
    # @require age is a string
    def __init__(self, name, species, age):
        
        # Should name not be a string:
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        
        # Should species not be a string:
        if not isinstance(species, str):
            raise TypeError("Species must be a string.")
        
        # Should age not be a int or float to convert to int:
        if not (isinstance(age, int) or isinstance(age, float)):
            raise TypeError("Age must be a integer or float for conversion to int.")
        
        # Assigns the values to their respective class variables
        self.name = name
        self._species = species
        self.age = int(age)



    # The special methods: __str__ and __repr__ for use in keeping the password hidden to minimize security risk
    
    # __repr__ method
    #
    # method returns a formatted string with delimiters (;) to seperate
    # the values later for displaying
    #
    # @param self
    def __repr__(self):
        return f"{self.name}; {self._species}; {self.age}"
        
        
        
    # __str__ method
    #
    # methods primarily for readability while testing
    #
    # @param self
    def __str__(self):
        return f"Name: {self.name}\n\tSpecies: {self._species}\n\n\t{self.name} is {self.age} years old."
        


    # Mutator and Accesor methods as needed
    
    # Accessor for the pet's name
    #
    # @param self
    #
    # @return name
    def getName(self):
        return self.name
    
    
    
    # Accessor for the pet's species
    #
    # @param self
    #
    # @return species
    def getSpecies(self):
        return self._species
    
    
    
    # Accessor for the pet's age
    #
    # @param self
    #
    # @return age
    def getAge(self):
        return self.age
    
    
    
    # Mutator for the pet's name
    #
    # @param name: new name
    #
    # @require new name is not already curr name
    #
    # @ensure name is properly set to new name
    def changeName(self, name):
        
        # Should new name be current name:
        if name is self.name:
            return False, "Pet's new name should be different."
        # Otherwise, set the new name
        else:
            self.name = name
            return True, "Successfully changed."
        
        

    # Mutator for the pet's age
    #
    # @param age: new age
    #
    # @require new age is not already curr age
    #
    # @ensure age is properly updated to new age
    def updateAge(self, age):
        
        # Should new age be current age:
        if age is self.age:
            return False, "Pet's updated age should be different."
        # Otherwise, set the new name
        else:
            self.age = age
            return True, "Successfully updated."

# username.py
# @author Allen Wittika
#
# Handles the username parameter handling as well as assigning the username and modifying username.


class Username:


    #
    # @param username
    #
    # @require username between 8 and 12 characters
    # @require username can only contain a '_' or '."
    # @require username is, otherwise, only alphanumerical
    #
    # @ensure only username is associated after validity
    def __init__(self, username):

        if username is None:
            raise ValueError("Error: Username cannot be empty..")

        if not (8 <= len(username) <= 12):
            raise ValueError("Error: Username must be between 8 and 12 characters..")

        for char in username:
            if not char.isalnum() and char not in "_.":
                raise TypeError("Error:  Username must be alphanumerical but can contain a '_' or '.'..")

        self._username = username




    # Special methods for displaying username. // No difference in printing
    def __str__(self):
        return f"@{self._username}"
    def __repr__(self):
        return f"@{self._username}"




    # Mutator for updating the username when request to change it is made.
    # @param new username
    #
    # @ensure username is not curr username
    def update(self, username):
        if username is self._username: # Don't make new username the current username
            raise ValueError("Error: You already have this username..")
        # Calls constructor to call the constraints to prevent incorrect injection
        self._username = Username(username)

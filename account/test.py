# Pet_profile implementation
#
# Allen Wittika
# Final portion

#imports
from user.account import Account
from flask import Flask, render_template, request, redirect, url_for


# Start the app
app = Flask(__name__)
app.secret_key = "development_secret_key"


acc = Account("Picklez36", "I.lovep!kl3")
acc.addPet('Robert', 2, 'M', 'Turtle')
acc.addPet('Suzie', 5, 'F', 'Lizard')
acc.addPet('Rex', 8, 'F', 'Gecko')


@app.route('/profile')
def profile():
    # Variables must be passed as keyword arguments (name=value)
    return render_template('profile.html', username=acc.getUsername(), pets=acc.getPets())


@app.route('/profile/add_pet', methods=['POST'])
def add_pet_route():
    try: # Try-except for displaying error to user
        # Extract data from the form
        name = request.form.get('name')
        age = int(request.form.get('age'))
        gender = request.form.get('gender')
        species = request.form.get('species')
        # Call the Account method to validate and add
        acc.addPet(name, age, gender, species)
        return redirect(url_for('profile'))
    
    except (TypeError, ValueError) as e:
        # Pass the validation error back to the profile page
        return redirect(url_for('profile', error=str(e)))
        #pass the error to profile, use req.geterror shit to grab the error then assign to err and flash that on reload if any




@app.route('/profile/remove_pet/<name>/<species>', methods=['POST'])
def removePet(name, species):
    acc.removePet(name, species)
    return redirect(url_for('profile'))




#Executes the DB loader and controller
if __name__ == "__main__":
    app.run(debug=True, port=9999, use_reloader=False, use_debugger=False) # Last two params are specific to Thonny clashing with Flask

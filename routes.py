# routes.py
#
# @author Jayla Hall & Allen Russell
#
# Handles the routing and logic for each page view.
'''
Commented app stuff out to work on PDF
'''

# Imports the needed libraries and dependencies
#from account.account import *
from flask import Flask, render_template, request, redirect, url_for
from psycopg2 import connect
#from flask_weasyprint import render_pdf, HTML


#connect to database
# we need some sort of secruity here for database connection password and username, but for now we will just hardcode it in the code
#conStr = "host=csdept dbname=capstone2 user=cap2user password=dbx!2917"
#conn = connect(conStr)


# Creates the webframe through flask
app = Flask(__name__)

# Displays the main landing page (homepage.html)

@app.route("/")
def homepage():
    return render_template('homepage.html')



# Displays a list of animals based on selected category
# Example URLs:
#   /speciesList/Lizards
#   /speciesList/Geckos
#   /speciesList/Shelled
#
# Queries database and passes results to speciesList.html
@app.route("/speciesList/<name>")
def speciesList(name):

    # Create cursor to execute SQL queries
    dbCursor = conn.cursor()

    # Special case:
    # "Shelled" category includes both tortoises and turtles
    if name == "Shelled":
        dbCursor.execute("SELECT english_name FROM overview WHERE animal_class IN (%s,%s)",("Tortoise", "Turtle"))
    else:
        # Standard case: filter by exact category
        dbCursor.execute("SELECT english_name FROM overview WHERE animal_class = %s", (name,))

    # Retrieve all matching rows
    rows = dbCursor.fetchall()

    #Close cursor after query
    dbCursor.close()
    
    # Send data to template:
    # - animals: list of species names
    # - category: used for page heading/display
    return render_template('speciesList.html', animals=rows, category=name)


#Indiviual Species Page

# Displays detailed information about ONE animal
# URL example: /info/Leopard Gecko
#
# Pulls data from multiple tables:
#   - overview (general info)
#   - diet_requirements
#   - environmental_requirements
#   - enclosure_details
@app.route("/info/<name>")
def infoPage(name):
    dbCursor = conn.cursor()
    
    #overview row 
    dbCursor.execute("SELECT * FROM overview WHERE english_name = %s;",(name,))
    
    animal = dbCursor.fetchone()

    #scientific name from overview
    sci_name = animal[3]
    
     #diet
    dbCursor.execute("SELECT * FROM diet_requirements WHERE scientific_name = %s", (sci_name,))
    diet = dbCursor.fetchone()
    #environment
    dbCursor.execute("SELECT * FROM environmental_requirements WHERE scientific_name = %s", (sci_name,))
    environment = dbCursor.fetchone()
    #enclosure
    dbCursor.execute("SELECT * FROM enclosure_details WHERE scientific_name = %s", (sci_name,))
    enclosure = dbCursor.fetchone()
    
    dbCursor.close()

    # Pass all retrieved data to the info.html template for rendering
    return render_template('info.html',animal=animal, diet=diet,environment=environment,enclosure=enclosure)

# Generates a downloadable PDF version of the animal info page
# Uses the SAME data as infoPage route
# Flow:
#   1. Query database
#   2. Render HTML template
#   3. Convert HTML to PDF
@app.route("/download/<name>")
def download(name):
	
    dbCursor = conn.cursor()
    
    #Same logic as infoPage

    #overview row 
    dbCursor.execute("SELECT * FROM overview WHERE english_name = %s;",(name,))
    
    animal = dbCursor.fetchone()
    #scientific name from overview
    sci_name = animal[3]
    
     #diet
    dbCursor.execute("SELECT * FROM diet_requirements WHERE scientific_name = %s", (sci_name,))
    diet = dbCursor.fetchone()
    #environment
    dbCursor.execute("SELECT * FROM environmental_requirements WHERE scientific_name = %s", (sci_name,))
    environment = dbCursor.fetchone()
    #enclosure
    dbCursor.execute("SELECT * FROM enclosure_details WHERE scientific_name = %s", (sci_name,))
    enclosure = dbCursor.fetchone()
    
    dbCursor.close()
    
    # Render HTML template as a string
    html = render_template('info.html',animal=animal, diet=diet,environment=environment,enclosure=enclosure)
    
    # Convert HTML string into a downloadable PDF
    return render_pdf(HTML(string=html))
	

# DEBUGGING | DEBUGGING | DEBUGGING
# The method for loading the login page and handeling the page functionality
# @author Allen W.
# @date 4/14/26

@app.route("/register", methods=['GET', 'POST'])
def register():
    cur = conn.cursor() #db cursor for table navigating / accessing
        # If user submits a registration request
    if request.method == 'POST':
        un = request.form.get('username')
        pw = request.form.get('password')
        
        # Return an error if either field is empty, user needs to submit both fields
        if not un or not pw:
            return render_template('register.html', error_msg="Error > Both fields are required to register.")
        # Return an error if the username is already in use
        if checkUsername(un):
            return render_template('register.html', error_msg="Error > Username is already in use.")
        
        # A try-catch is used to ensure an account creation failure will not crash the webpage, this was used
        # over implementing a static method in Account to use for creating accounts here.
        try: # If success: Connect the Table and add the account
            acc = Account(un, pw) # Attempts to safely create the account
            
            #Adds accounts to table | reminder: remove uid
            cursor = conn.cursor() 
            cursor.execute('INSERT INTO accounts (username, password) VALUES (%s, %s)', (un, acc._getPassword())) 
            conn.commit() # Save the changes to the database
            
            return redirect(url_for('login'))
            
        #If error: retry registration, and display the error to the user 
        except TypeError as err:
            return render_template('register.html', error_msg=str(err))
    # If a registration is not submitted, then assume the user requested to redirect to the registration page. 
    return render_template('register.html')




# WIP | WIP | WIP
# The method for loading the login page and handeling the page functionality
# @author Allen W.
# @date 4/14/26
@app.route("/login", methods=['GET', 'POST'])
def login():
    cur = conn.cursor() #db cursor for table navigating / accessing
    # If user submits a registration request
    if request.method == 'POST':
        un = request.form.get('username')
        pw = request.form.get('password')
    
        # Return an error if either field is empty, user needs to submit both fields
        if not un or not pw:
            return render_template('login.html', error_msg="Error > Both fields are required to log in.")
        
        cur = conn.cursor()# Connect the cursor
        # Attempt to find an account with the same username as the attempted
        cur.execute('SELECT password FROM accounts WHERE username = %s', (un,))
        result = cur.fetchone()
        # If account with username match found, determine if passwords match
        if result is not None:
            t_pass = result[0]
            # Create the temporary account
            db_acc = Account(un, pw, t_pass)
            
            # Authenticate given credentials with those in the DB, and let the user know if success or fail
            auth = db_acc.authenticate(un, pw)
            if auth[0]: # Successful authentication
                # | Temp code for ensuring auth works |
                print(auth[1])
                return f"<h1>Success!</h1><p>{auth[1]}</p><a href='/login'>Back to Login</a><a href='/register'>Back to Register</a>"
            # Else, retry and give the user an error message
            else:
                return render_template('login.html', error_msg=f"Error > {auth[1]}.")

        # Else, return an invalid account error
        else:
            return render_template('login.html', error_msg="Error > No account exists with those credentials.")
    # No post, load page to get login credentials
    return render_template('login.html')    



# This method checks to check if a username is in use before registering accounts in register().
# @author Allen W.
# @date 4/14/26
def checkUsername(un):
    cur = conn.cursor() #establish the cursor for traversing
    cur.execute('SELECT 1 FROM accounts WHERE username=%s',(un,))
    result = cur.fetchone()
    return result is not None
    
    
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=8087)

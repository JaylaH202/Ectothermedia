# routes.py
#
# @author Jayla Hall & Allen Russell
#
# Handles the routing and logic for each page view.


# Imports the needed libraries and dependencies
#from account.account import *
from flask import Flask, render_template, request, redirect, url_for, session
from psycopg2 import connect
from dotenv import load_dotenv
import os
from user.account import Account

#from flask_weasyprint import render_pdf, HTML


#connect to database
# we need some sort of secruity here for database connection password and username, but for now we will just hardcode it in the code
#conStr = "host=csdept dbname=capstone2 user=cap2user password=dbx!2917"
#conn = connect(conStr)
# Load the variables from the .env
# Find the exact path to the .env file | Had issues with just load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# THIS IS WORKING | DO NOT MODIFY | RUN THROUGH TERMINAL
#
# Creates the framework through flask and grabs the .env factors
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
try:
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    print("Database connected successfully!")
except Exception as e:
    print(f"Error: Trouble connecting to database: {e}")
    conn = None


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
	
# The method for loading the login page and handeling the page functionality
# @author Allen W.
# @date 4/14/26

@app.route("/register", methods=['GET', 'POST'])
def register():

    # If user submits a registration request
    if request.method == 'POST': 
        cursor = conn.cursor() # connect to cursor
        un = request.form.get('username')
        pw = request.form.get('password')
        
        if not un or not pw: # Fields should not be blank when signing up or logging in
            return render_template('register.html', error_msg="Error: Both fields needed.")
        cursor.execute("SELECT 1 FROM accounts WHERE username = %s", (un,)) # Is username already taken?
        if cursor.fetchone():
            return render_template('register.html', error_msg="Error: Username already taken.")
        
        try: # If success: Connect the Table and add the account
            acc = Account(un, pw) # Attempts to safely create the account
            cursor.execute('INSERT INTO accounts (username, password) VALUES (%s, %s) RETURNING user_id', (un, acc.getHash())) #Adds account to table
            # Retrieve the ID from the cursor
            user_id = cursor.fetchone()
            user_id = user_id[0]            
            conn.commit() # Save the changes to the database
            # Session implementation
            session.clear()           # Clear any old session data
            session['user_id'] = user_id # actually saves session via framework
            session['username'] = un  #for display purpose
            return redirect(url_for('homepage')) # Return user to Home
            
        #If error: retry registration, and display the error to the user 
        except (ValueError, TypeError) as e:
            conn.rollback() # RESET THE CONNECTION
            cursor.close()  # Close here            
            return render_template('register.html', error_msg=str(e))
        
    # If a registration is not submitted, then assume the user requested to redirect to the registration page. 
    return render_template('register.html')




# The method for loading the login page and handeling the page functionality
# @author Allen W.
# @date 4/14/26
@app.route("/login", methods=['GET', 'POST'])
def login():

    # If user submits a registration request
    if request.method == 'POST':
        cursor = conn.cursor() # connect to cursor
        un = request.form.get('username')
        pw = request.form.get('password')
    
       
        if not un or not pw: # Return an error if either field is empty, user needs to submit both fields
            return render_template('login.html', error_msg="Error: Both fields are required to log in.")
        cursor.execute('SELECT user_id, password FROM accounts WHERE username = %s', (un,))  # Attempt to find an account with the same username as the attempted
        result = cursor.fetchone()
        
        # If account with username match found, determine if passwords match
        if result:
            t_uid = result[0]   # user_id
            t_hash = result[1].encode('utf-8')  # hashed password
            t_acc = Account(un, pw) # temporary account
            t_acc.password._passhash = t_hash # override hash for valid authentication 
            
            if t_acc.authenticate(un, pw):
                # start the session
                session.clear()
                session['user_id'] = t_uid
                session['username'] = un
                cursor.close()
                return redirect(url_for('homepage')) # Redirect to homepage on login
            
            else: # error, try again
                cursor.close()
                return render_template('register.html', error_msg="Error: Invalid account credentials")                
    
        # error, try again
        else:
            return render_template('login.html', error_msg="Error: No account exists with those credentials.")
    
    # No post, load page to get login credentials
    return render_template('login.html')    
    
    
    
# Integrate button on homepage for logging out to pair with profile button
def logout():
    session.clear() # Wipes the user_id and username
    return redirect(url_for('homepage'))    




# Integrate later, navigate via Profile button on homepage
@app.route("/profile", methods = ['GET', 'POST'])
def profile():
    if 'username' not in session: #Prevents query injection to access profile info
        return redirect(url_for('login'))
    pass #integrate the profile later




if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=8050)

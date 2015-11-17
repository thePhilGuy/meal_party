#!/usr/bin/env python2.7

"""
Philippe-Guillaume Losembe - pvl2109
Tommy Orok - to2240
2015
Expanded on Columbia W4111 Intro to databases
Example webserver by eugene wu 2015

To run locally

    python server.py

Go to http://localhost:8111 in your browser
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
import factual_wrapper
from pprint import pprint

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

app.debug = True

# 
# Connect to the database on azure virtual machine
# postgresql://USER:PASSWORD@w4111db1.cloudapp.net:5432/proj1part2
#
DATABASEURI = "postgresql://azureuser@localhost:5432/mealparty"

#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass

#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a POST or GET request
# 
@app.route('/', methods=['GET', 'POST'])
def index():
  """
  MealParty landing page
  """
  # DEBUG: this is debugging code to see what request looks like
  print request.args

  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html")

@app.route('/area/<req_zip>')  
def area(req_zip):
  """
  Second map at specific area
  """

  # Get restaurants info for area
  cuisine_results, restaurant_results = factual_wrapper.get_restaurants_by_zip(req_zip)

  # Check if we already have area data 
  # query : select count(*) from area where zip=req_zip
  area_cursor = g.conn.execute("SELECT COUNT(*) FROM Area WHERE zip=\'" + req_zip + "\';")
  area_count = area_cursor.fetchone()['count']
  area_cursor.close()

  # This is the first time this area was requested
  if area_count < 1:
    # Insert it into the database
    g.conn.execute("INSERT INTO Area VALUES (\'" + req_zip + "\');")

    # Store in database
    for element in restaurant_results:
      insert_query = text(
        "INSERT INTO Restaurant (zip, name, website_url, cuisine)"
        "VALUES (:z, :n, :w, :c);"
        )
      g.conn.execute(insert_query, z=element["zip"], n=element["name"], w=element["website"], c=', '.join(element["cuisines"]))

  # Google API will only need lat/long/name
  restaurant_locations = [ dict(latitude=r['latitude'], longitude=r['longitude']) 
                           for r in restaurant_results ]

  context = dict(zip=req_zip, restaurants=restaurant_locations, cuisines=cuisine_results)

  return render_template("area.html", **context)

@app.route('/party', methods = ['POST'])
def party():
  """
  We receive a post request to make a party happen
  """

  proposal = request.get_json(force = True)

  # Make sure we have this user in our database
  person_id = 0;
  person_cursor = g.conn.execute("SELECT * FROM Person WHERE email=%s", proposal['email'])
  if person_cursor.rowcount < 1: 
    # Person does not exist, add them
    person = g.conn.execute("INSERT INTO Person (email, phone) VALUES (%s, %s)", (proposal['email'], proposal['phone']))
    print person
    person.close()
    person_id = g.conn.execute("SELECT * FROM Person WHERE email=%s", proposal['email']).fetchone()['id']
  else: 
    # Person already exists, get id
    person_id = person_cursor.fetchone()['id']
  person_cursor.close()

  print "Person id: ", person_id

  # Insert proposal into database
  insert_query = text(
    "INSERT "
    "INTO Proposal (uid, cuisine, zip, from_time, until_time, ideal_size, minimum_size, maximum_size, pending)"
    "VALUES (:p, :c, :z, :f, :u, :i, :n, :m, TRUE);" )
  g.conn.execute(insert_query, 
    p=person_id,
    c=", ".join(proposal["cuisines"]), 
    z=proposal["zip"], 
    f=proposal["from"], 
    u=proposal["until"], 
    i=proposal["ideal_size"], 
    n=proposal['min_size'], 
    m=proposal['max_size'])

  proposal_id = g.conn.execute("SELECT id FROM Proposal ORDER BY id DESC LIMIT 1").fetchone()['id']
  proposal["id"] = proposal_id

  msg = "We know you want to party at %s, we'll let\
          you know if any matches come up!!"
  
  sendMail(proposal['email'], msg)

  prop_hndler(proposal)


  return render_template("index.html"), 201

# Handling new proposal #########################################
def sendMail(toaddr, message):
  fromaddr = 'tommy@lawnearme.com'
  toaddrs  = toaddr
  msg = message
  username = 'tommy@lawnearme.com'
  password = 'lathamtich3w'
  server = smtplib.SMTP('smtp.gmail.com:587')
  server.ehlo()
  server.starttls()
  server.login(username,password)
  server.sendmail(fromaddr, toaddrs, msg)
  server.quit()


def timcompat(res, proposal):
  return proposal["from"] <  res["until_time"]

sharedCuisine = ""

def commonCuisine(res, proposal):
  try:
      g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None



  rescu = res["cuisine"].split(", ")
  procu = proposal["cuisines"].split(", ")
  for element in rescu:
    for element2 in procu:
      if element == element2:
        sharedCuisine = element
        return true
  return false

def findRest(cuisine):
  args = (cuisine)
  rests = g.conn.execute("SELECT name FROM Restaurant \
          WHERE cuisine = %s", args)
  return rests[0]



def prop_hndler(prop):
  mealcursor = g.conn.execute("SELECT * FROM Meal me, Matched ma, Proposal p\
               WHERE me.me_id = ma.mid AND \
               ma.pid = p.id AND me.pending = TRUE;")  #for pending meals

  groupfound = -1
  for result in mealcursor:
    if (prop.zip == result["zip"] and timcompat(result, prop) and commonCuisine(result, prop) and result["minimum_size"] <= prop.ideal_size  and prop.ideal_size <= result["max_size"]):  #prop's ideal needs to be between the min amd max of result
      if (result.next["me_id"] == result["me_id"]):  #part of a group
        continue
      else:
        args = (result["me_id"], prop["id"])
        g.conn.execute("INSERT INTO Matched\
                VALUES (%s, %s);", args)  #find out how to format string safe way and prevent injections on piazza)
        
        args = (result["me_id"])
        g.conn.execute("UPDATE Meal\
                SET size = size + 1\
                WHERE me_id = %s ;", args)  #or maybe should just give result["me_id"]

        groupfound = result["me_id"]

  if (groupfound == -1):
    #make a meal out of this proposal
    args = (1, prop["ideal_size"], prop["from"])
    g.conn.execute("INSERT INTO Meal(size, ideal_size, mtime, pending)\
            VALUES (%i, %s, %s);",args )
  else:
    args = (groupfound)
    meals = g.conn.execute("SELECT size, ideal_size FROM Meal\
                WHERE me_id = %i;", args)

    if meals[0] == meals[1]:
      args = (groupfound)
      g.conn.execute("UPDATE Meal\
              SET pending = false \
              WHERE me_id = %i;", args)
      mealcursor = g.conn.execute("SELECT * FROM Meal me, Matched ma, Proposal p, Person per\
                     WHERE %i=me.me_id AND me.me_id = ma.mid AND \
                     ma.pid = p.id AND p.uid = per.id;", args)
      
      #FIND RESTAURANT TO MATCH CUISINE
      chosen_restaurant = findRest(sharedCuisine)

      for record in mealcursor:
        sendMail(record["email"], """Time: {time}\nRestaurant:  {rest}""".format(time = record["mtime"], rest = chosen_restaurant))


  meals.close()
  mealcursor.close()
#################################################################

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()

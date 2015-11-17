import smtplib


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
	return proposal["from_time"] <  res["until_time"]

sharedCuisine = ""

def commonCuisine(res, proposal):
	rescu = res["cuisine"].split(", ")
	procu = proposal["cuisine"].split(", ")
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
		args = (1, prop["ideal_size"], prop["from_time"])
		g.conn.execute("INSERT INTO Meal(size, ideal_size, mtime, pending)\
						VALUES (%d, %s, %s);",args )
	else:
		args = (groupfound)
		meals = g.conn.execute("SELECT size, ideal_size FROM Meal\
								WHERE me_id = %d;", args)

		if meals[0] == meals[1]:
			args = (groupfound)
			g.conn.execute("UPDATE Meal\
							SET pending = false \
							WHERE me_id = %d;", args)
			mealcursor = g.conn.execute("SELECT * FROM Meal me, Matched ma, Proposal p, Person per\
										 WHERE %d=me.me_id AND me.me_id = ma.mid AND \
							 			 ma.pid = p.id AND p.uid = per.id;", args)
			
			#FIND RESTAURANT TO MATCH CUISINE
			chosen_restaurant = findRest(sharedCuisine)

			for record in mealcursor:
				sendMail(record["email"], """Time: {time}\nRestaurant:  {rest}""".format(time = record["mtime"], rest = chosen_restaurant))


	meals.close()
	mealcursor.close()
	g.conn.close()

#changes:
###############################
# add cuisine to proposal 
# change meal.id to meal.me_id
# add ideal_size to Meal
# add constraint to schema start time <= endtime - 30 min
# save latitude and longitude  to restaurant (maybe)
#
#To DO:
# need to manage group goals, maybe add a goal field in meal
#als oneed to mangage group times!
# also need to manage sizes for whole group
#
# 
#
#

from factual import Factual
from pprint import pprint
factual = Factual('key', 'secret')

def get_restaurants_by_zip(zip):
	# returns a set of cuisines, as well as a list of restaurants
	#		  cuisines, restaurants

	print "asking factual for restaurants in ", zip

	# get data from factual API
	restaurants = factual.table('restaurants-us')
	data = restaurants.filters({'postcode':zip}).data()

	# return objects
	results = []
	cuisines = set()

	# build results
	for i in xrange(20):
		restaurant = dict()
		restaurant['name'] = data[i]['name']
		restaurant['cuisines'] = data[i]['cuisine']
		cuisines.update(restaurant['cuisines'])
		restaurant['zip'] = data[i]['postcode']
		restaurant['price'] = data[i]['price']
		results.append(restaurant)
	# pprint(results)
	print "Set of cuisines in ", zip
	pprint(cuisines)
	return cuisines, results



if __name__ == '__main__':
	get_restaurants_by_zip('10025');
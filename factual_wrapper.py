from factual import Factual
from pprint import pprint
factual = Factual('key', 'secret')

def get_restaurants_by_zip(zip):
	print "asking factual for restaurants in ", zip
	restaurants = factual.table('restaurants-us')
	data = restaurants.filters({'postcode':zip}).limit(20).data()
	results = []
	for i in xrange(20):
		restaurant = dict()
		restaurant['name'] = data[i]['name']
		restaurant['cuisines'] = data[i]['cuisine']
		restaurant['zip'] = data[i]['postcode']
		restaurant['price'] = data[i]['price']
		results.append(restaurant)
	pprint(results)
	return results



if __name__ == '__main__':
	get_restaurants_by_zip('10025');
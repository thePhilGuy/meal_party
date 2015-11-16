from factual import Factual
factual = Factual('key', 'secret')

def get_restaurants_by_zip(zip):
	print "asking factual for restaurants in ", zip
	restaurants = factual.table('restaurants-us')
	data = restaurants.filters({'postcode':zip}).data()
	print(data)

get_restaurants_by_zip('10025');
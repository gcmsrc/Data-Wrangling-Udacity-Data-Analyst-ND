# -*- coding: utf-8 -*-

"""
	This file contains the function used to extract the amenity from the
	'milan' .osm file.

	Module-level variables are:

		parking: regex compile expression to check if a string starts with 'parking'

		tourism_amenity (dict): dictionary of edited mapping of tourism values.

		shop_amenity (list): list of amenity values that need to be categorised as
							 shops.
"""

import re
parking = re.compile(r'^parking')

tourism_amenity = {'aquarium':'aquarium',
                   'artwork':'general_attraction',
                   'attraction': 'general_attraction',
                   'botanical garden':'park',
                   'camp_site':'park',
                   'gallery':'museum',
                   'guest_house':'hotel',
                   'hostel':'hotel',
                   'hotel':'hotel',
                   'information':'tourist_information',
                   'motel':'hotel',
                   'museum':'museum',
                   'picnic_site':'park',
                   'residence':'hotel',
                   'theme_park':'theme_park',
                   'viewpoint':'general_attraction',
                   'zoo':'zoo'}

amenity_shops = ['insurance',
				 'massage',
				 'ice_cream']



def is_parking(amenity):

	"""
		This function is used to check if an amenity is either a parking, a parking_space, or
		a parking entrance.

		Argument:
			amenity (string): variable representing an amenity.

		Returns:
			bool: True if parking. False otherwise.
	"""
	return parking.search(amenity)


def amenity_extract(amenity,shop,tourism):
	"""
		This function is used to evaluate the appropriate amenity.

		Argument:
			amenity (string): amenity value. None otherwise.
			shop (string): shop value. None otherwise.
			tourism (string): touirsm value. None otherwise.


		Returns:
			extraction (dict): correct and formatted amenity dictionary.
				  			   The format is as per the examples belows:
				  			   {'type':'shop', 'goods':'supermarket'}
				  			   {'type':'museum'}
	"""

	extraction = {}

	if tourism in tourism_amenity.keys():
		extraction['type'] = tourism_amenity[tourism]
		return extraction

	elif shop:
		extraction['type'] = 'shop'
		extraction['goods'] = shop

	elif amenity:

		if amenity in amenity_shops:
			extraction['type'] = 'shop'
			extraction['goods'] = amenity

		elif is_parking(amenity):
			extraction['type'] = 'parking'

		else:
			extraction['type'] = amenity

	if extraction != {}:
		return extraction



def amenity_return(amenity_dict):

	"""
		This function is used to extract the correct amenity value.

		Argument:
			amenity_dict (dict): a dictionary containing values for 'amenity', 'shop',
								 and 'tourism' tags. Default values are None.

		Returns:
			dict: return correct and formatted amenity dictionary	
	"""

	amenity = amenity_dict['amenity']
	shop = amenity_dict['shop']
	tourism = amenity_dict['tourism']

	return amenity_extract(amenity,shop,tourism) 




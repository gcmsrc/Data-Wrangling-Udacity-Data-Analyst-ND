
# -*- coding: utf-8 -*-

"""
	This file contains all the functions used to fix and cleanse data
	in the 'milan.osm' file
"""

import re
from titlecase import titlecase

"""
	Module-level variables.

		first_word: regex compile expression to identify first word of a string

		street_types: list of street types in Milan

		post_code: regex compile expression to identify valid postcodes in Milan, i.e.
				   2 follow by any 4 digits.

		

"""
first_word = re.compile(r'^(\w+)')
street_types = ['alzaia', 'bastioni', 'corso', 'foro', 'galleria',
                'largo','passaggio','piazza','piazzale','piazzetta',
                'ripa','strada','via','viale','vicolo']
post_code = re.compile(r'^2\d{4}')




def fix_street(street, street_types = street_types):	

	""" This funcion is used to fix street names.

		Argument:
			street (string): variable representing an address (street only)
			street_types (optional(list)): list of acceptable street types. Defaults to street_types

		Returns:
			string: formatted address if successful. Same addreess otherwise.
	"""

	if street:
		street_type = first_word.search(street).group(1)
		if street_type.lower() in street_types:
			return titlecase(street)
		else:
			return street



def is_postcode(postcode):

	"""
		This function is used to check if a postcode value is valid.

		Argument:
			postcode (string): variable representing a postcode.

		Returns:
			bool: True if valid postcode. False otherwise.
	"""
	return post_code.search(postcode)




	


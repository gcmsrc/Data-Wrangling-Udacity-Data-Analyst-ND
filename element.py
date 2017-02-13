# -*- coding: utf-8 -*-

"""
	This file contains the function used to format each element of the .osm file
	according to a standard schema. An example is reported below.

	Sample schema

	{
		"fixme": ["Is this really a tourism attraction? A better tag should be found."],
		"name": "The Hub",
		"created": {"changeset": "12881709",
        	    	"user": "AnyFile",
            		"version": "3",
            		"uid": "113669",
            		"timestamp": "2012-08-27T16:40:40Z"},
		"pos": [45.4822582, 9.1802182],
		"amenity": {"type": "general_attraction"},
		"address": {"city": "Milano",
        		    "street": "via Paolo Sarpi",
            		"housenumber": "8",
            		"postcode": "20154"},
		"type": "node",
		"id": "613579685"
	}


	Module-level variables are:

		CREATED (list): all attributes to be stored into the created dictionary.
		FIXME (list): all attributes to be stored into the fixme list.
		addr: regex compile expression to checks if a tag is an address field with colon, 
			  e.g. 'addr:street'.

	Moduels imported:
		amenity

"""

import amenity
import fix
import re

CREATED = ["version", "changeset", "timestamp", "user", "uid"]
FIXME = ['FIXME','fixme','fixme:2']
addr = re.compile(r'^(addr):([a-z]+|_+)')


''' ******** ATTRIBUTES ******** 
___________________________________________________________________________________________________
'''

def create_attr(attrib_dict,created_dict,pos):

	"""
		This function adds attribute values to the attrib_dict

		Argument:
			attrib_dict (dict): calculated in element_attrib function
			created_dict (dict): calculated in element_attrib function
			pos (list): calculated in element_attrib function

		Returns:
			attrib_dict (dict): updated attrib_dict
	"""

	if created_dict != {}:
		attrib_dict['created'] = created_dict

	if pos != ['lat','lon']:
		attrib_dict['pos'] = pos

	return attrib_dict

def element_attrib(element):

	"""
		This function is used to return the dictionary of an
		element attribute values.

		Argument:
			element (n/a): xml element

		Returns:
			attrib_dict (dict): dictionary of created values
	"""

	attrib_dict = {}
	created_dict = {}
	pos = ['lat','lon']

	for attrib in element.attrib:

		if attrib in CREATED:
			created_dict[attrib] = element.attrib[attrib]
		elif attrib == pos[0]:
			pos[0] = float(element.attrib[attrib])
		elif attrib == pos[1]:
			pos[1] =  float(element.attrib[attrib])
		else:
			attrib_dict[attrib] = element.attrib[attrib]

	return create_attr(attrib_dict,created_dict,pos)



''' ******** TAGS ******** 
___________________________________________________________________________________________________
'''


def element_addr(k,v):

	"""
		This function is used to return a list of an address key-value pair.

		Argument:
			element (n/a): xml element (tag)

		Returns:
			addr_list (dict): list of key-value for an address tag.
	"""

	address_item = addr.search(k).group(2)
	"""extracts word after colon"""
	
	addr_list = []

	if address_item == 'street':
		addr_list.append(address_item)
		addr_list.append(fix.fix_street(v))

	elif address_item == 'postcode':
		if fix.is_postcode(v):
			addr_list.append(address_item)
			addr_list.append(v)

	else:
		addr_list.append(address_item)
		addr_list.append(v)

	 
	if len(addr_list) == 2:
		return addr_list
	else:
		return None


def create_tag(tag_dict, addr_dict, fixme, amenity_dict):
	"""
		This function adds attribute values to the tag_dict

		Argument:
			tag_dict (dict): calculated in element_tag function
			addr_dict (dict): calculated in element_ta fungction
			fixme (list): calculated in element_tag function
			amenity_dict (dict): calculated in element_ta fungction

		Returns:
			tag_dict (dict): updated tag_dict
	"""
	if addr_dict != {}:
		tag_dict['address'] = addr_dict

	if fixme != []:
		tag_dict['fixme'] = fixme

	if amenity_dict != {'amenity':None, 'tourism':None,'shop':None}:
		tag_dict['amenity'] =  amenity_dict

	return tag_dict




def element_tag(element):

	"""
		This function is used to return the dictionary of all the tag values.

		Argument:
			element (n/a): xml element

		Returns:
			tag_dict (dict): dictionary of all the tag values
	"""

	tag_dict = {}
	addr_dict = {}
	fixme = []
	amenity_dict = {'amenity':None, 
					'tourism':None,
					'shop':None}

	for tag in element.iter('tag'):
		k = tag.attrib['k']
		v = tag.attrib['v']

		if addr.search(k):
			addr_list = element_addr(k,v)
			if addr_list:
				addr_dict[addr_list[0]] = addr_list[1]

		elif k in FIXME:
			fixme.append(v)

		elif k in amenity_dict.keys():
			amenity_dict[k] = v

		elif k == 'name':
			tag_dict['name'] = v


	return create_tag(tag_dict, addr_dict, fixme, amenity_dict)

''' ******** ND_REFS ******** 
___________________________________________________________________________________________________
'''

def element_nd(element):

	"""
		This function is used to return the list of nd tags.

		Argument:
			element (n/a): xml element

		Returns:
			node_refs (list): list of node references
	"""

	node_refs = []

	for node in element.iter('nd'):
		node_refs.append(node.attrib['ref'])

	return node_refs

''' ******** MEMBER_REFS ******** 
___________________________________________________________________________________________________
'''

def element_member(element):

	"""
		This function is used to return the list of member tags.

		Argument:
			element (n/a): xml element

		Returns:
			member_refs (list): list of member references
	"""

	member_refs = []

	for member in element.iter('member'):
		member_refs.append(member.attrib['ref'])

	return member_refs


''' ******** ELEMENT ******** 
___________________________________________________________________________________________________
'''

def add_attr(element, element_dict):
	"""
		This function formats the element_dict by adding the attributes as per
		the correct schena.

		Argument:
			
			element_dict (dict): element_dict from add_all function
			element (n/a): xml element

		Returns:
			element_dict (dict): formatted element dictionary
	"""

	attrib_dict = element_attrib(element)

	for attrib in attrib_dict.keys():
		if attrib == 'created':
			element_dict['created'] = attrib_dict['created']
		elif attrib == 'pos':
			element_dict['pos'] = attrib_dict['pos']
		else:
			element_dict[attrib] = attrib_dict[attrib]

	return element_dict


def add_tag(element, element_dict):
	"""
		This function formats the element_dict by adding the tags as per
		the correct schena.

		Argument:
			
			element_dict (dict): element_dict from add_all function
			element (n/a): xml element

		Returns:
			element_dict (dict): formatted element dictionary
	"""
	tag_dict = element_tag(element)

	for tag in tag_dict.keys():
		if tag == 'amenity':
			element_dict[tag] = amenity.amenity_return(tag_dict[tag])
		else:
			element_dict[tag] = tag_dict[tag]

	return element_dict


def add_type(element, element_dict):

	"""
		This function formats the element_dict by adding the type value.

		Argument:
			
			element_dict (dict): element_dict from add_all function
			element (n/a): xml element

		Returns:
			element_dict (dict): formatted element dictionary
	"""
	element_dict['type'] = element.tag

	return element_dict


def add_nd_member(element, element_dict):
	"""
		This function adds final values to the element_dict

		Argument:
			element_dict (dict): calculated in add_all function
			node_refs (list): calculated in add_all function
			member_refs (list): calculated in add_all function

		Returns:
			element_dict (dict): updated element_dict
	"""

	node_refs = element_nd(element)

	if node_refs != []:
		element_dict['node_refs'] = node_refs

	member_refs = element_member(element)
	if member_refs != []:
		element_dict['member_refs'] = member_refs

	return element_dict

def add_all(element):
	"""
		This function adds all values

		Argument:
			element_dict (dict): calculated in shape_element function
			node_refs (list): calculated in shape_element function
			member_refs (list): calculated in shape_element function

		Returns:
			element_dict (dict): updated element_dict
	"""

	element_dict = {}

	element_dict = add_attr(element, element_dict)
	element_dict = add_tag(element, element_dict)
	element_dict = add_type(element, element_dict)
	element_dict = add_nd_member(element, element_dict)

	return element_dict	


def shape_element(element):

	"""
		This function returns a formatted element as per schema above

		Argument:
			element (n/a): xml element

		Returns:
			element_dict (dict): formatted element dictionary
	"""
	

	element_dict = add_all(element)

	return element_dict


	





#!/usr/bin/env python3
import requests

def test_route_a_list_post():
	headers = {
		"key": "a4149e95dbf049b6927945e819ae0ac9"
	}
	params = ()
	data = {
		"uuids": [
			"test" ,
			"eb7ebc60-3c3e-455f-9a9d-d3daa3d836ba" ,
			"what about here ?" ,
			"what about here there" ,
			"asdf123"
		]
	}
	url = 'http://localhost:9337/a-list'
	response = requests.post( url , headers=headers , params=params , data=data )
	response.raise_for_status()
	try:
		print( response.json() )
	except Exception as e:
		print( response.text )

def test_route_a_list_get():
	headers = {
		"key": "a4149e95dbf049b6927945e819ae0ac9"
	}
	params = ()
	data = {
		"uuids": [
			"test" ,
			"eb7ebc60-3c3e-455f-9a9d-d3daa3d836ba" ,
			"what about here ?" ,
			"what about here there" ,
			"asdf123"
		]
	}
	url = 'http://localhost:9337/a-list'
	response = requests.get( url , headers=headers , params=params , data=data )
	response.raise_for_status()
	try:
		print( response.json() )
	except Exception as e:
		print( response.text )

if __name__ == "__main__":
	# test_route_a_list_post()
	test_route_a_list_get()

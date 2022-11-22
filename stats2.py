#!/usr/bin/env python3
import sys
import yaml
import redis
import requests
import time
from pprint import pprint
import traceback

def write_yaml( file_path , python_object ):
	with open( file_path , 'w' , encoding='utf-8' ) as f:
		yaml.dump( python_object , f )

def read_yaml( file_path ):
	with open( file_path ) as f:
		return yaml.safe_load( f )

if __name__ == "__main__":
	config = read_yaml( sys.argv[ 1 ] )
	redis_connection = redis.StrictRedis(
		host=config[ "redis" ][ "host" ] ,
		port=config[ "redis" ][ "port" ] ,
		db=config[ "redis" ][ "db" ] ,
		password=config[ "redis" ][ "password" ] ,
		decode_responses=True
	)
	print( redis_connection )
	global_total_key = f"ANALYTICS.acd21e9a-f430-4283-a1c4-a5446e95c288.TOTAL"
	result = redis_connection.get( global_total_key )
	print( result )

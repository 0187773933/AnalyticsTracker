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

def get_total_views( redis_connection , uuid ):
	try:
		global_total_key = f"ANALYTICS.{uuid}.TOTAL"
		result = redis_connection.get( global_total_key )
		if result == None:
			result = 0
		result = int( result )
		return result
	except Exception as e:
		print( e )
		return 0

def get_unique_views( redis_connection , uuid ):
	try:
		global_ips_key = f"ANALYTICS.{uuid}.IPS"
		result = redis_connection.scard( global_ips_key )
		if result == None:
			result = 0
		result = int( result )
		return result
	except Exception as e:
		print( e )
		return 0

def sort_by_unique_views( snapshots ):
	try:
		return sorted( snapshots , key=lambda x: x[ "unique_views" ] , reverse=False )
	except Exception as e:
		print( traceback.format_exc() )

if __name__ == "__main__":
	config = read_yaml( sys.argv[ 1 ] )
	redis_connection = redis.StrictRedis(
		host=config[ "redis" ][ "host" ] ,
		port=config[ "redis" ][ "port" ] ,
		db=config[ "redis" ][ "db" ] ,
		password=config[ "redis" ][ "password" ] ,
		decode_responses=True
	)
	snapshots = []
	for index , name in enumerate( config[ "items" ] ):
		total_views = get_total_views( redis_connection , config[ "items" ][ name ][ "uuid" ] )
		unique_views = get_unique_views( redis_connection , config[ "items" ][ name ][ "uuid" ] )
		if "total_views" in config[ "items" ][ name ]:
			total_views_delta = ( total_views -  config[ "items" ][ name ][ "total_views" ] )
		else:
			total_views_delta = 0
		if "unique_views" in config[ "items" ][ name ]:
			unique_views_delta = ( unique_views -  config[ "items" ][ name ][ "unique_views" ] )
		else:
			unique_views_delta = 0
		config[ "items" ][ name ][ "total_views" ] = total_views
		config[ "items" ][ name ][ "unique_views" ] = unique_views
		snapshots.append({
			"total_views": total_views ,
			"unique_views": unique_views ,
			"total_views_delta": total_views_delta ,
			"unique_views_delta": unique_views_delta ,
			"uuid": config[ "items" ][ name ][ "uuid" ] ,
			"name": name ,
		})
	write_yaml( sys.argv[ 1 ] , config )
	snapshots = sort_by_unique_views( snapshots )
	for index , result in enumerate( snapshots ):
		print( f'{result["name"]} === {result["uuid"]} === ' , end="" )
		if result[ "total_views_delta" ] > 0:
			print( f'Total Views [ +{result["total_views_delta"]} ] : {result["total_views"]} === ' , end="" )
		else:
			print( f'Total Views : {result["total_views"]} === ' , end="" )
		if result[ "unique_views_delta" ] > 0:
			print( f'Unique Views [ +{result["unique_views_delta"]} ] : {result["unique_views"]}' )
		else:
			print( f'Unique Views : {result["unique_views"]}')

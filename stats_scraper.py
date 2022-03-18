#!/usr/bin/env python3
import sys
import re
import time
import yaml # pip install pyyaml
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import traceback

def read_yaml( file_path ):
	with open( file_path ) as f:
		return yaml.safe_load( f )

def convert_entry_to_dictionary( entry_items ):
	keys = [ "date" , "time" , "ip" , "country" , "lat_long" ]
	result = {}
	for index , item in enumerate( entry_items ):
		result[ keys[ index ] ] = item
	return result

def scrape_analytics_page( host , uuid , name ):
	try:
		url = f"{ host }/a/{ uuid }"
		response = requests.get( url )
		response.raise_for_status()
		html = response.text
		soup = BeautifulSoup( html , "html.parser" )

		try:
			total_views = int( soup.find_all( "h1" , string=re.compile( "^Total Views" ) )[ 0 ].text.split( " = " )[ 1 ] )
		except Exception as e:
			total_views = 0
		try:
			unique_views = int( soup.find_all( "h1" , string=re.compile( "^Unique Views" ) )[ 0 ].text.split( " = " )[ 1 ] )
		except Exception as e:
			unique_views = 0


		entries = soup.find_all( "li" )
		parsed_entries = []
		for index , entry in enumerate( entries ):
			items = entry.text.split( " === " )
			if items[ -1 ] == "Map":
				items.pop()
			entry_dictionary = convert_entry_to_dictionary( items )
			parsed_entries.append( entry_dictionary )
		return {
			"total_views":  total_views ,
			"unique_views": unique_views ,
			"entries": parsed_entries ,
			"uuid": uuid ,
			"name": name
		}
	except Exception as e:
		print( e )
		print( traceback.format_exc() )
		return False

def filter_blacklisted_lat_longs( parsed_analytics ):
	for parsed_analytic_index , parsed_analytic in enumerate( parsed_analytics ):
		filtered = []
		for index , entry in enumerate( parsed_analytic[ "entries" ] ):
			if "lat_long" in entry:
				# filter amazon ec2 webserver hits
				if entry[ "lat_long" ] == "39.0437,-77.4875":
					continue
				else:
					filtered.append( entry )
			else:
				filtered.append( entry )
		parsed_analytic[ "entries" ] = filtered
	return parsed_analytics

def recalculate_total_and_unique_views( parsed_analytics ):
	for parsed_analytic_index , parsed_analytic in enumerate( parsed_analytics ):
		unique = set()
		parsed_analytic[ "total_views" ] = len( parsed_analytic[ "entries" ] )
		for index , entry in enumerate( parsed_analytic[ "entries" ] ):
			unique.add( entry[ "ip" ] )
		parsed_analytic[ "unique_views" ] = len( unique )
	return parsed_analytics

def sort_by_unique_views( parsed_analytics ):
	try:
		return sorted( parsed_analytics , key=lambda x: x[ "unique_views" ] , reverse=False )
	except Exception as e:
		print( traceback.format_exc() )

if __name__ == "__main__":
	tracking = read_yaml( sys.argv[ 1 ] )
	parsed_analytics = []
	for index , name in enumerate( tracking[ "uuids" ] ):
		analytics = scrape_analytics_page( tracking[ "host" ] , tracking[ "uuids" ][ name ] , name )
		parsed_analytics.append( analytics )
		time.sleep( 1 )
	# pprint( parsed_analytics )

	parsed_analytics = filter_blacklisted_lat_longs( parsed_analytics )
	parsed_analytics = recalculate_total_and_unique_views( parsed_analytics )

	parsed_analytics = sort_by_unique_views( parsed_analytics )
	for index , result in enumerate( parsed_analytics ):
		print( f'{result["name"]} === {result["uuid"]} === {result[ "total_views" ]} === {result[ "unique_views" ]}' )
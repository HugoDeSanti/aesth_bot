import requests
import json
import mysql.connector
from mysql.connector import errorcode

def getCredentials() :
	# """ Gets credentials for use in all GET and POST requests
	
	# Returns:
	# 	dictonary: credentials needed globally
	# """

	creds = dict() # dictionary to hold everything
	creds['access_token'] = '' # access token for use with all api calls
	creds['graph_domain'] = 'https://graph.facebook.com/' # base domain for api calls
	creds['graph_version'] = 'v13.0' # version of the api we are hitting
	creds['endpoint_base'] = creds['graph_domain'] + creds['graph_version'] + '/' # base endpoint with domain and version
	creds['instagram_account_id'] = '17841445276335289' # users instagram account id

	return creds

def makeApiCall( url, endpointParams, type ) :
	# """ Request data from endpoint with params
	
	# Args:
	# 	url: string of the url endpoint to make request from
	# 	endpointParams: dictionary keyed by the names of the url parameters
	# Returns:
	# 	object: data from the endpoint
	# """

	if type == 'POST' : # POST request
		data = requests.post( url, endpointParams )
	else : # GET request
		data = requests.get( url, endpointParams )

	response = dict() # hold response info
	response['url'] = url # url we are hitting
	response['endpoint_params'] = endpointParams #parameters for the endpoint
	response['endpoint_params_pretty'] = json.dumps( endpointParams, indent = 4 ) # pretty print for cli
	response['json_data'] = json.loads( data.content ) # response data from the api
	response['json_data_pretty'] = json.dumps( response['json_data'], indent = 4 ) # pretty print for cli

	return response # get and return content

	
def connectMySQL():
	try:
		cnx = mysql.connector.connect(user='root', password='bR3SK9eQ76VDWDn', database='aesth_bot_schema', host='localhost', autocommit=True)
		cursor = cnx.cursor()	
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	return (cnx, cursor)

def updateSQLdb(reddit_img_id):
	cnx, cursor = connectMySQL()
	update_stmt = "UPDATE pics SET posted = 1 WHERE reddit_id = %(reddit_img_id)s"
	cursor.execute(update_stmt, {"reddit_img_id": reddit_img_id})
	return
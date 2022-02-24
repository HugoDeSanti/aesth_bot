import requests
import json

def getCredentials() :
	# """ Gets credentials for use in all GET and POST requests
	
	# Returns:
	# 	dictonary: credentials needed globally
	# """

	creds = dict() # dictionary to hold everything
	creds['access_token'] = 'EAAGHAQnIZCQIBAAbqtC6tFlRUSsF1ldS2HKUJx7voAckVitPxlc1spKyIMYTwZBnwjRZA2PVyuPM42Es2wCkZChCXqMGLL0XClZCZBgnBZBj68EvlSaZBA0P8nvc97dQ99E0f2AAt7k9miOZBhMr6lX8AtyTEBRt9aymQzI9o29MQigZDZD' # access token for use with all api calls
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
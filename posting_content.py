from defines import getCredentials, makeApiCall

def createMediaObject( params ) :
	# Create media object
	# Args:
	# 	params: dictionary of params
	
	# API Endpoint:
	# 	https://graph.facebook.com/v5.0/{ig-user-id}/media?image_url={image-url}&caption={caption}&access_token={access-token}
	# Returns:
	# 	object: data from the endpoint

	url = params['endpoint_base'] + params['instagram_account_id'] + '/media' # endpoint url
	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['caption'] = params['caption']  # caption for the post
	endpointParams['access_token'] = params['access_token'] # access token
	endpointParams['image_url'] = params['media_url']  # url to the asset
	
	return makeApiCall( url, endpointParams, 'POST' ) # make the api call

def publishMedia( mediaObjectId, params ) :
	# Publish content
	# Args:
	# 	mediaObjectId: id of the media object
	# 	params: dictionary of params
	
	# API Endpoint:
	# 	https://graph.facebook.com/v5.0/{ig-user-id}/media_publish?creation_id={creation-id}&access_token={access-token}
	# Returns:
	# 	object: data from the endpoint


	url = params['endpoint_base'] + params['instagram_account_id'] + '/media_publish' # endpoint url

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['creation_id'] = mediaObjectId # fields to get back
	endpointParams['access_token'] = params['access_token'] # access token

	return makeApiCall( url, endpointParams, 'POST' ) # make the api call

def getMediaObjectStatus( mediaObjectId, params ) :
	# Check the status of a media object
	# Args:
	# 	mediaObjectId: id of the media object
	# 	params: dictionary of params
	
	# API Endpoint:
	# 	https://graph.facebook.com/v5.0/{ig-container-id}?fields=status_code
	# Returns:
	# 	object: data from the endpoint

	url = params['endpoint_base'] + '/' + mediaObjectId # endpoint url

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['fields'] = 'status_code' # fields to get back
	endpointParams['access_token'] = params['access_token'] # access token

	return makeApiCall( url, endpointParams, 'GET' ) # make the api call
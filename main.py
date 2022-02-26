import time
import mysql.connector
from mysql.connector import errorcode
import defines
import posting_content
import reddit_scraper

def go_post():
  # Connect to SQL server to download image info like user and caption
  cnx, cursor = defines.connectMySQL()

  cursor.execute("SELECT * FROM pics WHERE posted = 0 ORDER BY id ASC")
  img_post = cursor.fetchone() #img_post is a tuple of a sql row now
  img_id = img_post[0]
  reddit_img_id = img_post[1]
  url = img_post[8]
  uploader = img_post[4]
  caption = img_post[3]
  submission_title = img_post[3]
  hashtags = [x for x in submission_title.split() if len(x) > 3]

  #Now get parameteres for img
  params = defines.getCredentials() # get creds from defines
  params['media_type'] = 'IMAGE' # type of asset
  params['media_url'] = url # url on public server for the post
  params['caption'] = '"' + caption + '"'
  params['caption'] += "\n"
  params['caption'] += "[" + str(img_id) + "]"
  params['caption'] += "\n"
  params['caption'] += ("\nvia u/" + uploader)
  params['caption'] += "\n"
  for word in hashtags:
    params['caption'] += ("#" + word + " ")

  imageMediaObjectResponse = posting_content.createMediaObject( params ) # create a media object through the api
  print(imageMediaObjectResponse)
  imageMediaObjectId = imageMediaObjectResponse['json_data']['id'] # id of the media object that was created

  imageMediaStatusCode = 'IN_PROGRESS';
  while imageMediaStatusCode != 'FINISHED' : # keep checking until the object status is finished
    imageMediaObjectStatusResponse = posting_content.getMediaObjectStatus( imageMediaObjectId, params ) # check the status on the object
    imageMediaStatusCode = imageMediaObjectStatusResponse['json_data']['status_code'] # update status code
    print( "\n---- IMAGE MEDIA OBJECT STATUS -----\n" ) # display status response
    print( "\t" + imageMediaStatusCode ) # status code of the object
    time.sleep( 5 ) # wait 5 seconds if the media object is still being processed

  publishImageResponse = posting_content.publishMedia( imageMediaObjectId, params ) # publish the post to instagram

  print( "\n---- PUBLISHED IMAGE RESPONSE -----\n" ) # title
  print( publishImageResponse['json_data_pretty'] ) # json response from ig api

  #Now tell SQL database that post is posted
  cursor.execute("UPDATE pics SET `posted` = '1' WHERE (`id` = '" + str(img_id) + "');")
  cnx.commit()
  cursor.close()
  cnx.close()

if __name__ == "__main__":
  #Every 7 days run scraper
  #Every 6h post pic
  while True:
    print("Scraping")
    reddit_scraper.scrape("analog")
    reddit_scraper.scrape("vaporwaveaesthetics")
    reddit_scraper.scrape("itookapicture")
    post_counter = 0
    while True:
      go_post()
      print("Just posted, now waiting 4 hours")
      post_counter += 1
      time.sleep(14400) #Wait 4 hours
      if post_counter >= 28: #28 posts a week
        break
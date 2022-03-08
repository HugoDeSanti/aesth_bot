import time
import mysql.connector
from mysql.connector import errorcode
import defines
import posting_content
import reddit_scraper

def go_post():
  # Connect to SQL server to download image info like user and caption
  cnx, cursor = defines.connectMySQL()
  cursor.execute("SELECT * FROM pics WHERE posted = 0 ORDER BY RAND()")
  img_post = cursor.fetchone() #img_post is a tuple of a sql row now

  reddit_img_id = str(img_post[1])
  reddit_title = img_post[3]
  reddit_uploader = img_post[4]
  reddit_url = img_post[8]
  ig_hashtags = [x for x in reddit_title.split() if len(x) > 3]
  ig_hashtags.append("aesthetic")

  #Now get parameteres for img
  params = defines.getCredentials() # get creds from defines
  params['media_type'] = 'IMAGE' # type of asset
  params['media_url'] = reddit_url # url on public server for the post
  params['caption'] = '"' + reddit_title + '"'
  params['caption'] += "\n"
  params['caption'] += "[" + reddit_img_id + "]"
  params['caption'] += "\n"
  params['caption'] += ("\nvia u/" + reddit_uploader)
  params['caption'] += "\n"
  for word in ig_hashtags:
    params['caption'] += ("#" + word + " ")

  imageMediaObjectResponse = posting_content.createMediaObject( params ) # create a media object through the api
  print(imageMediaObjectResponse)
  try:
    imageMediaObjectId = imageMediaObjectResponse['json_data']['id'] # id of the media object that was created
  except:
    print('Could not create image media object')
    defines.updateSQLdb(reddit_img_id)
    return #FIX THIS BECAUSE LINE 45 DOESNT GET READ IF THIS CODE GOES INTO THE EXCEPT STATEMENT

  imageMediaStatusCode = 'IN_PROGRESS';
  while imageMediaStatusCode != 'FINISHED' : # keep checking until the object status is finished
    imageMediaObjectStatusResponse = posting_content.getMediaObjectStatus( imageMediaObjectId, params ) # check the status on the object
    imageMediaStatusCode = imageMediaObjectStatusResponse['json_data']['status_code'] # update status code
    print( "\n---- IMAGE MEDIA OBJECT STATUS -----\n" ) # display status response
    print( "\t" + imageMediaStatusCode ) # status code of the object
    time.sleep( 5 ) # wait 5 seconds if the media object is still being processed

  try:
    publishImageResponse = posting_content.publishMedia( imageMediaObjectId, params ) # publish the post to instagram
  except:
    defines.updateSQLdb(reddit_img_id)
  #If bot was not able to post picture, it will still check it as posted in the database. Maybe change this later.


  print( "\n---- PUBLISHED IMAGE RESPONSE -----\n" ) # title
  print( publishImageResponse['json_data_pretty'] ) # json response from ig api

  #Now tell SQL database that post is posted
  print("IMG ID: " + reddit_img_id)

  #Tell database that img has been posted
  defines.updateSQLdb(reddit_img_id)


if __name__ == "__main__":
  #Every 7 days run scraper
  #Every 6h post pic
  while True:
    print("Scraping")
    #reddit_scraper.scrape("vaporwaveaesthetics", 8)
    #reddit_scraper.scrape("analog", 8)
    #reddit_scraper.scrape("architectureporn", 7)
    #reddit_scraper.scrape("artporn", 6)
    #reddit_scraper.scrape("nocontextpics", 5)
    #reddit_scraper.scrape("imaginarylandscapes", 4)
    #reddit_scraper.scrape("itookapicture", 4)
    post_counter = 0
    while True:
      go_post()
      print("Just posted, now waiting 4 hours")
      post_counter += 1
      time.sleep(14400) #Wait 4 hours
      if post_counter >= 28: #28 posts a week
        break
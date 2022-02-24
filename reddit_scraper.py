import praw
import urllib.request
from PIL import Image
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime, timezone
import os

def scrape():
  # Connect to SQL server to upload image info to database later
  try:
    cnx = mysql.connector.connect(user='root', password='bR3SK9eQ76VDWDn', database='aesth_bot_schema', host='localhost')
    cursor = cnx.cursor()
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
  #else:
    #cnx.close()

  #Prepare to upload data into sql database later
  add_img = ("INSERT INTO pics "
            "(reddit_id, location, caption, poster, subreddit, date_stored, url) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)")

  # Create a reddit instance, user credentials are in a .ini file
  reddit = praw.Reddit("bot1", user_agent="bot1 user agent")


  curr_subreddit = "itookapicture"
  # FOR /r/ITAP
  counter = 0 #Use the counter to get another img if one of them isnt jpg or png
  for submission in reddit.subreddit(curr_subreddit).top("week", limit=19):
    if counter >= 15:
      break

    file_title = curr_subreddit + "-" + submission.id + ".jpg"

    if submission.stickied: #Skip stickied submissions
      continue
    url = str(submission.url)
    if (url[-3:] == "jpg") or (url[-4:] == "jpeg"): #Check if the link is an image
      urllib.request.urlretrieve(url, file_title)
    elif (url[-3:] == "png"): #IG API only takes JPEG so convert PNG to JPEG
      urllib.request.urlretrieve(url, file_title[-4] + ".png")
      img_png = Image.open("D:\\aesth_bot\\" + file_title[:-4] + ".png")
      img_png.save("D:\\aesth_bot\\" + file_title)
    else:
      continue

    #By this point, if IMG is valid it has been saved so:
    counter += 1
    img_location = "D:\\aesth_bot\\" + file_title
    caption = submission.title[8:] # Removes "ITAP of" from caption
    poster = submission.author.name


    data_img = (submission.id, img_location, caption, poster, curr_subreddit, datetime.now(timezone.utc), submission.url)
    cursor.execute(add_img, data_img)
    cnx.commit()

  curr_subreddit = "analog"
  counter = 0
  #FOR /r/analog
  for submission in reddit.subreddit(curr_subreddit).top("week", limit=19):
    if counter >= 15:
      break
    file_title = curr_subreddit + "-" + submission.id + ".jpg"
    if submission.stickied: #Skip stickied submissions
      continue
    url = str(submission.url)
    if (url[-3:] == "jpg") or (url[-4:] == "jpeg"): #Check if the link is an image
      urllib.request.urlretrieve(url, file_title)
    elif (url[-3:] == "png"): #IG API only takes JPEG so convert PNG to JPEG
      urllib.request.urlretrieve(url, file_title[:-4] + ".png")
      img_png = Image.open("D:\\aesth_bot\\" + file_title[:-4] + ".png")
      img_png.save("D:\\aesth_bot\\" + file_title)
      os.remove("D:\\aesth_bot\\" + file_title[:-4] + ".png")
    else:
      continue

    counter += 1

    img_location = "D:\\aesth_bot\\" + file_title
    caption = submission.title
    poster = submission.author.name

    data_img = (submission.id, img_location, caption, poster, curr_subreddit, datetime.now(timezone.utc), submission.url)
    cursor.execute(add_img, data_img)
    cnx.commit()

  cursor.close()
  cnx.close()
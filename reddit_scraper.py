import praw
import urllib.request
from PIL import Image
from datetime import date, datetime, timezone
import os
import defines

def scrape(subreddit):
  #Scrapes top 15 weekly posts


  # Connect to SQL server to upload image info to database later
  cnx, cursor = defines.connectMySQL()

  # Create a reddit instance, user credentials are in a .ini file
  reddit = praw.Reddit("bot1", user_agent="bot1 user agent")

  saved_imgs = 0
  
  submissions = reddit.subreddit(subreddit).top("week", limit=40)
  for submission in submissions:
    if (saved_imgs > 15):
      break
    if submission.stickied:
      continue
    img_filename = subreddit + "-" + submission.id + ".jpg"
    post_url = str(submission.url)
    if (post_url[-3:] == "jpg") or (post_url[-4:] == "jpeg"): #Check if the link is an image
      urllib.request.urlretrieve(post_url, img_filename)
    # elif (post_url[-3:] == "png"): #IG API only takes JPEG so convert PNG to JPEG
    #   urllib.request.urlretrieve(post_url, img_filename[-4] + ".png")
    #   print(post_url, img_filename)
    #   img_png = Image.open("D:\\aesth_bot\\" + img_filename[:-4] + ".png")
    #   img_png.save("D:\\aesth_bot\\" + img_filename)
    #   os.remove("D:\\aesth_bot\\" + img_filename[:-4] + ".png")
    else:
      continue

    #IG only takes IMGs with Aspect Ratios of 1.91/1 or 4/5 width to height
    img_path = "D:\\aesth_bot\\" + img_filename
    if aspect_ratio_check(img_path) == False:
      os.remove(img_path)
      continue

    # Some cleaning of titles; Removes "ITAP of" from posts
    if (subreddit == "itookapicture"):
      caption = submission.title[8:]
    else:
      caption = submission.title

    poster = submission.author.name

    #Upload image info to SQL database
    add_img = ("INSERT INTO pics "
            "(reddit_id, location, caption, poster, subreddit, date_stored, url) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    data_img = (submission.id, img_path, caption, poster, subreddit, datetime.now(timezone.utc), submission.url)
    try: #Try adding img to database, if img is already in database then do not add
      cursor.execute(add_img, data_img)
      saved_imgs += 1
    except:
      print(img_filename +  " already in database")
    cnx.commit()
  

  cursor.close()
  cnx.close()

def aspect_ratio_check(path):
  img = Image.open(path)
  w = img.width
  h = img.height
  if (w/h > 1.9) or (w/h < 0.8):
    return False
  return True






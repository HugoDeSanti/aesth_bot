import praw
import urllib.request
from PIL import Image
from datetime import date, datetime, timezone
import os
import defines

def scrape(subreddit):
  # Connect to SQL server to upload image info to database later
  cnx, cursor = defines.connectMySQL()

  # Create a reddit instance, user credentials are in a .ini file
  reddit = praw.Reddit("bot1", user_agent="bot1 user agent")

  saved_imgs = 0
  while (saved_imgs < 15):
    submissions = reddit.subreddit(subreddit).top("week", limit=60)
    for submission in submissions:
      if submission.stickied:
        continue
      post_title = subreddit + "-" + submission.id + ".jpg"
      post_url = str(submission.url)
      if (post_url[-3:] == "jpg") or (post_url[-4:] == "jpeg"): #Check if the link is an image
        urllib.request.urlretrieve(post_url, post_title)
      elif (post_url[-3:] == "png"): #IG API only takes JPEG so convert PNG to JPEG
        urllib.request.urlretrieve(post_url, post_title[-4] + ".png")
        img_png = Image.open("D:\\aesth_bot\\" + post_title[:-4] + ".png")
        img_png.save("D:\\aesth_bot\\" + post_title)
      else:
        continue

    #IG only takes IMGs with Aspect Ratios of 1.91/1 or 4/5 width to height
    img_path = "D:\\aesth_bot\\" + post_title
    if aspect_ratio_check(img_path) == False:
      os.remove(img_path)
      continue
    else:
      saved_imgs += 1

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
    cursor.execute(add_img, data_img)
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






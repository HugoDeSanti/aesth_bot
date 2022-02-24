import mysql.connector
from mysql.connector import errorcode

# Connect to SQL server to download image info
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

cursor.execute("SELECT * FROM pics WHERE posted = 0")
myresult = cursor.fetchone()
img_location = myresult[2]
caption = myresult[3]
poster = myresult[4]
hashtags = [x for x in caption.split() if len(x) > 3]

cursor.close()
cnx.close()
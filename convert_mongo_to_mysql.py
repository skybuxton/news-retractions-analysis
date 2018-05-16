import os
import tqdm
import pymongo

# mysql> SET @@global.sql_mode= 'NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';

pyconn = pymongo.MongoClient()
import json
import MySQLdb as my
db = my.connect(host="127.0.0.1",
user="root",
passwd="",
db="retractions"
)
 
sql_cursor = db.cursor()

sql = "insert into retractions(body, title, url, event_id, month, year, correction_type, correction_check, correction_info) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

mongo_cursor = pyconn.db.articles.find({})

with tqdm.tqdm(total=mongo_cursor.count()) as pbar:
	for item in mongo_cursor:
		x = (db.escape_string(item.get('body', '')), db.escape_string(item.get('title', '')), item.get('url'), item.get('event_id'), item.get('month'), item.get('year'), item.get('correction_type'), item.get('correction_check'), json.dumps(item.get('correction_info')))
		# print(sql)
		# print(x)
		sql_cursor.execute(sql, x)
		db.commit()
		pbar.update(1)

import pymongo

conn = pymongo.MongoClient()

def import_event(obj):
	global conn
	event_id = obj["event_id"]
	if not event_id:
		print("event_id required")
		return
	conn.db.articles.ensure_index("event_id", unique=True)
	conn.db.articles.ensure_index("month")
	conn.db.articles.ensure_index("year")
	conn.db.articles.ensure_index("url")
	existing_obj = conn.db.articles.find_one({"event_id": event_id})
	if existing_obj:
		print("Already imported %s" % event_id)
	else:
		conn.db.articles.insert_one(obj)
		print("imported %s" % event_id)

def update_event(_id, updates):
	conn.db.articles.update_one({"_id": _id}, {"$set": updates})

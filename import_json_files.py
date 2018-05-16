import pymongo
import glob
import json

from . import db

csvs = glob.glob("*.csv")
dirs = map(lambda x: x.replace('.csv', ''), csvs)
dirs.remove("links")

for month_year in dirs:
	month = month_year.split("_")[0]
	year = month_year.split("_")[1]
	print("Importing %s" % month_year)
	jsons = glob.glob("%s/*.json" % month_year)
	for jf in jsons:
		event_id = jf.split("/")[1].split('.')[0]
		print("Importing %s %s" % (month, event_id))
		obj = json.loads(open(jf).read())
		obj["month"] = month
		obj["year"] = year
		obj["event_id"] = event_id
		# print("%s" % obj)
		# print(month)
		# print(year)
		db.import_event(obj)

		

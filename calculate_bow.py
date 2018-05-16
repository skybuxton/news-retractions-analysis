import os
import pymongo
from sklearn.feature_extraction.text import CountVectorizer
import pickle
from nltk.corpus import stopwords

conn = pymongo.MongoClient()

stops_list = stopwords.words("english")

cursor = conn.db.articles.find({"correction_type": 1})
bodys = []
for doc in cursor:
	body = doc['body']
	body = body.lower()
	body = body.replace("\"", " ")
	body = body.replace("'", " ")
	words = body.split()
	parsed_body = " ".join(words)
	bodys.append(parsed_body)

TOKENS_ALPHANUMERIC = '[A-Za-z0-9]+(?=\\s+)'
cv = CountVectorizer(stop_words=stops_list, token_pattern=TOKENS_ALPHANUMERIC)
bow = cv.fit_transform(bodys)
feature_names = cv.get_feature_names()

obj = {"bow": bow, "feature_names": feature_names}

pickle.dump(obj, open("./bow_and_features.pkl", "w"))

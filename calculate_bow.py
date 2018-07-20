import os
import pymongo
from sklearn.feature_extraction.text import CountVectorizer
import pickle
from nltk.corpus import stopwords

conn = pymongo.MongoClient()


#
# This calculates the count vectorizer
# We then use the count vectorizer later
# to vectorize each document
#
cursor = conn.db.articles.find()
bodys = []
for doc in cursor:
	body = doc['body']
	body = body.lower()
	body = body.replace("\"", " ")
	body = body.replace("'", " ")
	words = body.split()
	parsed_body = " ".join(words)
	bodys.append(parsed_body)

print("Loaded the docs")

stops_list = stopwords.words("english")
TOKENS_ALPHANUMERIC = '[A-Za-z0-9]+(?=\\s+)'
cv = CountVectorizer(stop_words=stops_list, token_pattern=TOKENS_ALPHANUMERIC)
bow = cv.fit_transform(bodys)
feature_names = cv.get_feature_names()

print("Done the vectorizer")

obj = {"bow": bow, "feature_names": feature_names}
# pickle.dump(obj, open("./bow_and_features.pkl", "wb"))
pickle.dump(cv.vocabulary_, open("./count_vectorizer.pkl","wb"))

print("Done saving")

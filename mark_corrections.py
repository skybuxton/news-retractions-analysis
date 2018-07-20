import os
import pymongo
import re

import db

conn = pymongo.MongoClient()

NO_CORRECTION = 0
MAJOR_CORRECTION = 1
MINOR_CORRECTION = 2
BREAKING_NEWS_UPDATE = 3
RESPONSE_UPDATE = 4

def get_correction_info(text):
    # TEXT_TO_SEARCH_FOR => (MAJOR/MINOR, Case Sensitive)
    corrections = {
        'Correction:': (MAJOR_CORRECTION, True),
        'CORRECTION:': (MAJOR_CORRECTION, True),
        'CORRECTION': (MAJOR_CORRECTION, True),
        'Clarification:': (MINOR_CORRECTION, True),
        'Clarifications:': (MINOR_CORRECTION, True),
        'CLARIFICATION': (MINOR_CORRECTION, True),
        'CLARIFICATIONS': (MINOR_CORRECTION, True),
        'Please Note:': (MINOR_CORRECTION, True),
        'PLEASE NOTE:': (MINOR_CORRECTION, True),
        'Typographical Error:': (MINOR_CORRECTION, True),
        'Please Note:': (MINOR_CORRECTION, True),
        'This story has been corrected since it was originally published': (MAJOR_CORRECTION, False),
        'This article has been corrected since it was originally published': (MAJOR_CORRECTION, False),
        'Please Note,': (MINOR_CORRECTION, True),
        'earlier alert': (BREAKING_NEWS_UPDATE, False),
        "editors' note appended": (MINOR_CORRECTION, False),
        "editors note appended": (MINOR_CORRECTION, False),
        'Correction Appended': (MAJOR_CORRECTION, True),
        "Correction notice:": (MAJOR_CORRECTION, False),
        "Update:": (BREAKING_NEWS_UPDATE, False),
        'UPDATE': (BREAKING_NEWS_UPDATE, True),
        "Editor's note:": (RESPONSE_UPDATE, False),
        "Editors note:": (RESPONSE_UPDATE, False),
        "Editors' note:": (RESPONSE_UPDATE, False),
        "Corrections & Amplifications:": (MAJOR_CORRECTION, False),
        'This article was amended': (MAJOR_CORRECTION, False),
        "Editor's note: This story includes a correction.": (MAJOR_CORRECTION,False),
        'CORRECTED-UPDATE': (MAJOR_CORRECTION, True),
        'CORRECTED-UPDATE': (MAJOR_CORRECTION, False),
        'CORRECTED-UPDATE 1-': (MAJOR_CORRECTION, True),
        'CORRECTED-UPDATE 2-': (MAJOR_CORRECTION, True),
        'CORRECTED-UPDATE 3-': (MAJOR_CORRECTION, True),
        'CORRECTED-UPDATE 4-': (MAJOR_CORRECTION, True),
        'CORRECTED-UPDATE 5-': (MAJOR_CORRECTION, True),
        'CORRECTED-UPDATE 6-': (MAJOR_CORRECTION, True),
        'CORRECTED-UPDATE 7-': (MAJOR_CORRECTION, True),
        'CORRECTED-UPDATE 8-': (MAJOR_CORRECTION, True),
        'CORRECTED-UPDATE 9-': (MAJOR_CORRECTION, True),
        'CORRECTED-UPDATE 10-': (MAJOR_CORRECTION, True),
        'CORRECTED-UPDATE 11-': (MAJOR_CORRECTION, True),
        'CORRECTED-UPDATE 12-': (MAJOR_CORRECTION, True),
        'CORRECTED-UPDATE 13-': (MAJOR_CORRECTION, True),
        'CORRECTED-UPDATE 14-': (MAJOR_CORRECTION, True),
        'CORRECTED-UPDATE 15-': (MAJOR_CORRECTION, True),
        'CORRECTED-UPDATE 16-': (MAJOR_CORRECTION, True),
        'CORRECTED-UPDATE 18-': (MAJOR_CORRECTION, True),
        'CORRECTED-UPDATE 19-': (MAJOR_CORRECTION, True),
        'CORRECTED-UPDATE 20-': (MAJOR_CORRECTION, True),
        'WITHDRAWAL': (MAJOR_CORRECTION, True),
        'CORRECTED': (MAJOR_CORRECTION, True),
        'CORRECTED-(OFFICIAL)': (MAJOR_CORRECTION, True),
        'WITHDRAWAL': (MAJOR_CORRECTION, True),
        'may have left the incorrect impression': (MINOR_CORRECTION, True),
        'clarifications:': (MINOR_CORRECTION, False),
        'An earlier version of this article': (MINOR_CORRECTION, False),
        'A previous version of this story': (MINOR_CORRECTION, False),
        'A previous version of this article': (MINOR_CORRECTION, False),
        'An earlier version of this story': (MINOR_CORRECTION, False),
        'An update to this story reflects': (RESPONSE_UPDATE, False),
        'An update to this article reflects': (RESPONSE_UPDATE, False),
        'This version has been corrected': (MAJOR_CORRECTION, False),
        'The original version of this article': (MINOR_CORRECTION, False),
        'The original version of this story': (MINOR_CORRECTION, False),
        'We have unequivocally retracted our story': (MAJOR_CORRECTION, True),
        'We have unequivocally retracted this article': (MAJOR_CORRECTION, True),
        'We regret the error': (MAJOR_CORRECTION, True),
        'Corrections and clarifications:': (MAJOR_CORRECTION, False),
        'Clarifications and corrections:': (MAJOR_CORRECTION, False),
        'We no longer stand by our story': (MAJOR_CORRECTION, True),
        'We no longer stand by this article': (MAJOR_CORRECTION, True),
        'The article has been changed': (MAJOR_CORRECTION, False),
        'The story has been changed': (MAJOR_CORRECTION, False),
        'This story has been changed': (MAJOR_CORRECTION, False),
        'This story has been updated': (RESPONSE_UPDATE, False),
        'This story has been updated throughout.': (BREAKING_NEWS_UPDATE, True),
        'This story was corrected': (MAJOR_CORRECTION, False),
        'The article has been changed': (MAJOR_CORRECTION, False),
        'This article has been changed': (MAJOR_CORRECTION, False),
        'This article has been updated': (RESPONSE_UPDATE, False),
        'This article has been updated throughout.': (BREAKING_NEWS_UPDATE, True),
        'This article was corrected': (MAJOR_CORRECTION, False),
        'Note: This article was published inadvertently and has been removed': (MAJOR_CORRECTION, True),
        'Note: This story was published inadvertently and has been removed': (MAJOR_CORRECTION, True),
        'The article was wrong; it referred incompletely to something (but it was not wrong)': (MINOR_CORRECTION, True),
        'The story was wrong; it referred incompletely to something (but it was not wrong)': (MINOR_CORRECTION, True),
        'The article was wrong; it referred imprecisely to something (but it was not wrong)': (MINOR_CORRECTION, True),
        'The story was wrong; it referred imprecisely to something (but it was not wrong)': (MINOR_CORRECTION, True),
        'This article was published inadvertently and has been removed': (MAJOR_CORRECTION, True),
        'This story was published inadvertently and has been removed': (MAJOR_CORRECTION, True),
        'earlier versions of this article': (MAJOR_CORRECTION, False)
    }
    corrections_info = {}
    for search_for, data in corrections.items():
        (correction_type, case_sensitive) = data
        search_text = text + ''
        search_for_2 = search_for + ''
        if not case_sensitive:
            search_text = search_text.lower()
            search_for_2 = search_for.lower()
        if search_for_2 in search_text:
            index = search_text.index(search_for_2)
            index_str = str(index)
            if index_str in corrections_info:
                corrections_info[index_str].append([correction_type, len(search_for_2), search_for_2])
            else:
                corrections_info[index_str] = [[correction_type, len(search_for_2), search_for_2]]
    return corrections_info

def get_correction_type(text):
    info = get_correction_info(text)
    if len(info) == 0:
        return NO_CORRECTION
    else:
        correction_type = min(map(lambda x: x[0][0], info.values()))
        return correction_type


conn = pymongo.MongoClient()
cursor = conn.db.articles.find({})
results = {
    NO_CORRECTION: 0,
    MINOR_CORRECTION: 0,
    MAJOR_CORRECTION: 0,
    BREAKING_NEWS_UPDATE: 0,
    RESPONSE_UPDATE: 0
}

import tqdm

with tqdm.tqdm(total=cursor.count()) as pbar:
    for doc in cursor:
        title = doc['title']
        body = doc['body']
        fulltext = title + " " + body
        correction_info = get_correction_info(fulltext)
        correction_type = get_correction_type(fulltext)
        results[correction_type] = results[correction_type] + 1

        # print("%s" % {
        #   "correction_type": correction_type,
        #   "correction_info": correction_info
        # })

        db.update_event(doc["_id"], {
            "correction_type": correction_type,
            "correction_info": correction_info
        })
        pbar.update(1)


print("Major Corrections: %s" % results[MAJOR_CORRECTION])
print("Minor Corrections: %s" % results[MINOR_CORRECTION])
print("No Corrections:    %s" % results[NO_CORRECTION])
print("Breaking News Update: %s" % results[BREAKING_NEWS_UPDATE])
print("RESPONSE_UPDATE: %s" % results[RESPONSE_UPDATE])

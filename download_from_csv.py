import requests
import json
import glob
import goose3 as goose
import os
import pandas as pd
import numpy as np
import logging
import sys

# ls *csv | sed 's/^.*$/& &/1' |sed 's/^/python download_from_csv.py /1' | sed 's/_2015.csv//2' | sed 's/[a-z]*/events-&/20'

# cd /Users/navarrabuxton/projects/gdelt-csvs
# cd ~/projects/gdelt-csvs
#ls && say done

# python download_from_csv.py jan_2013.csv jan_2013
# python download_from_csv.py feb_2013.csv feb_2013
# python download_from_csv.py march_2013.csv march_2013
# python download_from_csv.py april_2013.csv april_2013
# python download_from_csv.py may_2013.csv may_2013
# python download_from_csv.py june_2013.csv june_2013
# python download_from_csv.py july_2013.csv july_2013
# python download_from_csv.py aug_2013.csv aug_2013
# python download_from_csv.py sept_2013.csv sept_2013
# python download_from_csv.py oct_2013.csv oct_2013
# python download_from_csv.py nov_2013.csv nov_2013
# python download_from_csv.py dec_2013.csv dec_2013
# python download_from_csv.py jan_2014.csv jan_2014
# python download_from_csv.py feb_2014.csv feb_2014
# python download_from_csv.py march_2014.csv march_2014
# python download_from_csv.py april_2014.csv april_2014
# python download_from_csv.py may_2014.csv may_2014
# python download_from_csv.py june_2014.csv june_2014
# python download_from_csv.py july_2014.csv july_2014
# python download_from_csv.py aug_2014.csv aug_2014
# python download_from_csv.py sept_2014.csv sept_2014
# python download_from_csv.py oct_2014.csv oct_2014
# python download_from_csv.py nov_2014.csv nov_2014
# python download_from_csv.py dec_2014.csv dec_2014
# python download_from_csv.py jan_2015.csv jan_2015
# python download_from_csv.py feb_2015.csv feb_2015
# python download_from_csv.py march_2015.csv march_2015
# python download_from_csv.py april_2015.csv april_2015
# python download_from_csv.py may_2015.csv may_2015
# python download_from_csv.py june_2015.csv june_2015
# python download_from_csv.py july_2015.csv july_2015
# python download_from_csv.py aug_2015.csv aug_2015
# python download_from_csv.py sept_2015.csv sept_2015
# python download_from_csv.py oct_2015.csv oct_2015
# python download_from_csv.py nov_2015.csv nov_2015
# python download_from_csv.py dec_2015.csv dec_2015
# python download_from_csv.py Jan_2016.csv jan_2016
# python download_from_csv.py feb_2016.csv feb_2016
# python download_from_csv.py march_2016.csv march_2016
# python download_from_csv.py april_2016.csv april_2016
# python download_from_csv.py may_2016.csv may_2016
# python download_from_csv.py june_2016.csv june_2016
# python download_from_csv.py july_2016.csv july_2016
# python download_from_csv.py aug_2016.csv aug_2016
# python download_from_csv.py sept_2016.csv sept_2016
# python download_from_csv.py oct_2016.csv oct_2016
# python download_from_csv.py nov_2016.csv nov_2016
# python download_from_csv.py dec_2016.csv dec_2016
# python download_from_csv.py jan_2017.csv jan_2017
# python download_from_csv.py feb_2017.csv feb_2017
# python download_from_csv.py march_2017.csv march_2017
# python download_from_csv.py april_2017.csv april_2017
# python download_from_csv.py may_2017.csv may_2017
# python download_from_csv.py june_2017.csv june_2017
# python download_from_csv.py july_2017.csv july_2017
# NEW:
# python download_from_csv.py aug_2017.csv aug_2017
# python download_from_csv.py sept_2017.csv sept_2017
# python download_from_csv.py oct_2017.csv oct_2017
# python download_from_csv.py nov_2017.csv nov_2017
# python download_from_csv.py dec_2017.csv dec_2017

#### NEW FORMAT

# python download_from_csv.py jan_2013.csv jan_2013_url
# python download_from_csv.py feb_2013.csv feb_2013_url
# python download_from_csv.py march_2013.csv march_2013_url
# python download_from_csv.py april_2013.csv april_2013_url
# python download_from_csv.py may_2013.csv may_2013_url - broken
# python download_from_csv.py june_2013.csv june_2013_url
# python download_from_csv.py july_2013.csv july_2013_url
# python download_from_csv.py aug_2013.csv aug_2013_url
# python download_from_csv.py sept_2013.csv sept_2013_url
# python download_from_csv.py oct_2013.csv oct_2013_url
# python download_from_csv.py nov_2013.csv nov_2013_url
# python download_from_csv.py dec_2013.csv dec_2013_url
# python download_from_csv.py jan_2014.csv jan_2014_url
# python download_from_csv.py feb_2014.csv feb_2014_url
# python download_from_csv.py march_2014.csv march_2014_url
# python download_from_csv.py april_2014.csv april_2014_url
# python download_from_csv.py may_2014.csv may_2014_url
# python download_from_csv.py june_2014.csv june_2014_url
# python download_from_csv.py july_2014.csv july_2014_url
# python download_from_csv.py aug_2014.csv aug_2014_url
# python download_from_csv.py sept_2014.csv sept_2014_url
# python download_from_csv.py oct_2014.csv oct_2014_url
# python download_from_csv.py nov_2014.csv nov_2014_url
# python download_from_csv.py dec_2014.csv dec_2014_url
# python download_from_csv.py jan_2015.csv jan_2015_url
# python download_from_csv.py feb_2015.csv feb_2015_url
# python download_from_csv.py march_2015.csv march_2015_url
# python download_from_csv.py april_2015.csv april_2015_url
# python download_from_csv.py may_2015.csv may_2015_url
# python download_from_csv.py june_2015.csv june_2015_url
# python download_from_csv.py july_2015.csv july_2015_url
# python download_from_csv.py aug_2015.csv aug_2015_url
# python download_from_csv.py sept_2015.csv sept_2015_url
# python download_from_csv.py oct_2015.csv oct_2015_url
# python download_from_csv.py nov_2015.csv nov_2015_url
# python download_from_csv.py dec_2015.csv dec_2015_url
# python download_from_csv.py Jan_2016.csv jan_2016_url
# python download_from_csv.py feb_2016.csv feb_2016_url
# python download_from_csv.py march_2016.csv march_2016_url
# python download_from_csv.py april_2016.csv april_2016_url
# python download_from_csv.py may_2016.csv may_2016_url
# python download_from_csv.py june_2016.csv june_2016_url
# python download_from_csv.py july_2016.csv july_2016_url
# python download_from_csv.py aug_2016.csv aug_2016_url
# python download_from_csv.py sept_2016.csv sept_2016_url
# python download_from_csv.py oct_2016.csv oct_2016_url
# python download_from_csv.py nov_2016.csv nov_2016_url
# python download_from_csv.py dec_2016.csv dec_2016_url
# python download_from_csv.py jan_2017.csv jan_2017_url
# python download_from_csv.py feb_2017.csv feb_2017_url
# python download_from_csv.py march_2017.csv march_2017_url
# python download_from_csv.py april_2017.csv april_2017_url
# python download_from_csv.py may_2017.csv may_2017_url
# python download_from_csv.py june_2017.csv june_2017_url
# python download_from_csv.py july_2017.csv july_2017_url
# NEW:
# python download_from_csv.py aug_2017.csv aug_2017_url
# python download_from_csv.py sept_2017.csv sept_2017_url
# python download_from_csv.py oct_2017.csv oct_2017_url
# python download_from_csv.py nov_2017.csv nov_2017_url
# python download_from_csv.py dec_2017.csv dec_2017_url


USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"

# import signal
# class TimeoutException(Exception):   # Custom exception class
#     pass

# def timeout_handler(signum, frame):   # Custom signal handler
#     raise TimeoutException

# signal.signal(signal.SIGALRM, timeout_handler)


# from interruptingcow import timeout

import stopit

g = goose.Goose({'enable_image_fetching': False})

@stopit.threading_timeoutable(default='timeout')
def download_doc(url):
    global g
    # with timeout(5, exception=RuntimeError):
    headers = {"User-Agent": USER_AGENT}
    print("getting")
    resp = requests.get(url, headers=headers, timeout=0.5)
    print('got')
    # g = goose.Goose({'enable_image_fetching': False})
    print('parsing')
    doc = g.extract(raw_html=resp.text)
    # import time
    # time.sleep(20)
    print('parsed')
    return doc

def md5(s):
    import hashlib
    m = hashlib.md5()
    m.update(s.encode('ascii'))
    return m.hexdigest()

def save_event_to_file(directory, url):
    # filename = "/Users/navarrabuxton/projects/gdelt-events-feb/%s.json" % event_id
    md5str = md5(url)
    filename = "%s/%s.json" % (directory, md5str)
    print("FILENAME %s" % filename)
    if os.path.exists(filename):
        print("Already saved %s" % url)
        return False
    else:
        try:
            print("Downloading %s" % url)
            doc = download_doc(url, timeout=5)#0.1)
            if doc == 'timeout':
                raise Exception("Couldn't download + parse in 5 seconds")
            title = doc.title
            body = doc.cleaned_text
            if body == "" or body == None:
                raise Exception("%s can not be extracted" % url)
            if title == "" or title == None:
                raise Exception("%s can not be extracted" % url)
            d = {"title": title, "url": url, "body": body}
            json_string = json.dumps(d)
            with open(filename, "w") as f:
                f.write(json_string)
            print("Saved file %s" % url)
            return True
        except Exception as e:
            print("FAILED TO DOWNLOAD %s: %s" % (url, e))
            return False

if __name__ == '__main__':
    filename = sys.argv[1]
    output_dir = sys.argv[2]
    # filename = '/Users/navarrabuxton/Downloads/feb-2015.csv'
    print("Loading file: %s" % filename)
    print("Files will be downloaded to: %s" % output_dir)
    if not os.path.exists(filename):
        print("File does not exist: %s" % filename)
        exit(1)
    if not os.path.exists(output_dir):
        print("Directory does not exist: %s - creating" % output_dir)
        os.makedirs(output_dir)
        # exit(1)

    events = pd.DataFrame.from_csv(filename, index_col=None)
    events_len = len(events)
    print("Finished loading %s entries" % events_len)
    print("Shuffling events")
    events = events.sample(frac=1).reset_index(drop=True)
    print("Finished shuffling events")
    count = len(glob.glob("%s/*.json" % output_dir))
    print("We have already downloaded %s articles for this month" % count)
    max_articles = 10000
    sample_number = 15000
    print("Sampling %s entries" % sample_number)
    chosen_idx = np.random.choice(events_len, replace=False, size=sample_number)
    events = events.iloc[chosen_idx]
    print("Finished sampling")
    import gc
    gc.collect()
    for index, row in events.iterrows():
        if count >= max_articles:
            print("We have downloaded the max articles for this month")
            exit(0)
        url = row["SOURCEURL"]
        event_id = row["GLOBALEVENTID"]
        if url != "unspecified":
            # saved = save_event_to_file(output_dir, event_id, url)
            saved = save_event_to_file(output_dir, url)
            if saved:
                count = count + 1


